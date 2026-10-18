"""Source adapters: raw input (scoreboard, directory) -> profile-neutral records.

Imports are lazy so a local/offline run never pulls the CTFd client's httpx
dependency (keeps the offline path dependency-light on the host).
"""
from __future__ import annotations

__all__ = ["CTFdSource", "LocalSource"]


def __getattr__(name):
    if name == "LocalSource":
        from .local_source import LocalSource
        return LocalSource
    if name == "CTFdSource":
        from .ctfd_source import CTFdSource
        return CTFdSource
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
