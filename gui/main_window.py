import tkinter as tk
from tkinter import messagebox

# -------- Core Z70 --------
from core.assembler import preprocess, first_pass, second_pass
from core.CPU import CPU

# -------- GUI Components --------
from gui.layout.toolbar import Toolbar
from gui.layout.editor import CodeEditor
from gui.layout.cpu_panel import CPUPanel
from gui.layout.memory_panel import MemoryPanel
from gui.layout.ascii_panel import AsciiPanel
from gui.layout.explanation import ExplanationPanel

from gui.theme.colors import BG_MAIN
from gui.i18n.pt import STRINGS as STRINGS_PT


class Z70App(tk.Tk):
    def __init__(self):
        super().__init__()

        # ---------- Estado ----------
        self.strings = STRINGS_PT
        self.cpu = None
        self.program_loaded = False
        self.listing = []

        # 🔒 Garante espaço total suficiente
        self.geometry("1600x900")
        self.minsize(1600, 900)
        self.title(self.strings["app_title"])
        self.configure(bg=BG_MAIN)

        # ---------- Toolbar ----------
        self.toolbar = Toolbar(
            self,
            strings=self.strings,
            on_run=self.run_program,
            on_step=self.step_program,
            on_reset=self.reset_program
        )
        self.toolbar.pack(fill=tk.X)

        # ======================================================
        # ÁREA PRINCIPAL (EDITOR | CPU | MEMÓRIA)
        # ======================================================
        main_pane = tk.PanedWindow(
            self,
            orient=tk.HORIZONTAL,
            bg=BG_MAIN,
            sashwidth=6
        )
        main_pane.pack(fill=tk.BOTH, expand=True)

        # ---------------- EDITOR ----------------
        editor_frame = tk.Frame(main_pane, bg=BG_MAIN)
        self.editor = CodeEditor(editor_frame, title=self.strings["editor_title"])
        self.editor.pack(fill=tk.BOTH, expand=True)

        self.editor.set_code(
            "mov A, 05H\nmov B, 03H\nadd A, B"
        )
        self.editor.text.bind("<Key>", self._on_code_changed)

        main_pane.add(
            editor_frame,
            stretch="always",
            minsize=420   # 🔒 não deixa o editor esmagar o resto
        )

        # ---------------- CPU ----------------
        cpu_frame = tk.Frame(main_pane, bg=BG_MAIN, width=240)
        cpu_frame.pack_propagate(False)

        self.cpu_panel = CPUPanel(cpu_frame)
        self.cpu_panel.pack(fill=tk.X, padx=6, pady=6)

        main_pane.add(cpu_frame, minsize=240)

        # ---------------- MEMÓRIA ----------------
        mem_frame = tk.Frame(main_pane, bg=BG_MAIN)

        self.memory_panel = MemoryPanel(mem_frame)
        self.memory_panel.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        # 🔒 largura mínima suficiente para 16 colunas (0–F)
        main_pane.add(
            mem_frame,
            stretch="always",
            minsize=760
        )

        # ======================================================
        # ÁREA INFERIOR (ASCII | EXPLICAÇÃO)
        # ======================================================
        bottom_pane = tk.PanedWindow(
            self,
            orient=tk.HORIZONTAL,
            bg=BG_MAIN,
            sashwidth=6,
            height=120
        )
        bottom_pane.pack(fill=tk.X)
        bottom_pane.pack_propagate(False)

        # ---------------- ASCII ----------------
        ascii_frame = tk.Frame(bottom_pane, bg=BG_MAIN)
        self.ascii_panel = AsciiPanel(ascii_frame)
        self.ascii_panel.pack(fill=tk.BOTH, expand=True, padx=6, pady=4)

        bottom_pane.add(ascii_frame, stretch="always")

        # ---------------- EXPLICAÇÃO ----------------
        explanation_frame = tk.Frame(bottom_pane, bg=BG_MAIN)
        self.explanation_panel = ExplanationPanel(explanation_frame)
        self.explanation_panel.pack(fill=tk.BOTH, expand=True, padx=6, pady=4)

        bottom_pane.add(explanation_frame, stretch="always")

        # ======================================================
        # LOG
        # ======================================================
        self.output = tk.Text(
            self,
            height=3,
            bg="#111",
            fg="#0f0",
            font=("Consolas", 10),
        )
        self.output.pack(fill=tk.X)

    # =========================
    # PIPELINE
    # =========================
    def load_program(self):
        try:
            lines = self.editor.get_code_lines()

            pp = preprocess(lines)
            parsed, labels = first_pass(pp)
            mem, listing, code_end = second_pass(parsed, labels)

            self.listing = listing
            self.cpu = CPU(mem, labels)
            self.cpu.program_end = code_end
            self.program_loaded = True

            self.log(self.strings["program_loaded"])
            self.update_output()

        except Exception as e:
            messagebox.showerror("Assembler error", str(e))
            self.program_loaded = False

    # =========================
    # EXECUÇÃO / STEP / RESET
    # =========================
    def run_program(self):
        if not self.program_loaded:
            self.load_program()
        if not self.cpu:
            return

        self.cpu.run()
        self.update_output()
        self.highlight_pc_end()
        self.explain_last_instruction()

        messagebox.showinfo(
            self.strings["app_title"],
            self.strings["program_finished"]
        )

    def step_program(self):
        if not self.program_loaded:
            self.load_program()
        if not self.cpu:
            return

        self.highlight_pc()
        cont = self.cpu.step()

        self.update_output()
        self.explain_last_instruction()

        # ⛔ NÃO mostra popup no STEP
        # Apenas para a execução silenciosamente

    def reset_program(self):
        self.cpu = None
        self.program_loaded = False
        self.listing = []

        self.output.delete("1.0", tk.END)
        self.cpu_panel.update(None)
        self.memory_panel.clear()
        self.ascii_panel.clear()
        self.editor.highlight_line(0)
        self.explanation_panel.clear()

    # =========================
    # HELPERS
    # =========================
    def _on_code_changed(self, event=None):
        self.program_loaded = False

    def log(self, txt):
        self.output.insert(tk.END, txt + "\n")
        self.output.see(tk.END)

    def update_output(self):
        if not self.cpu:
            return

        self.output.delete("1.0", tk.END)
        self.log(f"REGS:  {self.cpu.regs()}")
        self.log(f"FLAGS: {self.cpu.flags()}")

        self.cpu_panel.update(self.cpu)
        self.memory_panel.update(self.cpu)
        self.ascii_panel.update(self.cpu)

    # =========================
    # HIGHLIGHT / EXPLICAÇÃO
    # =========================
    def highlight_pc(self):
        if not self.cpu or not self.listing:
            return

        pc = self.cpu.PC
        for idx, (addr, _, _) in enumerate(self.listing, start=1):
            if addr == pc:
                self.editor.highlight_line(idx)
                break

        self.memory_panel.highlight(pc)

    def highlight_pc_end(self):
        if not self.cpu or not self.listing:
            return

        last_pc = self.cpu.PC - 1
        for idx, (addr, _, _) in enumerate(self.listing, start=1):
            if addr == last_pc:
                self.editor.highlight_line(idx)
                break

    def explain_last_instruction(self):
        if not self.cpu or not self.listing:
            return

        last_pc = self.cpu.PC - 1
        for addr, _, src in self.listing:
            if addr == last_pc:
                instr = src.strip()
                break
        else:
            return

        lines = [f"Instrução executada: {instr}"]
        low = instr.lower()

        if low.startswith("add"):
            lines += [
                "Operação: soma",
                f"Carry: {'sim' if self.cpu.get_flag('CF') else 'não'}",
                f"Zero: {'sim' if self.cpu.get_flag('ZF') else 'não'}",
                f"Overflow: {'sim' if self.cpu.get_flag('OF') else 'não'}",
            ]

        elif low.startswith("sub"):
            lines += [
                "Operação: subtração",
                f"Borrow: {'sim' if self.cpu.get_flag('CF') else 'não'}",
                f"Zero: {'sim' if self.cpu.get_flag('ZF') else 'não'}",
            ]

        elif low.startswith("mov"):
            lines.append("Operação: cópia de valor")

        elif low.startswith("jmp"):
            lines.append("Operação: salto incondicional")

        elif low.startswith("jz"):
            lines.append(
                "Salto executado"
                if self.cpu.get_flag("ZF")
                else "Salto não executado"
            )

        self.explanation_panel.set_text("\n".join(lines))
