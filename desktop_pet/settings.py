from __future__ import annotations

import json
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = APP_ROOT / "data"
SETTINGS_PATH = DATA_DIR / "settings.json"

DEFAULT_SETTINGS = {
    "selected_pet": None,
}


def load_settings() -> dict:
    if not SETTINGS_PATH.exists():
        return DEFAULT_SETTINGS.copy()

    try:
        with SETTINGS_PATH.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except (OSError, json.JSONDecodeError):
        return DEFAULT_SETTINGS.copy()

    settings = DEFAULT_SETTINGS.copy()
    settings.update(data)
    return settings


def save_settings(settings: dict) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with SETTINGS_PATH.open("w", encoding="utf-8") as file:
        json.dump(settings, file, ensure_ascii=False, indent=2)
