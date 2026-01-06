import tkinter as tk

from gui.theme.colors import (
    BG_PANEL, TEXT_PRIMARY, TEXT_SECONDARY,
    SUCCESS, WARNING, ERROR
)
from gui.theme.fonts import FONT_NORMAL, FONT_TITLE
from gui.i18n.pt import STRINGS


class CPUPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_PANEL)

        # ---------- Título ----------
        title = tk.Label(
            self,
            text=STRINGS["cpu_title"],
            bg=BG_PANEL,
            fg=TEXT_PRIMARY,
            font=FONT_TITLE
        )
        title.pack(anchor="w", padx=8, pady=(6, 4))

        # ---------- Registradores ----------
        self.reg_labels = {}

        regs_frame = tk.Frame(self, bg=BG_PANEL)
        regs_frame.pack(fill=tk.X, padx=8)

        for reg in ["A", "B", "I", "PC"]:
            row = tk.Frame(regs_frame, bg=BG_PANEL)
            row.pack(fill=tk.X, pady=2)

            name = tk.Label(
                row,
                text=f"{reg}:",
                width=4,
                anchor="w",
                bg=BG_PANEL,
                fg=TEXT_PRIMARY,
                font=FONT_NORMAL
            )
            name.pack(side=tk.LEFT)

            val = tk.Label(
                row,
                text="00H",
                anchor="w",
                bg=BG_PANEL,
                fg=TEXT_SECONDARY,
                font=FONT_NORMAL
            )
            val.pack(side=tk.LEFT)

            self.reg_labels[reg] = val

        # ---------- Flags ----------
        flags_title = tk.Label(
            self,
            text=STRINGS["flags_title"],
            bg=BG_PANEL,
            fg=TEXT_PRIMARY,
            font=FONT_TITLE
        )
        flags_title.pack(anchor="w", padx=8, pady=(10, 4))

        self.flag_labels = {}

        for flag in ["ZF", "CF", "OF", "PF", "SF"]:
            row = tk.Frame(self, bg=BG_PANEL)
            row.pack(fill=tk.X, padx=8, pady=2)

            name = tk.Label(
                row,
                text=f"{flag}:",
                width=4,
                anchor="w",
                bg=BG_PANEL,
                fg=TEXT_PRIMARY,
                font=FONT_NORMAL
            )
            name.pack(side=tk.LEFT)

            val = tk.Label(
                row,
                text="0",
                width=2,
                anchor="w",
                bg=BG_PANEL,
                fg=TEXT_SECONDARY,
                font=FONT_NORMAL
            )
            val.pack(side=tk.LEFT)

            desc = tk.Label(
                row,
                text=STRINGS[f"flag_{flag}"],
                bg=BG_PANEL,
                fg=TEXT_SECONDARY,
                font=("Segoe UI", 9)
            )
            desc.pack(side=tk.LEFT, padx=6)

            self.flag_labels[flag] = val

    # =========================
    # API PÚBLICA
    # =========================
    def update(self, cpu):
        if not cpu:
            return

        # Registradores
        self.reg_labels["A"].config(text=f"{cpu.A:02X}H")
        self.reg_labels["B"].config(text=f"{cpu.B:02X}H")
        self.reg_labels["I"].config(text=f"{cpu.I:02X}H")
        self.reg_labels["PC"].config(text=f"{cpu.PC:02X}H")

        # Flags
        for flag, lbl in self.flag_labels.items():
            value = cpu.get_flag(flag)
            lbl.config(text=str(value))

            if value:
                lbl.config(fg=SUCCESS)
            else:
                lbl.config(fg=TEXT_SECONDARY)
