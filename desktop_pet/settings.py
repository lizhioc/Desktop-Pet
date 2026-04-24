from __future__ import annotations

import json
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = APP_ROOT / "data"
SETTINGS_PATH = DATA_DIR / "settings.json"

DEFAULT_SETTINGS = {
    "selected_character": None,
    "window_x": None,
    "window_y": None,
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


def remember_selected_character(settings: dict, character_id: str) -> None:
    settings["selected_character"] = character_id
    save_settings(settings)


def get_saved_window_position(settings: dict) -> tuple[int, int] | None:
    window_x = settings.get("window_x")
    window_y = settings.get("window_y")
    if isinstance(window_x, int) and isinstance(window_y, int):
        return window_x, window_y
    return None


def remember_window_position(settings: dict, window_x: int, window_y: int) -> None:
    settings["window_x"] = int(window_x)
    settings["window_y"] = int(window_y)
    save_settings(settings)
