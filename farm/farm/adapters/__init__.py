"""Source adapters: turn a raw input (a scoreboard, a directory) into the
profile-neutral records the engine's profiles ingest. One per input kind."""
from .ctfd_source import CTFdSource
from .local_source import LocalSource

__all__ = ["CTFdSource", "LocalSource"]
