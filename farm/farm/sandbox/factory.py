"""Sandbox backend selection.

`auto` prefers Docker when the daemon is up and the sandbox image exists,
otherwise falls back to LocalSandbox with a clear warning (isolation is a
non-negotiable per the blueprint, so the fallback is logged, not silent).
"""
from __future__ import annotations

import logging

from ..config import SandboxConfig, SETTINGS
from .base import SandboxProvider
from .local import LocalSandboxProvider

log = logging.getLogger("slopi.sandbox")


def make_provider(cfg: SandboxConfig = None) -> SandboxProvider:
    cfg = cfg or SETTINGS.sandbox
    backend = cfg.backend
    if backend in ("docker", "auto"):
        from .docker import DockerSandboxProvider, docker_available, image_exists
        if docker_available() and image_exists(cfg.image):
            return DockerSandboxProvider(cfg)
        if backend == "docker":
            raise RuntimeError(
                f"docker backend requested but unavailable or image '{cfg.image}' "
                "missing (build it with sandbox/Dockerfile)")
        log.warning("sandbox: docker/image unavailable -> falling back to LOCAL "
                    "(not isolated; fine for the offline corpus)")
    return LocalSandboxProvider(cfg)
