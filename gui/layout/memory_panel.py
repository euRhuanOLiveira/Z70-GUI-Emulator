import tkinter as tk
from gui.theme.colors import BG_PANEL, BG_EDITOR, TEXT_PRIMARY, TEXT_SECONDARY, BG_HIGHLIGHT
from gui.theme.fonts import FONT_CODE, FONT_TITLE
from gui.i18n.pt import STRINGS

CELL_WIDTH = 3
ADDR_WIDTH = 4


class MemoryPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_PANEL)

        title = tk.Label(
            self,
            text=STRINGS["memory_title"],
            bg=BG_PANEL,
            fg=TEXT_PRIMARY,
            font=FONT_TITLE
        )
        title.pack(anchor="w", padx=8, pady=(6, 4))

        grid = tk.Frame(self, bg=BG_PANEL)
        grid.pack(padx=8, pady=6)

        self.cells = {}

        tk.Label(grid, text="", width=ADDR_WIDTH, bg=BG_PANEL).grid(row=0, column=0)

        for col in range(16):
            tk.Label(
                grid,
                text=f"{col:X}",
                width=CELL_WIDTH,
                anchor="center",
                bg=BG_PANEL,
                fg=TEXT_SECONDARY,
                font=FONT_CODE
            ).grid(row=0, column=col + 1)

        for row in range(16):
            tk.Label(
                grid,
                text=f"{row:X}0",
                width=ADDR_WIDTH,
                anchor="w",
                bg=BG_PANEL,
                fg=TEXT_SECONDARY,
                font=FONT_CODE
            ).grid(row=row + 1, column=0)

            for col in range(16):
                addr = row * 16 + col
                lbl = tk.Label(
                    grid,
                    text="00",
                    width=CELL_WIDTH,
                    anchor="center",
                    bg=BG_EDITOR,
                    fg=TEXT_PRIMARY,
                    font=FONT_CODE,
                    relief=tk.FLAT,
                    borderwidth=1
                )
                lbl.grid(row=row + 1, column=col + 1, padx=1, pady=1)
                self.cells[addr] = lbl

    def update(self, cpu):
        if not cpu:
            self.clear()
            return

        for addr, lbl in self.cells.items():
            lbl.config(text=f"{cpu.mem[addr]:02X}", bg=BG_EDITOR)

    def highlight(self, addr):
        if addr in self.cells:
            self.cells[addr].config(bg=BG_HIGHLIGHT)

    def clear(self):
        for lbl in self.cells.values():
            lbl.config(text="00", bg=BG_EDITOR)
