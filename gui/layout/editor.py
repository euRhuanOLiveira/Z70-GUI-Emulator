import tkinter as tk
from gui.theme.colors import (
    BG_PANEL, BG_EDITOR, BG_HIGHLIGHT,
    TEXT_PRIMARY, TEXT_SECONDARY
)
from gui.theme.fonts import FONT_CODE, FONT_TITLE


class CodeEditor(tk.Frame):
    def __init__(self, parent, title: str):
        super().__init__(parent, bg=BG_PANEL)

        # --------- Título ----------
        title_lbl = tk.Label(
            self,
            text=title,
            bg=BG_PANEL,
            fg=TEXT_PRIMARY,
            font=FONT_TITLE
        )
        title_lbl.pack(anchor="w", padx=8, pady=(6, 2))

        # --------- Área principal ----------
        area = tk.Frame(self, bg=BG_PANEL)
        area.pack(fill=tk.BOTH, expand=True, padx=8, pady=6)

        # Numeração de linhas
        self.lines = tk.Text(
            area,
            width=4,
            padx=4,
            bg=BG_PANEL,
            fg=TEXT_SECONDARY,
            font=FONT_CODE,
            state=tk.DISABLED,
            relief=tk.FLAT
        )
        self.lines.pack(side=tk.LEFT, fill=tk.Y)

        # Editor de código
        self.text = tk.Text(
            area,
            bg=BG_EDITOR,
            fg=TEXT_PRIMARY,
            insertbackground=TEXT_PRIMARY,
            font=FONT_CODE,
            undo=True,
            wrap=tk.NONE
        )
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbars
        yscroll = tk.Scrollbar(area, orient=tk.VERTICAL, command=self._on_scroll_y)
        yscroll.pack(side=tk.RIGHT, fill=tk.Y)

        xscroll = tk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.text.xview)
        xscroll.pack(fill=tk.X)

        self.text.config(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)

        # Eventos
        self.text.bind("<KeyRelease>", self._update_lines)
        self.text.bind("<MouseWheel>", self._update_lines)

        # Highlight da linha atual (PC futuramente)
        self.text.tag_configure(
            "current_line",
            background=BG_HIGHLIGHT
        )

        self._update_lines()

    # =========================
    # API PÚBLICA
    # =========================
    def get_code_lines(self):
        return self.text.get("1.0", tk.END).splitlines()

    def set_code(self, code: str):
        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", code)
        self._update_lines()

    def highlight_line(self, line_number: int):
        self.text.tag_remove("current_line", "1.0", tk.END)
        index = f"{line_number}.0"
        self.text.tag_add("current_line", index, f"{line_number}.end")
        self.text.see(index)

    # =========================
    # INTERNOS
    # =========================
    def _update_lines(self, event=None):
        self.lines.config(state=tk.NORMAL)
        self.lines.delete("1.0", tk.END)

        line_count = int(self.text.index("end-1c").split(".")[0])
        for i in range(1, line_count + 1):
            self.lines.insert(tk.END, f"{i}\n")

        self.lines.config(state=tk.DISABLED)

    def _on_scroll_y(self, *args):
        self.text.yview(*args)
        self.lines.yview(*args)
