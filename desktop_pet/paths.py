from __future__ import annotations

import sys
from pathlib import Path


def resource_root() -> Path:
    """Return the root folder used for bundled read-only resources."""
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent.parent


def runtime_root() -> Path:
    """Return the writable folder beside the executable or project root."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent.parent
