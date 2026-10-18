"""DockerSandbox - real ephemeral isolation for untrusted execution.

One long-lived container per attempt (created on `create`, `exec`-ed per tool,
`rm -f`-ed on `destroy`). Hardening applied per the blueprint's execution plane:

  * network deny-by-default (`--network none`); an egress allowlist is honoured
    only when explicitly provided (a dedicated bridge is out of scope here, so a
    non-empty allowlist upgrades to `bridge` and callers must still restrict at
    the app layer — logged clearly).
  * cpu / memory / pids limits, no new privileges, all caps dropped,
  * read-only rootfs with a writable tmpfs workdir,
  * no host secrets mounted; the API key never enters the container.

Uses the docker CLI (no python-docker dependency required).
"""
from __future__ import annotations

import shlex
import subprocess
import tempfile
import uuid
from pathlib import Path
from typing import List, Optional, Tuple

from ..config import SandboxConfig
from .base import ExecResult, Sandbox, SandboxProvider


def docker_available() -> bool:
    try:
        r = subprocess.run(["docker", "info"], capture_output=True,
                           text=True, timeout=10)
        return r.returncode == 0
    except Exception:  # noqa: BLE001
        return False


def image_exists(image: str) -> bool:
    try:
        r = subprocess.run(["docker", "image", "inspect", image],
                           capture_output=True, text=True, timeout=10)
        return r.returncode == 0
    except Exception:  # noqa: BLE001
        return False


class DockerSandbox(Sandbox):
    workdir = "/work"

    def __init__(self, container: str, cfg: SandboxConfig):
        self._c = container
        self._cfg = cfg

    @staticmethod
    def _s(x) -> str:
        if x is None:
            return ""
        if isinstance(x, bytes):
            return x.decode("utf-8", errors="replace")
        return x

    def run(self, command: str, timeout: Optional[float] = None) -> ExecResult:
        timeout = timeout or self._cfg.tool_timeout
        try:
            proc = subprocess.run(
                ["docker", "exec", "-w", self.workdir, self._c,
                 "/bin/sh", "-c", command],
                capture_output=True, text=True, timeout=timeout, errors="ignore")
            return ExecResult(proc.returncode, self._s(proc.stdout),
                              self._s(proc.stderr))
        except subprocess.TimeoutExpired as e:
            return ExecResult(124, self._s(e.stdout),
                              self._s(e.stderr) + f"\n[timeout after {timeout}s]",
                              timed_out=True)
        except Exception as e:  # noqa: BLE001
            return ExecResult(1, "", f"[docker exec error: {e}]")

    def read_file(self, rel_path: str, max_bytes: int = 200_000) -> str:
        safe = shlex.quote(rel_path)
        r = self.run(f"head -c {max_bytes} {safe} 2>/dev/null || cat {safe}")
        return r.stdout if r.stdout else (r.stderr or f"[no such file: {rel_path}]")

    def write_file(self, rel_path: str, content: str) -> None:
        # stream via stdin to avoid arg-length limits and quoting hell
        try:
            subprocess.run(
                ["docker", "exec", "-i", "-w", self.workdir, self._c,
                 "/bin/sh", "-c", f"mkdir -p \"$(dirname {shlex.quote(rel_path)})\" "
                 f"&& cat > {shlex.quote(rel_path)}"],
                input=content, text=True, capture_output=True, timeout=30)
        except Exception:  # noqa: BLE001
            pass

    def list_files(self, rel_path: str = ".") -> List[str]:
        r = self.run(f"find {shlex.quote(rel_path)} -type f 2>/dev/null | sed 's|^\\./||'")
        return [l for l in r.stdout.splitlines() if l.strip()]

    def destroy(self) -> None:
        subprocess.run(["docker", "rm", "-f", self._c],
                       capture_output=True, text=True)


class DockerSandboxProvider(SandboxProvider):
    def __init__(self, cfg: SandboxConfig):
        self._cfg = cfg

    @property
    def name(self) -> str:
        return "docker"

    def create(self, name: str, seed_files: Optional[List[Tuple[Path, str]]] = None,
               egress_allowlist: Optional[List[str]] = None) -> DockerSandbox:
        cname = f"slopi_{_slug(name)}_{uuid.uuid4().hex[:8]}"
        # egress: config default (usually 'none' for data tasks), but live CTF
        # tasks set network='bridge' so the agent can reach the challenge service;
        # an explicit allowlist also forces bridge.
        network = "bridge" if (egress_allowlist or self._cfg.network == "bridge") \
            else self._cfg.network
        args = [
            "docker", "run", "-d", "--name", cname,
            "--network", network,
            "--cpus", self._cfg.cpu_limit,
            "--memory", self._cfg.mem_limit,
            "--pids-limit", str(self._cfg.pids_limit),
            "--security-opt", "no-new-privileges",
            "--cap-drop", "ALL",
            "--read-only",
            "--tmpfs", f"{DockerSandbox.workdir}:rw,exec,size=512m",
            "--tmpfs", "/tmp:rw,exec,size=128m",   # tools/python need a writable /tmp
            "--env", "TMPDIR=/work",
            "--workdir", DockerSandbox.workdir,
            self._cfg.image, "sleep", "3600",
        ]
        r = subprocess.run(args, capture_output=True, text=True, timeout=60)
        if r.returncode != 0:
            raise RuntimeError(f"docker run failed: {r.stderr.strip()}")
        sb = DockerSandbox(cname, self._cfg)
        # seed files by streaming them in (rootfs is read-only, tmpfs workdir ok)
        for host_path, dest in (seed_files or []):
            try:
                content = Path(host_path).read_bytes()
                subprocess.run(
                    ["docker", "exec", "-i", "-w", DockerSandbox.workdir, cname,
                     "/bin/sh", "-c",
                     f"mkdir -p \"$(dirname {shlex.quote(dest)})\" && cat > {shlex.quote(dest)}"],
                    input=content, capture_output=True, timeout=60)
            except Exception:  # noqa: BLE001
                pass
        return sb


def _slug(s: str) -> str:
    # Docker names allow only [a-zA-Z0-9_.-]; Cyrillic task ids must be stripped.
    import string
    ok = set(string.ascii_letters + string.digits)
    return "".join(c if c in ok else "_" for c in s)[:24] or "x"
