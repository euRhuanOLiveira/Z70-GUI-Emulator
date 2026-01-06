import tkinter as tk
from gui.theme.colors import BG_PANEL, TEXT_PRIMARY
from gui.theme.fonts import FONT_CODE
from gui.i18n.pt import STRINGS


class AsciiPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_PANEL)

        title = tk.Label(
            self,
            text=STRINGS["ascii_title"],
            bg=BG_PANEL,
            fg=TEXT_PRIMARY,
            font=("Segoe UI", 10, "bold")
        )
        title.pack(anchor="w", padx=8, pady=(6, 4))

        self.text = tk.Text(
            self,
            height=4,
            bg="#0f0f0f",
            fg="#d0ffd0",
            font=FONT_CODE,
            wrap=tk.NONE
        )
        self.text.pack(fill=tk.X, padx=8, pady=(0, 6))
        self.text.config(state=tk.DISABLED)

    def update(self, cpu, start=0x80, end=0xFF):
        if not cpu:
            self.clear()
            return

        chars = []
        for i in range(start, end + 1):
            b = cpu.mem[i]
            chars.append(chr(b) if 32 <= b <= 126 else ".")

        self.text.config(state=tk.NORMAL)
        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", "".join(chars))
        self.text.config(state=tk.DISABLED)

    def clear(self):
        self.text.config(state=tk.NORMAL)
        self.text.delete("1.0", tk.END)
        self.text.config(state=tk.DISABLED)
