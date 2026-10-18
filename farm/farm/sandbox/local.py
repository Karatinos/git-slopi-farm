"""LocalSandbox - scoped temp workdir with timeouts and a scrubbed env.

NOT a security boundary: it runs commands as the current user in a temp dir.
It is the fallback backend for the offline corpus (no untrusted binaries are
executed there) and for dev hosts without Docker. When real untrusted code must
run, use DockerSandbox. The factory logs loudly when it falls back here.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import List, Optional, Tuple

from ..config import SandboxConfig
from .base import ExecResult, Sandbox, SandboxProvider


class LocalSandbox(Sandbox):
    def __init__(self, root: Path, cfg: SandboxConfig):
        # resolve() up front so symlinked temp dirs (/var -> /private/var on
        # macOS) don't cause spurious "path escapes sandbox" mismatches.
        self._root = Path(root).resolve()
        self._cfg = cfg
        self.workdir = str(self._root)

    def _resolve(self, rel: str) -> Path:
        # prevent escape from the sandbox root
        p = (self._root / rel).resolve()
        if not str(p).startswith(str(self._root)):
            raise ValueError(f"path escapes sandbox: {rel}")
        return p

    @staticmethod
    def _s(x) -> str:
        # subprocess may hand back bytes (notably on TimeoutExpired), so always
        # coerce to str before it reaches string-concatenating callers.
        if x is None:
            return ""
        if isinstance(x, bytes):
            return x.decode("utf-8", errors="replace")
        return x

    def run(self, command: str, timeout: Optional[float] = None) -> ExecResult:
        timeout = timeout or self._cfg.tool_timeout
        env = {
            "PATH": os.environ.get("PATH", "/usr/bin:/bin:/usr/local/bin"),
            "HOME": str(self._root),
            "LANG": "C.UTF-8",
            "PYTHONDONTWRITEBYTECODE": "1",
        }
        try:
            proc = subprocess.run(
                ["/bin/sh", "-c", command], cwd=self._root, env=env,
                capture_output=True, text=True, timeout=timeout, errors="ignore")
            return ExecResult(proc.returncode, self._s(proc.stdout),
                              self._s(proc.stderr))
        except subprocess.TimeoutExpired as e:
            return ExecResult(124, self._s(e.stdout),
                              self._s(e.stderr) + f"\n[timeout after {timeout}s]",
                              timed_out=True)
        except Exception as e:  # noqa: BLE001
            return ExecResult(1, "", f"[sandbox error: {e}]")

    def read_file(self, rel_path: str, max_bytes: int = 200_000) -> str:
        p = self._resolve(rel_path)
        if not p.exists():
            return f"[no such file: {rel_path}]"
        data = p.read_bytes()[:max_bytes]
        try:
            return data.decode("utf-8")
        except UnicodeDecodeError:
            return data.decode("latin-1", errors="replace")

    def write_file(self, rel_path: str, content: str) -> None:
        p = self._resolve(rel_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")

    def list_files(self, rel_path: str = ".") -> List[str]:
        base = self._resolve(rel_path)
        if not base.exists():
            return []
        out = []
        for p in sorted(base.rglob("*")):
            if p.is_file():
                out.append(str(p.relative_to(self._root)))
        return out

    def destroy(self) -> None:
        shutil.rmtree(self._root, ignore_errors=True)


class LocalSandboxProvider(SandboxProvider):
    def __init__(self, cfg: SandboxConfig):
        self._cfg = cfg

    @property
    def name(self) -> str:
        return "local"

    def create(self, name: str, seed_files=None, egress_allowlist=None) -> LocalSandbox:
        root = Path(tempfile.mkdtemp(prefix=f"slopi_{_slug(name)}_"))
        for host_path, dest in (seed_files or []):
            dst = root / dest
            dst.parent.mkdir(parents=True, exist_ok=True)
            try:
                shutil.copy2(host_path, dst)
            except Exception:  # noqa: BLE001 - skip unreadable seed files
                pass
        return LocalSandbox(root, self._cfg)


def _slug(s: str) -> str:
    return "".join(c if c.isalnum() else "_" for c in s)[:24]
