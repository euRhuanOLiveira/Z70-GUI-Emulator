import tkinter as tk

from gui.theme.colors import BG_PANEL, TEXT_PRIMARY, TEXT_SECONDARY
from gui.theme.fonts import FONT_NORMAL, FONT_TITLE
from gui.i18n.pt import STRINGS


class ExplanationPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_PANEL)

        title = tk.Label(
            self,
            text=STRINGS["explanation_title"],
            bg=BG_PANEL,
            fg=TEXT_PRIMARY,
            font=FONT_TITLE
        )
        title.pack(anchor="w", padx=8, pady=(6, 4))

        self.text = tk.Text(
            self,
            height=6,
            bg=BG_PANEL,
            fg=TEXT_SECONDARY,
            font=FONT_NORMAL,
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.text.pack(fill=tk.BOTH, expand=True, padx=8, pady=6)

    def set_text(self, text: str):
        self.text.config(state=tk.NORMAL)
        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", text)
        self.text.config(state=tk.DISABLED)

    def clear(self):
        self.set_text("")
