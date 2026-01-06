import tkinter as tk
from tkinter import ttk

from gui.theme.colors import (
    BG_PANEL, TEXT_PRIMARY, ACCENT
)
from gui.theme.fonts import FONT_NORMAL


class Toolbar(tk.Frame):
    def __init__(self, parent, strings, on_run, on_step, on_reset):
        super().__init__(parent, bg=BG_PANEL)

        self.strings = strings

        # Botão RUN
        self.run_btn = tk.Button(
            self,
            text="▶ " + strings["run"],
            command=on_run,
            bg=ACCENT,
            fg="black",
            font=FONT_NORMAL,
            relief=tk.FLAT,
            padx=12,
            pady=6
        )
        self.run_btn.pack(side=tk.LEFT, padx=6, pady=6)

        # Botão STEP
        self.step_btn = tk.Button(
            self,
            text="⏸ " + strings["step"],
            command=on_step,
            bg=BG_PANEL,
            fg=TEXT_PRIMARY,
            font=FONT_NORMAL,
            relief=tk.FLAT,
            padx=12,
            pady=6
        )
        self.step_btn.pack(side=tk.LEFT, padx=6)

        # Botão RESET
        self.reset_btn = tk.Button(
            self,
            text="⟳ " + strings["reset"],
            command=on_reset,
            bg=BG_PANEL,
            fg=TEXT_PRIMARY,
            font=FONT_NORMAL,
            relief=tk.FLAT,
            padx=12,
            pady=6
        )
        self.reset_btn.pack(side=tk.LEFT, padx=6)

    def set_running(self, running: bool):
        """
        Atualiza visualmente quando o programa está rodando.
        """
        if running:
            self.run_btn.config(state=tk.DISABLED)
        else:
            self.run_btn.config(state=tk.NORMAL)
