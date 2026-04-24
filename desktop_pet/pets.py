from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parent.parent
ASSET_ROOT = APP_ROOT / "assets" / "pet"


@dataclass(frozen=True)
class CharacterDefinition:
    character_id: str
    label: str
    description: str
    folder_path: Path


CHARACTER_DEFINITIONS = {
    "boy": CharacterDefinition(
        character_id="boy",
        label="男生",
        description="Q版男生形象，会随机轮换文件夹中的站立姿态图片。",
        folder_path=ASSET_ROOT / "boy",
    ),
    "girl": CharacterDefinition(
        character_id="girl",
        label="女生",
        description="Q版女生形象，会随机轮换文件夹中的站立姿态图片。",
        folder_path=ASSET_ROOT / "girl",
    ),
}

DEFAULT_CHARACTER_ID = "boy"


def get_character_definition(character_id: str) -> CharacterDefinition:
    return CHARACTER_DEFINITIONS.get(character_id, CHARACTER_DEFINITIONS[DEFAULT_CHARACTER_ID])


def get_character_pose_paths(character_id: str) -> tuple[Path, ...]:
    definition = get_character_definition(character_id)
    if not definition.folder_path.exists():
        return ()

    return tuple(
        sorted(
            (path for path in definition.folder_path.iterdir() if path.is_file() and path.suffix.lower() == ".png"),
            key=lambda path: path.name.lower(),
        )
    )


def get_character_move_frame_paths(character_id: str, direction: str) -> tuple[Path, ...]:
    folder_path = ASSET_ROOT / direction / character_id
    if not folder_path.exists():
        return ()

    return tuple(
        sorted(
            (path for path in folder_path.iterdir() if path.is_file() and path.suffix.lower() == ".png"),
            key=lambda path: path.stem.zfill(8).lower(),
        )
    )


def get_character_left_frame_paths(character_id: str) -> tuple[Path, ...]:
    return get_character_move_frame_paths(character_id, "left")


def get_character_right_frame_paths(character_id: str) -> tuple[Path, ...]:
    return get_character_move_frame_paths(character_id, "right")


def get_character_catch_frame_paths(character_id: str) -> tuple[Path, ...]:
    folder_path = ASSET_ROOT / "catch" / character_id
    if not folder_path.exists():
        return ()

    return tuple(
        sorted(
            (path for path in folder_path.iterdir() if path.is_file() and path.suffix.lower() == ".png"),
            key=lambda path: path.stem.zfill(8).lower(),
        )
    )


def get_character_interact_frame_paths(character_id: str, action_id: str) -> tuple[Path, ...]:
    action_first_folder = ASSET_ROOT / "interact" / action_id / character_id
    gender_first_folder = ASSET_ROOT / "interact" / character_id

    if action_first_folder.exists():
        return _png_files_in_folder(action_first_folder)

    if gender_first_folder.exists():
        action_file = gender_first_folder / f"{action_id}.png"
        if action_file.exists():
            return (action_file,)
        return _png_files_in_folder(gender_first_folder / action_id)

    return ()


def _png_files_in_folder(folder_path: Path) -> tuple[Path, ...]:
    if not folder_path.exists():
        return ()

    return tuple(
        sorted(
            (path for path in folder_path.iterdir() if path.is_file() and path.suffix.lower() == ".png"),
            key=lambda path: path.stem.zfill(8).lower(),
        )
    )
