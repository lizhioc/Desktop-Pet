from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Tuple
import tkinter as tk


@dataclass(frozen=True)
class EyeSpec:
    offset_x: float
    offset_y: float
    white_radius: float
    pupil_radius: float
    max_offset: float


@dataclass(frozen=True)
class PetDrawResult:
    pupil_ids: Tuple[int, ...]
    eye_specs: Tuple[EyeSpec, ...]


@dataclass(frozen=True)
class PetDefinition:
    pet_id: str
    label: str
    accent: str
    description: str
    draw_fn: Callable[[tk.Canvas, float, float, float, str], PetDrawResult]


def oval_coords(center_x: float, center_y: float, radius_x: float, radius_y: float) -> Tuple[float, float, float, float]:
    return (
        center_x - radius_x,
        center_y - radius_y,
        center_x + radius_x,
        center_y + radius_y,
    )


def circle_coords(center_x: float, center_y: float, radius: float) -> Tuple[float, float, float, float]:
    return oval_coords(center_x, center_y, radius, radius)


def _create_eye(
    canvas: tk.Canvas,
    tag: str,
    center_x: float,
    center_y: float,
    eye_spec: EyeSpec,
) -> int:
    canvas.create_oval(
        *circle_coords(center_x, center_y, eye_spec.white_radius),
        fill="#ffffff",
        outline="",
        tags=(tag,),
    )
    return canvas.create_oval(
        *circle_coords(center_x, center_y, eye_spec.pupil_radius),
        fill="#1f1e24",
        outline="",
        tags=(tag,),
    )


def _draw_rabbit(canvas: tk.Canvas, center_x: float, center_y: float, scale: float, tag: str) -> PetDrawResult:
    eye_specs = (
        EyeSpec(-24 * scale, -18 * scale, 12 * scale, 4.4 * scale, 4.5 * scale),
        EyeSpec(24 * scale, -18 * scale, 12 * scale, 4.4 * scale, 4.5 * scale),
    )

    canvas.create_oval(
        *oval_coords(center_x, center_y + 74 * scale, 42 * scale, 12 * scale),
        fill="#d1d8df",
        outline="",
        tags=(tag,),
    )
    canvas.create_oval(
        *oval_coords(center_x, center_y + 34 * scale, 55 * scale, 48 * scale),
        fill="#f4efe9",
        outline="",
        tags=(tag,),
    )
    canvas.create_oval(
        *oval_coords(center_x - 18 * scale, center_y + 55 * scale, 15 * scale, 11 * scale),
        fill="#efe3d9",
        outline="",
        tags=(tag,),
    )
    canvas.create_oval(
        *oval_coords(center_x + 18 * scale, center_y + 55 * scale, 15 * scale, 11 * scale),
        fill="#efe3d9",
        outline="",
        tags=(tag,),
    )

    for offset_x in (-27 * scale, 27 * scale):
        canvas.create_oval(
            *oval_coords(center_x + offset_x, center_y - 90 * scale, 13 * scale, 52 * scale),
            fill="#f4efe9",
            outline="",
            tags=(tag,),
        )
        canvas.create_oval(
            *oval_coords(center_x + offset_x, center_y - 92 * scale, 6 * scale, 33 * scale),
            fill="#efb8c6",
            outline="",
            tags=(tag,),
        )

    canvas.create_oval(
        *oval_coords(center_x, center_y - 6 * scale, 64 * scale, 58 * scale),
        fill="#fbf7f2",
        outline="",
        tags=(tag,),
    )
    canvas.create_oval(
        *oval_coords(center_x - 23 * scale, center_y + 4 * scale, 12 * scale, 9 * scale),
        fill="#ffe8ef",
        outline="",
        tags=(tag,),
    )
    canvas.create_oval(
        *oval_coords(center_x + 23 * scale, center_y + 4 * scale, 12 * scale, 9 * scale),
        fill="#ffe8ef",
        outline="",
        tags=(tag,),
    )

    pupil_ids = []
    for eye_spec in eye_specs:
        pupil_ids.append(
            _create_eye(
                canvas,
                tag,
                center_x + eye_spec.offset_x,
                center_y + eye_spec.offset_y,
                eye_spec,
            )
        )

    canvas.create_oval(
        *oval_coords(center_x, center_y + 4 * scale, 10 * scale, 7 * scale),
        fill="#ef9fb2",
        outline="",
        tags=(tag,),
    )
    canvas.create_line(
        center_x,
        center_y + 10 * scale,
        center_x,
        center_y + 18 * scale,
        smooth=True,
        fill="#8f6a71",
        width=2,
        tags=(tag,),
    )
    canvas.create_arc(
        center_x - 16 * scale,
        center_y + 10 * scale,
        center_x,
        center_y + 26 * scale,
        start=215,
        extent=115,
        style=tk.ARC,
        outline="#8f6a71",
        width=2,
        tags=(tag,),
    )
    canvas.create_arc(
        center_x,
        center_y + 10 * scale,
        center_x + 16 * scale,
        center_y + 26 * scale,
        start=205,
        extent=115,
        style=tk.ARC,
        outline="#8f6a71",
        width=2,
        tags=(tag,),
    )

    return PetDrawResult(tuple(pupil_ids), eye_specs)


