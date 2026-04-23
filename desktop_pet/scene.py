from __future__ import annotations

import math
import tkinter as tk
from tkinter import ttk
from typing import Optional

from .pets import PetDrawResult, draw_pet


class PetScene(ttk.Frame):
    def __init__(self, master: tk.Tk, pet_id: str) -> None:
        super().__init__(master, padding=18, style="Surface.TFrame")
        self.master = master
        self.pet_id = pet_id
        self.canvas_width = 520
        self.canvas_height = 400
        self.pet_x = self.canvas_width / 2
        self.pet_y = self.canvas_height / 2 + 8
        self.tick_ms = 33
        self.pet_tag = "pet"
        self.pet_render: Optional[PetDrawResult] = None

        self.canvas = tk.Canvas(
            self,
            width=self.canvas_width,
            height=self.canvas_height,
            bg="#f7fbff",
            highlightthickness=0,
            bd=0,
        )
        self.canvas.pack(fill="both", expand=True)

        ttk.Label(
            self,
            text="鼠标在窗口外时，宠物会朝鼠标方向移动；鼠标进入窗口后，眼神会跟着你走。",
            style="Body.TLabel",
            anchor="center",
            justify="center",
        ).pack(fill="x", pady=(12, 0))

        self._draw_background()
        self._draw_pet()

    def start(self) -> None:
        self.after(self.tick_ms, self._tick)

    def set_pet(self, pet_id: str) -> None:
        if pet_id == self.pet_id:
            return

        self.pet_id = pet_id
        self._draw_pet()

    def _draw_background(self) -> None:
        self.canvas.delete("background")
        width = self.canvas_width
        height = self.canvas_height

        self.canvas.create_rectangle(0, 0, width, height, fill="#f7fbff", outline="", tags=("background",))
        self.canvas.create_oval(24, 36, 184, 144, fill="#eef6ff", outline="", tags=("background",))
        self.canvas.create_oval(330, 24, 500, 130, fill="#fff0dd", outline="", tags=("background",))
        self.canvas.create_oval(16, 286, 230, 426, fill="#edf6ec", outline="", tags=("background",))
        self.canvas.create_oval(300, 278, 524, 430, fill="#fceede", outline="", tags=("background",))
        self.canvas.create_rectangle(0, height - 78, width, height, fill="#e4f0dc", outline="", tags=("background",))
        self.canvas.create_text(
            width / 2,
            34,
            text="Desktop Pet",
            fill="#7d7a78",
            font=("Microsoft YaHei UI", 14, "bold"),
            tags=("background",),
        )

    def _draw_pet(self) -> None:
        self.canvas.delete(self.pet_tag)
        self.pet_render = draw_pet(self.canvas, self.pet_id, self.pet_x, self.pet_y, 1.0, tag=self.pet_tag)
        self._update_pupils(self.pet_x, self.pet_y)

    def _tick(self) -> None:
        pointer_screen_x, pointer_screen_y = self.master.winfo_pointerxy()
        inside_window = self._is_pointer_inside(pointer_screen_x, pointer_screen_y)
        local_x = pointer_screen_x - self.canvas.winfo_rootx()
        local_y = pointer_screen_y - self.canvas.winfo_rooty()

        if inside_window:
            self._update_pupils(local_x, local_y)
        else:
            self._move_toward_pointer(local_x, local_y)

        self.after(self.tick_ms, self._tick)

    def _is_pointer_inside(self, pointer_x: int, pointer_y: int) -> bool:
        left = self.master.winfo_rootx()
        top = self.master.winfo_rooty()
        right = left + self.master.winfo_width()
        bottom = top + self.master.winfo_height()
        return left <= pointer_x <= right and top <= pointer_y <= bottom

    def _move_toward_pointer(self, local_x: float, local_y: float) -> None:
        target_x = self._clamp(local_x, 88, self.canvas_width - 88)
        target_y = self._clamp(local_y, 110, self.canvas_height - 72)

        delta_x = target_x - self.pet_x
        delta_y = target_y - self.pet_y
        distance = math.hypot(delta_x, delta_y)

        if distance < 1:
            self._update_pupils(target_x, target_y)
            return

        speed = min(8.0, max(2.2, distance * 0.08))
        move_x = delta_x / distance * speed
        move_y = delta_y / distance * speed

        self.pet_x += move_x
        self.pet_y += move_y
        self.canvas.move(self.pet_tag, move_x, move_y)
        self._update_pupils(target_x, target_y)

    def _update_pupils(self, target_x: float, target_y: float) -> None:
        if not self.pet_render:
            return

        for pupil_id, eye_spec in zip(self.pet_render.pupil_ids, self.pet_render.eye_specs):
            eye_center_x = self.pet_x + eye_spec.offset_x
            eye_center_y = self.pet_y + eye_spec.offset_y

            delta_x = target_x - eye_center_x
            delta_y = target_y - eye_center_y
            distance = math.hypot(delta_x, delta_y)

            if distance > 0:
                ratio = min(eye_spec.max_offset, distance) / distance
                pupil_x = eye_center_x + delta_x * ratio
                pupil_y = eye_center_y + delta_y * ratio
            else:
                pupil_x = eye_center_x
                pupil_y = eye_center_y

            radius = eye_spec.pupil_radius
            self.canvas.coords(
                pupil_id,
                pupil_x - radius,
                pupil_y - radius,
                pupil_x + radius,
                pupil_y + radius,
            )

    @staticmethod
    def _clamp(value: float, minimum: float, maximum: float) -> float:
        return max(minimum, min(maximum, value))
