from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from .pets import DEFAULT_PET_ID, PET_DEFINITIONS
from .scene import PetScene
from .selection import PetSelectionDialog
from .settings import clear_selected_pet, load_settings, remember_selected_pet
from .settings_panel import SettingsPanel


def run() -> None:
    root = tk.Tk()
    root.withdraw()
    _configure_styles()

    settings = load_settings()
    selected_pet = settings.get("selected_pet")

    if selected_pet not in PET_DEFINITIONS:
        dialog = PetSelectionDialog(root)
        root.wait_window(dialog)
        selected_pet = dialog.selected_pet or DEFAULT_PET_ID
        remember_selected_pet(settings, selected_pet)

    root.deiconify()
    root.title("桌面宠物")
    root.geometry("560x500")
    root.resizable(False, False)
    root.configure(bg="#fff6ea")

    container = ttk.Frame(root, padding=18, style="Surface.TFrame")
    container.pack(fill="both", expand=True)

    top_bar = ttk.Frame(container, style="Surface.TFrame")
    top_bar.pack(fill="x", pady=(0, 12))

    pet_name_var = tk.StringVar(value=_pet_status_text(selected_pet))
    startup_mode_var = tk.StringVar(value=_startup_mode_text(settings))
    settings_panel: SettingsPanel | None = None

    ttk.Label(
        top_bar,
        textvariable=pet_name_var,
        style="Subtitle.TLabel",
    ).pack(side="left")

    ttk.Label(
        top_bar,
        textvariable=startup_mode_var,
        style="Muted.TLabel",
    ).pack(side="left", padx=(12, 0))

    scene = PetScene(container, selected_pet)

    def refresh_panel_state() -> None:
        remember_enabled = settings.get("selected_pet") != scene.pet_id
        clear_enabled = settings.get("selected_pet") is not None
        pet_name_var.set(_pet_status_text(scene.pet_id))
        startup_mode_var.set(_startup_mode_text(settings))

        if settings_panel and settings_panel.winfo_exists():
            settings_panel.update_state(
                current_pet_text=_pet_status_text(scene.pet_id),
                startup_mode_text=_startup_mode_text(settings),
                remember_enabled=remember_enabled,
                clear_enabled=clear_enabled,
            )

    def handle_reselect() -> None:
        dialog = PetSelectionDialog(root, initial_pet_id=scene.pet_id, allow_cancel=True)
        root.wait_window(dialog)

        if not dialog.selected_pet or dialog.selected_pet == scene.pet_id:
            return

        scene.set_pet(dialog.selected_pet)
        remember_selected_pet(settings, dialog.selected_pet)
        refresh_panel_state()

    def handle_restore_default() -> None:
        scene.set_pet(DEFAULT_PET_ID)
        remember_selected_pet(settings, DEFAULT_PET_ID)
        refresh_panel_state()

    def handle_clear_startup_choice() -> None:
        clear_selected_pet(settings)
        refresh_panel_state()

    def handle_remember_current_pet() -> None:
        remember_selected_pet(settings, scene.pet_id)
        refresh_panel_state()

    def open_settings_panel() -> None:
        nonlocal settings_panel
        if settings_panel and settings_panel.winfo_exists():
            settings_panel.focus_panel()
            return

        settings_panel = SettingsPanel(
            master=root,
            current_pet_text=_pet_status_text(scene.pet_id),
            startup_mode_text=_startup_mode_text(settings),
            on_reselect=handle_reselect,
            on_restore_default=handle_restore_default,
            on_clear_startup_choice=handle_clear_startup_choice,
            on_remember_current_pet=handle_remember_current_pet,
        )
        refresh_panel_state()

    ttk.Button(
        top_bar,
        text="设置",
        command=open_settings_panel,
        style="Secondary.TButton",
    ).pack(side="right")

    scene.pack(fill="both", expand=True)
    scene.start()

    root.mainloop()


def _configure_styles() -> None:
    style = ttk.Style()
    style.theme_use("clam")

    style.configure("Surface.TFrame", background="#fff6ea")
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
        "Subtitle.TLabel",
        background="#fff6ea",
        foreground="#5a4d41",
        font=("Microsoft YaHei UI", 10, "bold"),
    )
    style.configure(
        "Muted.TLabel",
        background="#fff6ea",
        foreground="#88796c",
        font=("Microsoft YaHei UI", 9),
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
    style.map(
        "Primary.TButton",
        background=[("active", "#f5c48e"), ("pressed", "#e1aa6c")],
    )
    style.configure(
        "Secondary.TButton",
        background="#fff4e6",
        foreground="#5a4737",
        font=("Microsoft YaHei UI", 10),
        borderwidth=1,
        padding=(12, 8),
    )
    style.map(
        "Secondary.TButton",
        background=[("active", "#fdebd2"), ("pressed", "#f4ddbd")],
    )
    style.configure(
        "Danger.TButton",
        background="#f6ddd7",
        foreground="#74493d",
        font=("Microsoft YaHei UI", 10),
        borderwidth=1,
        padding=(12, 8),
    )
    style.map(
        "Danger.TButton",
        background=[("active", "#f2d0c7"), ("pressed", "#e8c1b7")],
    )
    style.configure(
        "Card.TRadiobutton",
        background="#fffdf8",
        foreground="#4c433b",
        font=("Microsoft YaHei UI", 10, "bold"),
    )
    style.configure(
        "PanelLabel.TLabel",
        background="#fffdf8",
        foreground="#7d7065",
        font=("Microsoft YaHei UI", 9),
    )
    style.configure(
        "PanelValue.TLabel",
        background="#fffdf8",
        foreground="#3b342d",
        font=("Microsoft YaHei UI", 11, "bold"),
    )
    style.configure(
        "PanelHint.TLabel",
        background="#fffdf8",
        foreground="#5d5349",
        font=("Microsoft YaHei UI", 9),
    )


def _pet_status_text(pet_id: str) -> str:
    pet = PET_DEFINITIONS.get(pet_id, PET_DEFINITIONS[DEFAULT_PET_ID])
    return f"当前陪伴你的是：{pet.label}"


def _startup_mode_text(settings: dict) -> str:
    selected_pet = settings.get("selected_pet")
    if selected_pet in PET_DEFINITIONS:
        pet = PET_DEFINITIONS[selected_pet]
        return f"下次启动会直接使用：{pet.label}"
    return "下次启动会重新进入宠物选择界面"