def _draw_cat(canvas: tk.Canvas, center_x: float, center_y: float, scale: float, tag: str) -> PetDrawResult:
    eye_specs = (
        EyeSpec(-24 * scale, -16 * scale, 12 * scale, 4.3 * scale, 4.5 * scale),
        EyeSpec(24 * scale, -16 * scale, 12 * scale, 4.3 * scale, 4.5 * scale),
    )

    canvas.create_oval(
        *oval_coords(center_x, center_y + 76 * scale, 44 * scale, 12 * scale),
        fill="#d6dde4",
        outline="",
        tags=(tag,),
    )
    canvas.create_oval(
        *oval_coords(center_x, center_y + 38 * scale, 57 * scale, 48 * scale),
        fill="#c6a67f",
        outline="",
        tags=(tag,),
    )
    canvas.create_oval(
        *oval_coords(center_x - 16 * scale, center_y + 60 * scale, 16 * scale, 9 * scale),
        fill="#b08d64",
        outline="",
        tags=(tag,),
    )
    canvas.create_oval(
        *oval_coords(center_x + 16 * scale, center_y + 60 * scale, 16 * scale, 9 * scale),
        fill="#b08d64",
        outline="",
        tags=(tag,),
    )

    canvas.create_oval(
        *oval_coords(center_x, center_y - 2 * scale, 66 * scale, 55 * scale),
        fill="#d8b387",
        outline="",
        tags=(tag,),
    )
    canvas.create_polygon(
        center_x - 50 * scale,
        center_y - 26 * scale,
        center_x - 20 * scale,
        center_y - 90 * scale,
        center_x - 2 * scale,
        center_y - 24 * scale,
        fill="#d8b387",
        outline="",
        tags=(tag,),
    )
    canvas.create_polygon(
        center_x + 50 * scale,
        center_y - 26 * scale,
        center_x + 20 * scale,
        center_y - 90 * scale,
        center_x + 2 * scale,
        center_y - 24 * scale,
        fill="#d8b387",
        outline="",
        tags=(tag,),
    )
    canvas.create_polygon(
        center_x - 38 * scale,
        center_y - 30 * scale,
        center_x - 20 * scale,
        center_y - 72 * scale,
        center_x - 8 * scale,
        center_y - 24 * scale,
        fill="#f3c6d0",
        outline="",
        tags=(tag,),
    )
    canvas.create_polygon(
        center_x + 38 * scale,
        center_y - 30 * scale,
        center_x + 20 * scale,
        center_y - 72 * scale,
        center_x + 8 * scale,
        center_y - 24 * scale,
        fill="#f3c6d0",
        outline="",
        tags=(tag,),
    )

    canvas.create_oval(
        *oval_coords(center_x, center_y + 11 * scale, 36 * scale, 25 * scale),
        fill="#f3ddc1",
        outline="",
        tags=(tag,),
    )

    pupil_ids = []
    for eye_spec in eye_specs:
        pupil_ids.append(
            _create_eye(
                canvas,
                tag,
                center_x + eye_spec.offset_x,
                center_y + eye_spec.offset_y,
                eye_spec,
            )
        )

    canvas.create_polygon(
        center_x,
        center_y + 2 * scale,
        center_x - 8 * scale,
        center_y + 12 * scale,
        center_x + 8 * scale,
        center_y + 12 * scale,
        fill="#b76e7c",
        outline="",
        tags=(tag,),
    )
    canvas.create_line(
        center_x - 20 * scale,
        center_y + 13 * scale,
        center_x - 48 * scale,
        center_y + 9 * scale,
        fill="#7b5e42",
        width=2,
        tags=(tag,),
    )
    canvas.create_line(
        center_x - 20 * scale,
        center_y + 18 * scale,
        center_x - 48 * scale,
        center_y + 24 * scale,
        fill="#7b5e42",
        width=2,
        tags=(tag,),
    )
    canvas.create_line(
        center_x + 20 * scale,
        center_y + 13 * scale,
        center_x + 48 * scale,
        center_y + 9 * scale,
        fill="#7b5e42",
        width=2,
        tags=(tag,),
    )
    canvas.create_line(
        center_x + 20 * scale,
        center_y + 18 * scale,
        center_x + 48 * scale,
        center_y + 24 * scale,
        fill="#7b5e42",
        width=2,
        tags=(tag,),
    )
    canvas.create_arc(
        center_x - 12 * scale,
        center_y + 10 * scale,
        center_x + 12 * scale,
        center_y + 28 * scale,
        start=200,
        extent=140,
        style=tk.ARC,
        outline="#7b5e42",
        width=2,
        tags=(tag,),
    )

    return PetDrawResult(tuple(pupil_ids), eye_specs)


