"""Importing this package registers every built-in profile by name.

Adding a competition type = add a module here and `@register` it. No engine or
CLI edits, no `if profile == ...`. `core.profile.available()` lists them.
"""
from . import ctf, generic  # noqa: F401  (import side-effect: registration)
