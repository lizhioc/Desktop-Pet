from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable


class SettingsPanel(tk.Toplevel):
    def __init__(
        self,
        master: tk.Tk,
        current_pet_text: str,
        startup_mode_text: str,
        on_reselect: Callable[[], None],
        on_restore_default: Callable[[], None],
        on_clear_startup_choice: Callable[[], None],
        on_remember_current_pet: Callable[[], None],
    ) -> None:
        super().__init__(master)
        self._current_pet_var = tk.StringVar(value=current_pet_text)
        self._startup_mode_var = tk.StringVar(value=startup_mode_text)
        self._remember_enabled = True
        self._clear_enabled = True

        self._on_reselect = on_reselect
        self._on_restore_default = on_restore_default
        self._on_clear_startup_choice = on_clear_startup_choice
        self._on_remember_current_pet = on_remember_current_pet

        self.title("宠物设置")
        self.configure(bg="#fff6ea")
        self.resizable(False, False)
        self.transient(master)

        self._build()
        self._show_dialog()

        self.protocol("WM_DELETE_WINDOW", self.close)

    def _build(self) -> None:
        wrapper = ttk.Frame(self, padding=20, style="Surface.TFrame")
        wrapper.pack(fill="both", expand=True)

        ttk.Label(
            wrapper,
            text="宠物设置",
            style="Title.TLabel",
        ).pack(anchor="w")
        ttk.Label(
            wrapper,
            text="在这里切换宠物、恢复默认，或者决定下次启动是否直接沿用当前选择。",
            style="Body.TLabel",
            wraplength=340,
        ).pack(anchor="w", pady=(6, 18))

        info_card = ttk.Frame(wrapper, padding=14, style="Card.TFrame")
        info_card.pack(fill="x")

        ttk.Label(info_card, text="当前宠物", style="PanelLabel.TLabel").pack(anchor="w")
        ttk.Label(info_card, textvariable=self._current_pet_var, style="PanelValue.TLabel").pack(anchor="w", pady=(4, 12))
        ttk.Label(info_card, text="启动方式", style="PanelLabel.TLabel").pack(anchor="w")
        ttk.Label(info_card, textvariable=self._startup_mode_var, style="PanelHint.TLabel", wraplength=320).pack(anchor="w", pady=(4, 0))

        actions = ttk.Frame(wrapper, style="Surface.TFrame")
        actions.pack(fill="x", pady=(16, 0))

        ttk.Button(
            actions,
            text="重新选择宠物",
            command=self._on_reselect,
            style="Secondary.TButton",
        ).pack(fill="x")

        ttk.Button(
            actions,
            text="恢复默认宠物",
            command=self._on_restore_default,
            style="Secondary.TButton",
        ).pack(fill="x", pady=(10, 0))

        self._remember_button = ttk.Button(
            actions,
            text="记住当前宠物",
            command=self._on_remember_current_pet,
            style="Secondary.TButton",
        )
        self._remember_button.pack(fill="x", pady=(10, 0))

        self._clear_button = ttk.Button(
            actions,
            text="下次启动重新选择",
            command=self._on_clear_startup_choice,
            style="Danger.TButton",
        )
        self._clear_button.pack(fill="x", pady=(10, 0))

        ttk.Button(
            wrapper,
            text="关闭",
            command=self.close,
            style="Primary.TButton",
        ).pack(anchor="e", pady=(18, 0))

    def update_state(
        self,
        current_pet_text: str,
        startup_mode_text: str,
        remember_enabled: bool,
        clear_enabled: bool,
    ) -> None:
        self._current_pet_var.set(current_pet_text)
        self._startup_mode_var.set(startup_mode_text)
        self._remember_enabled = remember_enabled
        self._clear_enabled = clear_enabled
        self._remember_button.state(["!disabled"] if remember_enabled else ["disabled"])
        self._clear_button.state(["!disabled"] if clear_enabled else ["disabled"])

    def focus_panel(self) -> None:
        self.deiconify()
        self.lift()
        self.focus_force()

    def close(self) -> None:
        self.destroy()

    def _show_dialog(self) -> None:
        width = 390
        height = 390
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        pos_x = max(0, (screen_width - width) // 2 + 120)
        pos_y = max(0, (screen_height - height) // 2 - 40)

        self.geometry(f"{width}x{height}+{pos_x}+{pos_y}")
        self.deiconify()
        self.lift()
        self.focus_force()
