from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Dict, Optional

from .pets import PET_DEFINITIONS, DEFAULT_PET_ID, draw_pet


class PetSelectionDialog(tk.Toplevel):
    def __init__(self, master: tk.Tk) -> None:
        super().__init__(master)
        self.selected_pet: Optional[str] = None
        self.choice = tk.StringVar(value=DEFAULT_PET_ID)
        self._card_frames: Dict[str, ttk.Frame] = {}

        self.title("选择你的桌面宠物")
        self.configure(bg="#fff6ea")
        self.resizable(False, False)
        if master.state() != "withdrawn":
            self.transient(master)
        self.grab_set()

        self._build()
        self._refresh_highlight()
        self._show_dialog()

        self.protocol("WM_DELETE_WINDOW", self._confirm)

    def _build(self) -> None:
        wrapper = ttk.Frame(self, padding=20, style="Surface.TFrame")
        wrapper.pack(fill="both", expand=True)

        ttk.Label(
            wrapper,
            text="第一次见面，先挑一个陪你的宠物吧",
            style="Title.TLabel",
        ).pack(anchor="w")
        ttk.Label(
            wrapper,
            text="本次会记住你的选择，后续启动默认直接进入主界面。",
            style="Body.TLabel",
        ).pack(anchor="w", pady=(6, 18))

        cards = ttk.Frame(wrapper, style="Surface.TFrame")
        cards.pack(fill="both", expand=True)

        for column, pet in enumerate(PET_DEFINITIONS.values()):
            card = ttk.Frame(cards, padding=14, style="Card.TFrame")
            card.grid(row=0, column=column, padx=8, sticky="nsew")
            cards.columnconfigure(column, weight=1)
            self._card_frames[pet.pet_id] = card
            self._build_card(card, pet.pet_id)

        footer = ttk.Frame(wrapper, style="Surface.TFrame")
        footer.pack(fill="x", pady=(16, 0))

        ttk.Button(
            footer,
            text="确认选择",
            command=self._confirm,
            style="Primary.TButton",
        ).pack(side="right")

    def _build_card(self, parent: ttk.Frame, pet_id: str) -> None:
        pet = PET_DEFINITIONS[pet_id]

        canvas = tk.Canvas(
            parent,
            width=180,
            height=170,
            bg="#fffdf7",
            highlightthickness=0,
            bd=0,
        )
        canvas.pack(fill="x")
        canvas.create_oval(42, 136, 138, 158, fill="#dde4eb", outline="")
        draw_pet(canvas, pet_id, 90, 88, 0.72, tag=f"preview-{pet_id}")

        title = ttk.Label(parent, text=pet.label, style="CardTitle.TLabel")
        title.pack(anchor="center", pady=(10, 6))

        desc = ttk.Label(
            parent,
            text=pet.description,
            style="CardBody.TLabel",
            wraplength=180,
            justify="center",
        )
        desc.pack(fill="x")

        radio = ttk.Radiobutton(
            parent,
            text="选它",
            value=pet_id,
            variable=self.choice,
            command=self._refresh_highlight,
            style="Card.TRadiobutton",
        )
        radio.pack(pady=(12, 0))

        clickable_widgets = (parent, canvas, title, desc)
        for widget in clickable_widgets:
            widget.bind("<Button-1>", lambda _event, value=pet_id: self._choose(value))
            widget.bind("<Double-Button-1>", lambda _event, value=pet_id: self._quick_confirm(value))

    def _choose(self, pet_id: str) -> None:
        self.choice.set(pet_id)
        self._refresh_highlight()

    def _quick_confirm(self, pet_id: str) -> None:
        self.choice.set(pet_id)
        self._refresh_highlight()
        self._confirm()

    def _refresh_highlight(self) -> None:
        current = self.choice.get()
        for pet_id, frame in self._card_frames.items():
            if pet_id == current:
                frame.configure(style="CardSelected.TFrame")
            else:
                frame.configure(style="Card.TFrame")

    def _confirm(self) -> None:
        self.selected_pet = self.choice.get() or DEFAULT_PET_ID
        self.destroy()

    def _show_dialog(self) -> None:
        width = 760
        height = 420
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        pos_x = max(0, (screen_width - width) // 2)
        pos_y = max(0, (screen_height - height) // 2)

        self.geometry(f"{width}x{height}+{pos_x}+{pos_y}")
        self.deiconify()
        self.lift()
        self.focus_force()