def _draw_dog(canvas: tk.Canvas, center_x: float, center_y: float, scale: float, tag: str) -> PetDrawResult:
    eye_specs = (
        EyeSpec(-24 * scale, -14 * scale, 12 * scale, 4.2 * scale, 4.4 * scale),
        EyeSpec(24 * scale, -14 * scale, 12 * scale, 4.2 * scale, 4.4 * scale),
    )

    canvas.create_oval(
        *oval_coords(center_x, center_y + 78 * scale, 46 * scale, 12 * scale),
        fill="#d1d9e0",
        outline="",
        tags=(tag,),
    )
    canvas.create_oval(
        *oval_coords(center_x, center_y + 40 * scale, 56 * scale, 48 * scale),
        fill="#d8b48a",
        outline="",
        tags=(tag,),
    )
    canvas.create_oval(
        *oval_coords(center_x - 18 * scale, center_y + 60 * scale, 16 * scale, 11 * scale),
        fill="#c89a67",
        outline="",
        tags=(tag,),
    )
    canvas.create_oval(
        *oval_coords(center_x + 18 * scale, center_y + 60 * scale, 16 * scale, 11 * scale),
        fill="#c89a67",
        outline="",
        tags=(tag,),
    )

    canvas.create_oval(
        *oval_coords(center_x, center_y - 4 * scale, 65 * scale, 55 * scale),
        fill="#e9c49b",
        outline="",
        tags=(tag,),
    )
    canvas.create_oval(
        *oval_coords(center_x - 48 * scale, center_y - 28 * scale, 18 * scale, 38 * scale),
        fill="#9d6e49",
        outline="",
        tags=(tag,),
    )
    canvas.create_oval(
        *oval_coords(center_x + 48 * scale, center_y - 28 * scale, 18 * scale, 38 * scale),
        fill="#9d6e49",
        outline="",
        tags=(tag,),
    )
    canvas.create_oval(
        *oval_coords(center_x, center_y + 12 * scale, 36 * scale, 28 * scale),
        fill="#f2dfc7",
        outline="",
        tags=(tag,),
    )
    canvas.create_oval(
        *oval_coords(center_x - 30 * scale, center_y - 2 * scale, 11 * scale, 9 * scale),
        fill="#f7e9d8",
        outline="",
        tags=(tag,),
    )
    canvas.create_oval(
        *oval_coords(center_x + 30 * scale, center_y - 2 * scale, 11 * scale, 9 * scale),
        fill="#f7e9d8",
        outline="",
        tags=(tag,),
    )

    pupil_ids = []
    for eye_spec in eye_specs:
        pupil_ids.append(
            _create_eye(
                canvas,
                tag,
                center_x + eye_spec.offset_x,
                center_y + eye_spec.offset_y,
                eye_spec,
            )
        )

    canvas.create_oval(
        *oval_coords(center_x, center_y + 8 * scale, 11 * scale, 8 * scale),
        fill="#2b2a30",
        outline="",
        tags=(tag,),
    )
    canvas.create_arc(
        center_x - 18 * scale,
        center_y + 10 * scale,
        center_x + 18 * scale,
        center_y + 30 * scale,
        start=200,
        extent=140,
        style=tk.ARC,
        outline="#73533c",
        width=2,
        tags=(tag,),
    )
    canvas.create_line(
        center_x,
        center_y + 16 * scale,
        center_x,
        center_y + 24 * scale,
        fill="#73533c",
        width=2,
        tags=(tag,),
    )

    return PetDrawResult(tuple(pupil_ids), eye_specs)


PET_DEFINITIONS = {
    "rabbit": PetDefinition(
        pet_id="rabbit",
        label="小兔",
        accent="#f3becb",
        description="软绵绵的小兔，耳朵长长，表情温柔。",
        draw_fn=_draw_rabbit,
    ),
    "cat": PetDefinition(
        pet_id="cat",
        label="小猫",
        accent="#d7a46f",
        description="机灵的小猫，耳朵尖尖，眼神灵动。",
        draw_fn=_draw_cat,
    ),
    "dog": PetDefinition(
        pet_id="dog",
        label="小狗",
        accent="#b47c4e",
        description="黏人的小狗，耳朵垂垂，动作活泼。",
        draw_fn=_draw_dog,
    ),
}

DEFAULT_PET_ID = "rabbit"


def get_pet_definition(pet_id: str) -> PetDefinition:
    return PET_DEFINITIONS.get(pet_id, PET_DEFINITIONS[DEFAULT_PET_ID])


def draw_pet(
    canvas: tk.Canvas,
    pet_id: str,
    center_x: float,
    center_y: float,
    scale: float,
    tag: str = "pet",
) -> PetDrawResult:
    pet = get_pet_definition(pet_id)
    return pet.draw_fn(canvas, center_x, center_y, scale, tag)
