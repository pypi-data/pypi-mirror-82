#!/usr/bin/env python3

try:
    # From python3.8
    from importlib.metadata import version
except (ModuleNotFoundError):
    # Prior to python3.8
    from importlib_metadata import version

try:
    __version__ = version(__name__)
except (PackageNotFoundError, ModuleNotFoundError):
    __version__ = "?"
