"""Sandbox interfaces (execution plane, blueprint §9/§10).

A sandbox is created per attempt, seeded with the task's agent-visible files,
used to run tools, then destroyed. Two backends implement this contract:

  * DockerSandbox - real isolation: ephemeral container, network deny-by-default,
    cpu/mem/pids limits, read-only rootfs + tmpfs workdir. Preferred.
  * LocalSandbox  - a scoped temp workdir with timeouts and a scrubbed env, for
    hosts without Docker (e.g. quick dev on macOS). Not true isolation; used
    only for the offline corpus where no untrusted binaries are executed.

The interface is deliberately narrow so a Firecracker/gVisor backend can drop in
on Linux without touching tools or the agent.
"""
from __future__ import annotations

import abc
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple


@dataclass
class ExecResult:
    exit_code: int
    stdout: str
    stderr: str
    timed_out: bool = False

    @property
    def ok(self) -> bool:
        return self.exit_code == 0 and not self.timed_out


class Sandbox(abc.ABC):
    """One ephemeral execution environment for a single attempt."""

    workdir: str = "/work"

    @abc.abstractmethod
    def run(self, command: str, timeout: Optional[float] = None) -> ExecResult:
        ...

    @abc.abstractmethod
    def read_file(self, rel_path: str, max_bytes: int = 200_000) -> str:
        ...

    @abc.abstractmethod
    def write_file(self, rel_path: str, content: str) -> None:
        ...

    @abc.abstractmethod
    def list_files(self, rel_path: str = ".") -> List[str]:
        ...

    @abc.abstractmethod
    def destroy(self) -> None:
        ...

    def __enter__(self) -> "Sandbox":
        return self

    def __exit__(self, *exc) -> None:
        self.destroy()


class SandboxProvider(abc.ABC):
    @abc.abstractmethod
    def create(self, name: str, seed_files: Optional[List[Tuple[Path, str]]] = None,
               egress_allowlist: Optional[List[str]] = None) -> Sandbox:
        """seed_files: list of (host_path, dest_relative). egress_allowlist:
        hostnames the sandbox may reach (default: none = deny all)."""
        ...

    @property
    @abc.abstractmethod
    def name(self) -> str:
        ...
