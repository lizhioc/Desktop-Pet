from __future__ import annotations

import random
import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional

from .pets import (
    get_character_catch_frame_paths,
    get_character_interact_frame_paths,
    get_character_left_frame_paths,
    get_character_pose_paths,
    get_character_right_frame_paths,
)

TRANSPARENT_COLOR = "#ff00ff"


class PetScene(ttk.Frame):
    WINDOW_WIDTH = 320
    WINDOW_HEIGHT = 400
    POSE_CHANGE_MIN_MS = 3000
    POSE_CHANGE_MAX_MS = 10000
    IMAGE_SUBSAMPLE = 4
    FOLLOW_TICK_MS = 70
    FOLLOW_STOP_DISTANCE = 54
    FOLLOW_STEP_MAX = 4
    MENU_AUTO_HIDE_MS = 3000
    INTERACTION_DISPLAY_MS = 3000
    MENU_BUTTON_WIDTH = 82
    MENU_BUTTON_HEIGHT = 32
    MENU_BUTTON_GAP = 10
    MENU_SIDE_OFFSET = 94
    MENU_EDGE_PADDING = 10
    FREE_MODE = "free"
    FOLLOW_MODE = "follow"
    MENU_TAG = "interaction-menu"
    INTERACTION_ACTIONS = (
        ("head", "摸头"),
        ("ear", "揪耳朵"),
        ("ass", "拍PP"),
        ("eatcake", "喂蛋糕"),
        ("drink", "喝饮料"),
    )

    def __init__(self, master: tk.Widget, character_id: str) -> None:
        super().__init__(master, style="Transparent.TFrame")
        self.character_id = character_id
        self.canvas_width = self.WINDOW_WIDTH
        self.canvas_height = self.WINDOW_HEIGHT
        self.character_x = self.canvas_width / 2
        self.character_y = self.canvas_height - 8
        self.character_tag = "character"
        self._drag_start_pointer: Optional[tuple[int, int]] = None
        self._drag_start_window: Optional[tuple[int, int]] = None
        self._left_button_down = False
        self._dragging = False
        self._suppress_next_character_click = False
        self._pose_job: Optional[str] = None
        self._follow_job: Optional[str] = None
        self._menu_hide_job: Optional[str] = None
        self._interaction_restore_job: Optional[str] = None
        self._current_pose_index = 0
        self._image_cache: dict[str, list[tk.PhotoImage]] = {}
        self._action_image_cache: dict[str, tk.PhotoImage] = {}
        self._movement_mode = self.FREE_MODE
        self._movement_direction: Optional[str] = None
        self._movement_frame_index = 0
        self._catch_image_visible = False
        self._interaction_image_visible = False
        self._on_character_clicked: Optional[Callable[[], None]] = None
        self._on_character_right_clicked: Optional[Callable[[int, int], None]] = None
        self._on_character_dropped: Optional[Callable[[int, int], None]] = None

        self.canvas = tk.Canvas(
            self,
            width=self.canvas_width,
            height=self.canvas_height,
            bg=TRANSPARENT_COLOR,
            highlightthickness=0,
            bd=0,
        )
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<ButtonPress-1>", self._handle_left_press)
        self.canvas.bind("<B1-Motion>", self._handle_left_drag)
        self.canvas.bind("<ButtonRelease-1>", self._handle_left_release)
        self.canvas.bind("<Button-3>", self._handle_right_click)

        self._draw_character()

    def start(self) -> None:
        self._schedule_next_pose()

    def set_interaction_callbacks(
        self,
        on_character_clicked: Callable[[], None],
        on_character_right_clicked: Callable[[int, int], None],
        on_character_dropped: Callable[[int, int], None],
    ) -> None:
        self._on_character_clicked = on_character_clicked
        self._on_character_right_clicked = on_character_right_clicked
        self._on_character_dropped = on_character_dropped

    def set_character(self, character_id: str) -> None:
        if character_id == self.character_id:
            return

        self.character_id = character_id
        self._current_pose_index = 0
        self._movement_direction = None
        self._movement_frame_index = 0
        self._left_button_down = False
        self._dragging = False
        self._suppress_next_character_click = False
        self._catch_image_visible = False
        self._interaction_image_visible = False
        self._cancel_interaction_restore()
        self._draw_character()
        if self._movement_mode == self.FREE_MODE:
            self._schedule_next_pose()

    def _load_images(self, character_id: str) -> list[tk.PhotoImage]:
        cached_images = self._image_cache.get(character_id)
        if cached_images is not None:
            return cached_images

        pose_paths = get_character_pose_paths(character_id)
        if not pose_paths:
            raise FileNotFoundError(f"角色 {character_id} 的素材文件夹中没有可用的 png 图片。")

        images = [tk.PhotoImage(file=str(pose_path)).subsample(self.IMAGE_SUBSAMPLE, self.IMAGE_SUBSAMPLE) for pose_path in pose_paths]
        self._image_cache[character_id] = images
        return images

    def _draw_character(self) -> None:
        current_image = self._load_images(self.character_id)[self._current_pose_index]
        self._draw_image(current_image)

    def _draw_image(self, image: tk.PhotoImage) -> None:
        self.canvas.delete(self.character_tag)
        self.canvas.create_image(
            self.character_x,
            self.character_y,
            image=image,
            anchor="s",
            tags=(self.character_tag,),
        )
        if self._is_menu_visible():
            self.canvas.tag_raise(self.MENU_TAG)

    def _schedule_next_pose(self) -> None:
        self._cancel_pose_switch()
        delay = random.randint(self.POSE_CHANGE_MIN_MS, self.POSE_CHANGE_MAX_MS)
        self._pose_job = self.after(delay, self._switch_pose)

    def _switch_pose(self) -> None:
        if self._movement_mode != self.FREE_MODE:
            return
        if self._left_button_down or self._dragging or self._catch_image_visible or self._interaction_image_visible:
            self._schedule_next_pose()
            return

        images = self._load_images(self.character_id)
        next_indices = [index for index in range(len(images)) if index != self._current_pose_index]
        if next_indices:
            self._current_pose_index = random.choice(next_indices)
            self._draw_character()
        self._schedule_next_pose()

    def _load_action_image(self, path) -> tk.PhotoImage:
        cache_key = str(path)
        cached_image = self._action_image_cache.get(cache_key)
        if cached_image is not None:
            return cached_image

        if not path.exists():
            raise FileNotFoundError(f"移动动作图片不存在：{path}")

        image = tk.PhotoImage(file=str(path)).subsample(self.IMAGE_SUBSAMPLE, self.IMAGE_SUBSAMPLE)
        self._action_image_cache[cache_key] = image
        return image

    def show_root_menu(self) -> None:
        self._clear_menu_items()
        interact_x, interact_y = self._menu_button_position(0, 2)
        mode_x, mode_y = self._menu_button_position(1, 2)
        self._draw_menu_button(
            center_x=interact_x,
            center_y=interact_y,
            width=self.MENU_BUTTON_WIDTH,
            height=self.MENU_BUTTON_HEIGHT,
            text="互动",
            command=self.show_interaction_menu,
        )
        self._draw_menu_button(
            center_x=mode_x,
            center_y=mode_y,
            width=self.MENU_BUTTON_WIDTH,
            height=self.MENU_BUTTON_HEIGHT,
            text="模式",
            command=self.show_mode_menu,
        )
        self.canvas.tag_raise(self.MENU_TAG)
        self._schedule_menu_auto_hide()

    def show_interaction_menu(self) -> None:
        self._clear_menu_items()
        button_count = len(self.INTERACTION_ACTIONS) + 1
        for index, (action_id, label) in enumerate(self.INTERACTION_ACTIONS):
            button_x, button_y = self._menu_button_position(index, button_count)
            self._draw_menu_button(
                center_x=button_x,
                center_y=button_y,
                width=self.MENU_BUTTON_WIDTH,
                height=self.MENU_BUTTON_HEIGHT,
                text=label,
                command=lambda selected_action=action_id: self.play_interaction(selected_action),
                close_after_click=True,
            )

        back_x, back_y = self._menu_button_position(button_count - 1, button_count)
        self._draw_menu_button(
            center_x=back_x,
            center_y=back_y,
            width=self.MENU_BUTTON_WIDTH,
            height=self.MENU_BUTTON_HEIGHT,
            text="返回",
            command=self.show_root_menu,
        )
        self.canvas.tag_raise(self.MENU_TAG)
        self._schedule_menu_auto_hide()

    def show_mode_menu(self) -> None:
        self._clear_menu_items()
        free_x, free_y = self._menu_button_position(0, 3)
        follow_x, follow_y = self._menu_button_position(1, 3)
        back_x, back_y = self._menu_button_position(2, 3)
        self._draw_menu_button(
            center_x=free_x,
            center_y=free_y,
            width=self.MENU_BUTTON_WIDTH,
            height=self.MENU_BUTTON_HEIGHT,
            text="自由",
            command=self.enable_free_mode,
            close_after_click=True,
        )
        self._draw_menu_button(
            center_x=follow_x,
            center_y=follow_y,
            width=self.MENU_BUTTON_WIDTH,
            height=self.MENU_BUTTON_HEIGHT,
            text="跟随",
            command=self.enable_follow_mode,
            close_after_click=True,
        )
        self._draw_menu_button(
            center_x=back_x,
            center_y=back_y,
            width=self.MENU_BUTTON_WIDTH,
            height=self.MENU_BUTTON_HEIGHT,
            text="返回",
            command=self.show_root_menu,
        )
        self.canvas.tag_raise(self.MENU_TAG)
        self._schedule_menu_auto_hide()

    def hide_menu(self) -> None:
        self._cancel_menu_auto_hide()
        self._clear_menu_items()

    def enable_free_mode(self) -> None:
        self.hide_menu()
        self._cancel_interaction_restore()
        self._interaction_image_visible = False
        self._movement_mode = self.FREE_MODE
        self._cancel_follow()
        self._movement_direction = None
        self._movement_frame_index = 0
        self._draw_character()
        self._schedule_next_pose()

    def enable_follow_mode(self) -> None:
        self.hide_menu()
        self._cancel_interaction_restore()
        self._interaction_image_visible = False
        self._movement_mode = self.FOLLOW_MODE
        self._movement_direction = None
        self._movement_frame_index = 0
        self._cancel_pose_switch()
        self._schedule_follow()

    def _draw_menu_button(
        self,
        center_x: float,
        center_y: float,
        width: int,
        height: int,
        text: str,
        command: Callable[[], None],
        close_after_click: bool = False,
    ) -> None:
        tag = f"{self.MENU_TAG}-{text}"
        left = center_x - width / 2
        top = center_y - height / 2
        right = center_x + width / 2
        bottom = center_y + height / 2
        self.canvas.create_oval(left, top, right, bottom, fill="#4da3ff", outline="", tags=(self.MENU_TAG, tag))
        self.canvas.create_text(
            center_x,
            center_y,
            text=text,
            fill="#000000",
            font=("Microsoft YaHei UI", 9, "bold"),
            tags=(self.MENU_TAG, tag),
        )
        self.canvas.tag_bind(
            tag,
            "<Button-1>",
            lambda event: self._invoke_menu_command(event, command, close_after_click),
        )

    def _menu_button_position(self, index: int, button_count: int) -> tuple[float, float]:
        side = self._menu_side()
        direction = 1 if side == "right" else -1
        center_x = self.character_x + direction * self.MENU_SIDE_OFFSET
        center_x = self._clamp(
            center_x,
            self.MENU_EDGE_PADDING + self.MENU_BUTTON_WIDTH / 2,
            self.canvas_width - self.MENU_EDGE_PADDING - self.MENU_BUTTON_WIDTH / 2,
        )

        total_height = button_count * self.MENU_BUTTON_HEIGHT + (button_count - 1) * self.MENU_BUTTON_GAP
        start_y = self.character_y - 210
        start_y = self._clamp(
            start_y,
            self.MENU_EDGE_PADDING,
            self.canvas_height - self.MENU_EDGE_PADDING - total_height,
        )
        center_y = start_y + self.MENU_BUTTON_HEIGHT / 2 + index * (self.MENU_BUTTON_HEIGHT + self.MENU_BUTTON_GAP)
        return center_x, center_y

    def _menu_side(self) -> str:
        top_level = self.winfo_toplevel()
        character_screen_x = top_level.winfo_x() + self.character_x
        right_edge = character_screen_x + self.MENU_SIDE_OFFSET + self.MENU_BUTTON_WIDTH / 2
        left_edge = character_screen_x - self.MENU_SIDE_OFFSET - self.MENU_BUTTON_WIDTH / 2
        screen_width = top_level.winfo_screenwidth()

        if right_edge > screen_width and left_edge >= 0:
            return "left"
        return "right"

    def _invoke_menu_command(
        self,
        _event: tk.Event,
        command: Callable[[], None],
        close_after_click: bool,
    ) -> str:
        if close_after_click:
            self._suppress_next_character_click = True
            self.hide_menu()
        else:
            self._schedule_menu_auto_hide()
        command()
        return "break"

    def play_interaction(self, action_id: str) -> None:
        frame_paths = get_character_interact_frame_paths(self.character_id, action_id)
        if not frame_paths:
            return

        self._cancel_pose_switch()
        self._cancel_interaction_restore()
        self._movement_direction = None
        self._movement_frame_index = 0
        self._catch_image_visible = False
        self._interaction_image_visible = True
        self._draw_image(self._load_action_image(random.choice(frame_paths)))
        self._interaction_restore_job = self.after(self.INTERACTION_DISPLAY_MS, self._restore_after_interaction)

    def _schedule_follow(self) -> None:
        self._cancel_follow()
        self._follow_job = self.after(self.FOLLOW_TICK_MS, self._follow_pointer)

    def _follow_pointer(self) -> None:
        if self._movement_mode != self.FOLLOW_MODE:
            self._follow_job = None
            return

        if (
            not self._left_button_down
            and not self._dragging
            and not self._interaction_image_visible
            and not self._is_menu_visible()
        ):
            top_level = self.winfo_toplevel()
            pointer_x, pointer_y = top_level.winfo_pointerxy()
            center_x = top_level.winfo_x() + top_level.winfo_width() / 2
            center_y = top_level.winfo_y() + top_level.winfo_height() / 2
            delta_x = pointer_x - center_x
            delta_y = pointer_y - center_y
            distance = max(1.0, (delta_x**2 + delta_y**2) ** 0.5)

            if distance > self.FOLLOW_STOP_DISTANCE:
                step = min(self.FOLLOW_STEP_MAX, max(1, int(distance * 0.035)))
                move_x = int(delta_x / distance * step)
                move_y = int(delta_y / distance * step)
                self._draw_movement_frame("right" if delta_x >= 0 else "left")
                self._move_window_by(move_x, move_y)
            elif self._movement_direction is not None:
                self._movement_direction = None
                self._movement_frame_index = 0
                self._draw_character()

        self._follow_job = self.after(self.FOLLOW_TICK_MS, self._follow_pointer)

    def _draw_movement_frame(self, direction: str) -> None:
        frame_paths = (
            get_character_left_frame_paths(self.character_id)
            if direction == "left"
            else get_character_right_frame_paths(self.character_id)
        )
        frames = [self._load_action_image(path) for path in frame_paths]
        if not frames:
            return

        if self._movement_direction != direction:
            self._movement_direction = direction
            self._movement_frame_index = 0

        self._draw_image(frames[self._movement_frame_index % len(frames)])
        self._movement_frame_index += 1

    def _draw_random_catch_frame(self) -> None:
        frame_paths = get_character_catch_frame_paths(self.character_id)
        if not frame_paths:
            return

        self._draw_image(self._load_action_image(random.choice(frame_paths)))
        self._catch_image_visible = True

    def _restore_after_drag(self) -> None:
        self._catch_image_visible = False
        self._movement_direction = None
        self._movement_frame_index = 0
        self._draw_character()

    def _restore_after_interaction(self) -> None:
        self._interaction_restore_job = None
        self._interaction_image_visible = False
        self._movement_direction = None
        self._movement_frame_index = 0
        self._draw_character()
        if self._movement_mode == self.FREE_MODE:
            self._schedule_next_pose()

    def _move_window_by(self, delta_x: int, delta_y: int) -> None:
        top_level = self.winfo_toplevel()
        screen_width = top_level.winfo_screenwidth()
        screen_height = top_level.winfo_screenheight()
        max_x = max(0, screen_width - top_level.winfo_width())
        max_y = max(0, screen_height - top_level.winfo_height())
        next_x = max(0, min(top_level.winfo_x() + delta_x, max_x))
        next_y = max(0, min(top_level.winfo_y() + delta_y, max_y))
        top_level.geometry(f"+{int(next_x)}+{int(next_y)}")

    def _cancel_pose_switch(self) -> None:
        if self._pose_job:
            self.after_cancel(self._pose_job)
            self._pose_job = None

    def _cancel_follow(self) -> None:
        if self._follow_job:
            self.after_cancel(self._follow_job)
            self._follow_job = None

    def _cancel_interaction_restore(self) -> None:
        if self._interaction_restore_job:
            try:
                self.after_cancel(self._interaction_restore_job)
            except tk.TclError:
                pass
            self._interaction_restore_job = None

    def _schedule_menu_auto_hide(self) -> None:
        self._cancel_menu_auto_hide()
        self._menu_hide_job = self.after(self.MENU_AUTO_HIDE_MS, self._auto_hide_menu)

    def _cancel_menu_auto_hide(self) -> None:
        if self._menu_hide_job:
            try:
                self.after_cancel(self._menu_hide_job)
            except tk.TclError:
                pass
            self._menu_hide_job = None

    def _auto_hide_menu(self) -> None:
        self._menu_hide_job = None
        self._clear_menu_items()

    def _clear_menu_items(self) -> None:
        self.canvas.delete(self.MENU_TAG)

    def _is_menu_visible(self) -> bool:
        return bool(self.canvas.find_withtag(self.MENU_TAG))

    def _handle_left_press(self, event: tk.Event) -> None:
        if self._suppress_next_character_click:
            self._left_button_down = False
            self._drag_start_pointer = None
            self._drag_start_window = None
            self._dragging = False
            return

        if self._pointer_is_over_menu(event.x, event.y):
            self._left_button_down = False
            self._drag_start_pointer = None
            self._drag_start_window = None
            self._dragging = False
            return

        if not self._pointer_is_over_character(event.x, event.y):
            return

        top_level = self.winfo_toplevel()
        self._left_button_down = True
        self._drag_start_pointer = (event.x_root, event.y_root)
        self._drag_start_window = (top_level.winfo_x(), top_level.winfo_y())
        self._dragging = False
        self._cancel_pose_switch()

    def _handle_left_drag(self, event: tk.Event) -> None:
        if not self._drag_start_pointer or not self._drag_start_window:
            return

        start_pointer_x, start_pointer_y = self._drag_start_pointer
        start_window_x, start_window_y = self._drag_start_window
        delta_x = event.x_root - start_pointer_x
        delta_y = event.y_root - start_pointer_y

        if abs(delta_x) > 3 or abs(delta_y) > 3:
            if not self._dragging:
                self.hide_menu()
                self._cancel_interaction_restore()
                self._interaction_image_visible = False
                self._draw_random_catch_frame()
            self._dragging = True

        if not self._dragging:
            return

        top_level = self.winfo_toplevel()
        screen_width = top_level.winfo_screenwidth()
        screen_height = top_level.winfo_screenheight()
        max_x = max(0, screen_width - top_level.winfo_width())
        max_y = max(0, screen_height - top_level.winfo_height())
        next_x = max(0, min(start_window_x + delta_x, max_x))
        next_y = max(0, min(start_window_y + delta_y, max_y))
        top_level.geometry(f"+{int(next_x)}+{int(next_y)}")

    def _handle_left_release(self, event: tk.Event) -> None:
        if self._suppress_next_character_click:
            self._suppress_next_character_click = False
            self._left_button_down = False
            self._drag_start_pointer = None
            self._drag_start_window = None
            self._dragging = False
            self._resume_idle_after_pointer_release()
            return

        if self._pointer_is_over_menu(event.x, event.y):
            self._left_button_down = False
            self._drag_start_pointer = None
            self._drag_start_window = None
            self._dragging = False
            self._resume_idle_after_pointer_release()
            return

        if not self._drag_start_pointer:
            self._left_button_down = False
            self._resume_idle_after_pointer_release()
            return

        was_dragging = self._dragging
        self._left_button_down = False
        self._drag_start_pointer = None
        self._drag_start_window = None
        self._dragging = False

        top_level = self.winfo_toplevel()
        if was_dragging:
            self._restore_after_drag()
            self._resume_idle_after_pointer_release()
            if self._on_character_dropped:
                self._on_character_dropped(top_level.winfo_x(), top_level.winfo_y())
            return

        self._resume_idle_after_pointer_release()
        if self._pointer_is_over_character(event.x, event.y) and self._on_character_clicked:
            self._on_character_clicked()

    def _resume_idle_after_pointer_release(self) -> None:
        if self._movement_mode == self.FREE_MODE:
            self._schedule_next_pose()

    def _handle_right_click(self, event: tk.Event) -> None:
        if self._pointer_is_over_character(event.x, event.y) and self._on_character_right_clicked:
            self._on_character_right_clicked(event.x_root, event.y_root)

    def _pointer_is_over_character(self, x: int, y: int) -> bool:
        overlapping_items = self.canvas.find_overlapping(x, y, x, y)
        for item_id in reversed(overlapping_items):
            if self.character_tag in self.canvas.gettags(item_id):
                return True
        return False

    def _pointer_is_over_menu(self, x: int, y: int) -> bool:
        overlapping_items = self.canvas.find_overlapping(x, y, x, y)
        for item_id in reversed(overlapping_items):
            if self.MENU_TAG in self.canvas.gettags(item_id):
                return True
        return False

    @staticmethod
    def _clamp(value: float, minimum: float, maximum: float) -> float:
        return max(minimum, min(maximum, value))
