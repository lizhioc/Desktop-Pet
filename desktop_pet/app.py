from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Optional

from .pets import CHARACTER_DEFINITIONS, DEFAULT_CHARACTER_ID
from .scene import PetScene, TRANSPARENT_COLOR
from .selection import CharacterSelectionDialog
from .settings import (
    get_saved_window_position,
    load_settings,
    remember_selected_character,
    remember_window_position,
)

PET_CLICK_SEQUENCE_MS = 350


def run() -> None:
    root = tk.Tk()
    root.withdraw()
    _configure_styles()

    settings = load_settings()
    selected_character = settings.get("selected_character")

    if selected_character not in CHARACTER_DEFINITIONS:
        selected_character = _choose_character(root, DEFAULT_CHARACTER_ID, allow_cancel=False)
        remember_selected_character(settings, selected_character)

    root.deiconify()
    root.title("桌面宠物")
    root.geometry(_window_geometry(settings))
    root.resizable(False, False)
    root.configure(bg=TRANSPARENT_COLOR)
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    try:
        root.wm_attributes("-transparentcolor", TRANSPARENT_COLOR)
    except tk.TclError:
        pass

    container = ttk.Frame(root, style="Transparent.TFrame")
    container.pack(fill="both", expand=True)

    pending_click_job: Optional[str] = None
    click_count = 0

    scene = PetScene(container, selected_character)
    scene.pack(fill="both", expand=True)

    def apply_character(character_id: str) -> None:
        scene.set_character(character_id)
        remember_selected_character(settings, character_id)

    def open_character_selection() -> None:
        selected = _choose_character(root, scene.character_id, allow_cancel=True)
        if selected:
            apply_character(selected)

    def finalize_character_click() -> None:
        nonlocal pending_click_job, click_count
        current_click_count = click_count
        pending_click_job = None
        click_count = 0

        if current_click_count >= 3:
            scene.hide_menu()
            open_character_selection()

    def handle_character_click() -> None:
        nonlocal pending_click_job, click_count
        click_count += 1
        scene.show_root_menu()

        if pending_click_job:
            root.after_cancel(pending_click_job)

        pending_click_job = root.after(PET_CLICK_SEQUENCE_MS, finalize_character_click)

    def handle_character_drop(window_x: int, window_y: int) -> None:
        remember_window_position(settings, window_x, window_y)

    def show_exit_menu(pointer_x: int, pointer_y: int) -> None:
        menu = tk.Menu(root, tearoff=0)
        menu.add_command(label="退出程序", command=root.destroy)
        try:
            menu.tk_popup(pointer_x, pointer_y)
        finally:
            menu.grab_release()

    scene.set_interaction_callbacks(handle_character_click, show_exit_menu, handle_character_drop)
    scene.start()
    root.mainloop()


def _choose_character(root: tk.Tk, initial_character_id: str, allow_cancel: bool) -> Optional[str]:
    dialog = CharacterSelectionDialog(root, initial_character_id=initial_character_id, allow_cancel=allow_cancel)
    root.wait_window(dialog)
    if allow_cancel:
        return dialog.selected_character
    return dialog.selected_character or DEFAULT_CHARACTER_ID


def _configure_styles() -> None:
    style = ttk.Style()
    style.theme_use("clam")

    style.configure("Surface.TFrame", background="#fff6ea")
    style.configure("Transparent.TFrame", background=TRANSPARENT_COLOR)
    style.configure("Card.TFrame", background="#fffdf8", relief="flat", borderwidth=1)
    style.configure("CardSelected.TFrame", background="#ffe7c7", relief="flat", borderwidth=1)
    style.configure(
        "Title.TLabel",
        background="#fff6ea",
        foreground="#3b342d",
        font=("Microsoft YaHei UI", 17, "bold"),
    )
    style.configure(
        "Body.TLabel",
        background="#fff6ea",
        foreground="#6c6258",
        font=("Microsoft YaHei UI", 10),
    )
    style.configure(
        "CardTitle.TLabel",
        background="#fffdf8",
        foreground="#3b342d",
        font=("Microsoft YaHei UI", 12, "bold"),
    )
    style.configure(
        "CardBody.TLabel",
        background="#fffdf8",
        foreground="#6b6358",
        font=("Microsoft YaHei UI", 9),
    )
    style.configure(
        "Primary.TButton",
        background="#f0b97d",
        foreground="#2d241b",
        font=("Microsoft YaHei UI", 10, "bold"),
        borderwidth=0,
        padding=(14, 8),
    )
    style.map("Primary.TButton", background=[("active", "#f5c48e"), ("pressed", "#e1aa6c")])
    style.configure(
        "Secondary.TButton",
        background="#fff4e6",
        foreground="#5a4737",
        font=("Microsoft YaHei UI", 10),
        borderwidth=1,
        padding=(12, 8),
    )
    style.map("Secondary.TButton", background=[("active", "#fdebd2"), ("pressed", "#f4ddbd")])
    style.configure(
        "Danger.TButton",
        background="#f6ddd7",
        foreground="#74493d",
        font=("Microsoft YaHei UI", 10),
        borderwidth=1,
        padding=(12, 8),
    )
    style.map("Danger.TButton", background=[("active", "#f2d0c7"), ("pressed", "#e8c1b7")])
    style.configure(
        "Card.TRadiobutton",
        background="#fffdf8",
        foreground="#4c433b",
        font=("Microsoft YaHei UI", 10, "bold"),
    )

def _window_geometry(settings: dict) -> str:
    position = get_saved_window_position(settings)
    if position:
        return f"{PetScene.WINDOW_WIDTH}x{PetScene.WINDOW_HEIGHT}+{position[0]}+{position[1]}"
    return _default_geometry()


def _default_window_position() -> tuple[int, int]:
    return 80, 120


def _default_geometry() -> str:
    default_x, default_y = _default_window_position()
    return f"{PetScene.WINDOW_WIDTH}x{PetScene.WINDOW_HEIGHT}+{default_x}+{default_y}"
