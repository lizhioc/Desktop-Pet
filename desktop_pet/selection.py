from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Dict, Optional

from .pets import CHARACTER_DEFINITIONS, DEFAULT_CHARACTER_ID, get_character_pose_paths


class CharacterSelectionDialog(tk.Toplevel):
    def __init__(
        self,
        master: tk.Tk,
        initial_character_id: str = DEFAULT_CHARACTER_ID,
        allow_cancel: bool = False,
    ) -> None:
        super().__init__(master)
        initial_value = initial_character_id if initial_character_id in CHARACTER_DEFINITIONS else DEFAULT_CHARACTER_ID
        self.selected_character: Optional[str] = None
        self.choice = tk.StringVar(value=initial_value)
        self.allow_cancel = allow_cancel
        self._card_frames: Dict[str, ttk.Frame] = {}
        self._preview_images: Dict[str, tk.PhotoImage] = {}

        self.title("选择桌宠")
        self.configure(bg="#fff6ea")
        self.resizable(False, False)
        if master.state() != "withdrawn":
            self.transient(master)
        self.grab_set()

        self._build()
        self._refresh_highlight()
        self._show_dialog()

        self.protocol("WM_DELETE_WINDOW", self._cancel if self.allow_cancel else self._confirm)

    def _build(self) -> None:
        wrapper = ttk.Frame(self, padding=20, style="Surface.TFrame")
        wrapper.pack(fill="both", expand=True)

        heading = "第一次启动，先选择一个桌宠形象"
        subtitle = "确认后会记住本次选择，下次打开直接显示对应角色。"
        if self.allow_cancel:
            heading = "重新选择桌宠形象"
            subtitle = "只有点击确认后才会切换；取消会继续保留当前角色。"

        ttk.Label(wrapper, text=heading, style="Title.TLabel").pack(anchor="w")
        ttk.Label(wrapper, text=subtitle, style="Body.TLabel").pack(anchor="w", pady=(6, 18))

        cards = ttk.Frame(wrapper, style="Surface.TFrame")
        cards.pack(fill="both", expand=True)

        for column, character in enumerate(CHARACTER_DEFINITIONS.values()):
            card = ttk.Frame(cards, padding=14, style="Card.TFrame")
            card.grid(row=0, column=column, padx=8, sticky="nsew")
            cards.columnconfigure(column, weight=1)
            self._card_frames[character.character_id] = card
            self._build_card(card, character.character_id)

        footer = ttk.Frame(wrapper, style="Surface.TFrame")
        footer.pack(fill="x", pady=(16, 0))

        if self.allow_cancel:
            ttk.Button(footer, text="取消", command=self._cancel, style="Secondary.TButton").pack(side="right", padx=(0, 10))

        ttk.Button(footer, text="确认选择", command=self._confirm, style="Primary.TButton").pack(side="right")

    def _build_card(self, parent: ttk.Frame, character_id: str) -> None:
        character = CHARACTER_DEFINITIONS[character_id]
        pose_paths = get_character_pose_paths(character_id)

        canvas = tk.Canvas(
            parent,
            width=180,
            height=230,
            bg="#fffdf7",
            highlightthickness=0,
            bd=0,
        )
        canvas.pack(fill="x")
        if pose_paths:
            preview_image = tk.PhotoImage(file=str(pose_paths[0])).subsample(7, 7)
            self._preview_images[character_id] = preview_image
            canvas.create_image(90, 214, image=preview_image, anchor="s")
        else:
            canvas.create_text(
                90,
                112,
                text="未找到图片",
                fill="#7d7065",
                font=("Microsoft YaHei UI", 10, "bold"),
            )

        title = ttk.Label(parent, text=character.label, style="CardTitle.TLabel")
        title.pack(anchor="center", pady=(10, 6))

        desc = ttk.Label(parent, text=character.description, style="CardBody.TLabel", wraplength=180, justify="center")
        desc.pack(fill="x")

        radio = ttk.Radiobutton(
            parent,
            text="选这个",
            value=character_id,
            variable=self.choice,
            command=self._refresh_highlight,
            style="Card.TRadiobutton",
        )
        radio.pack(pady=(12, 0))

        for widget in (parent, canvas, title, desc):
            widget.bind("<Button-1>", lambda _event, value=character_id: self._choose(value))
            widget.bind("<Double-Button-1>", lambda _event, value=character_id: self._quick_confirm(value))

    def _choose(self, character_id: str) -> None:
        self.choice.set(character_id)
        self._refresh_highlight()

    def _quick_confirm(self, character_id: str) -> None:
        self.choice.set(character_id)
        self._refresh_highlight()
        self._confirm()

    def _refresh_highlight(self) -> None:
        current = self.choice.get()
        for character_id, frame in self._card_frames.items():
            frame.configure(style="CardSelected.TFrame" if character_id == current else "Card.TFrame")

    def _confirm(self) -> None:
        self.selected_character = self.choice.get() or DEFAULT_CHARACTER_ID
        self.destroy()

    def _cancel(self) -> None:
        self.selected_character = None
        self.destroy()

    def _show_dialog(self) -> None:
        width = 520
        height = 430
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        pos_x = max(0, (screen_width - width) // 2)
        pos_y = max(0, (screen_height - height) // 2)

        self.geometry(f"{width}x{height}+{pos_x}+{pos_y}")
        self.deiconify()
        self.lift()
        self.focus_force()
