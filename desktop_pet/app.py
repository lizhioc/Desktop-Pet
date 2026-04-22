from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from .pets import DEFAULT_PET_ID, PET_DEFINITIONS
from .scene import PetScene
from .selection import PetSelectionDialog
from .settings import load_settings, save_settings


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
        settings["selected_pet"] = selected_pet
        save_settings(settings)

    root.deiconify()
    root.title("桌面宠物")
    root.geometry("560x500")
    root.resizable(False, False)
    root.configure(bg="#fff6ea")

    scene = PetScene(root, selected_pet)
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
        "Card.TRadiobutton",
        background="#fffdf8",
        foreground="#4c433b",
        font=("Microsoft YaHei UI", 10, "bold"),
    )
