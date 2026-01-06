
#TESTES AUTOMATIZADOS USANDO O CHAT GPT



import subprocess
import tempfile
import os
import sys


def run_z70(src_code):
    """
    Executa um programa Z70 e retorna o stdout real do emulador.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".z70", mode="w") as f:
        f.write(src_code)
        src_path = f.name

    out_file = tempfile.NamedTemporaryFile(delete=False)
    out_file.close()

    result = subprocess.run(
        [
            sys.executable,
            "Z70.py",
            src_path,
            "00h-FFh",
            out_file.name
        ],
        capture_output=True,
        text=True
    )

    os.remove(src_path)
    os.remove(out_file.name)

    return result.stdout


# =========================================================
# TESTES BÁSICOS DE REGISTRADORES
# =========================================================

def test_add_mov_registers():
    src = """
        mov A, 05H
        mov B, 03H
        add A, B
    """
    out = run_z70(src)
    assert "A=08H" in out


def test_sub_registers():
    src = """
        mov A, 05H
        mov B, 02H
        sub A, B
    """
    out = run_z70(src)
    assert "A=03H" in out


# =========================================================
# TESTES DE FLAGS
# =========================================================

def test_zero_flag():
    src = """
        mov A, 00H
        sub A, 00H
    """
    out = run_z70(src)
    assert "ZF=1" in out


def test_carry_flag():
    src = """
        mov A, 01H
        sub A, 02H
    """
    out = run_z70(src)
    assert "CF=1" in out


def test_overflow_flag():
    src = """
        mov A, 7FH
        add A, 01H
    """
    out = run_z70(src)
    assert "OF=1" in out


# =========================================================
# CONTROLE DE FLUXO
# =========================================================

def test_jump_zero():
    src = """
        mov A, 00H
        sub A, 00H
        jz SKIP
        mov B, FFH
    SKIP:
        nop
    """
    out = run_z70(src)
    assert "B=00H" in out


def test_unconditional_jump():
    src = """
        mov A, 01H
        jmp END
        mov A, FFH
    END:
        nop
    """
    out = run_z70(src)
    assert "A=01H" in out


# =========================================================
# MEMÓRIA
# =========================================================

def test_memory_store_load():
    src = """
        mov I, 10H
        mov A, 05H
        mov [I], A
        mov A, 00H
        mov A, [I]
    """
    out = run_z70(src)
    assert "A=05H" in out


def test_multiple_memory_positions():
    src = """
        mov I, 20H
        mov A, 0AH
        mov [I], A
        inc I
        mov A, 0BH
        mov [I], A
        dec I
        mov A, [I]
    """
    out = run_z70(src)
    assert "A=0AH" in out


# =========================================================
# LOOPS
# =========================================================

def test_loop_countdown():
    src = """
        mov A, 05H
    LOOP:
        dec A
        jz END
        jmp LOOP
    END:
        nop
    """
    out = run_z70(src)
    assert "A=00H" in out


def test_loop_with_counter():
    src = """
        mov A, 03H
        mov B, 00H
    LOOP:
        inc B
        dec A
        jz END
        jmp LOOP
    END:
        nop
    """
    out = run_z70(src)
    assert "B=03H" in out


# =========================================================
# TESTES SURREAIS (EDGE CASES)
# =========================================================

def test_overflow_and_carry_together():
    src = """
        mov A, FFH
        add A, 01H
    """
    out = run_z70(src)
    assert "A=00H" in out
    assert "CF=1" in out
    assert "ZF=1" in out


def test_double_borrow_chain():
    src = """
        mov A, 00H
        sub A, 01H
        sub A, 01H
    """
    out = run_z70(src)
    assert "A=FEH" in out
    assert "CF=1" in out


def test_zero_flag_turns_off():
    src = """
        mov A, 00H
        sub A, 00H
        add A, 01H
    """
    out = run_z70(src)
    assert "ZF=0" in out


def test_self_overwriting_memory():
    src = """
        mov I, 30H
        mov A, 0AH
        mov [I], A
        mov A, [I]
        inc A
        mov [I], A
        mov A, [I]
    """
    out = run_z70(src)
    assert "A=0BH" in out


def test_minimal_loop():
    src = """
        mov A, 01H
    LOOP:
        dec A
        jz END
        jmp LOOP
    END:
        nop
    """
    out = run_z70(src)
    assert "A=00H" in out


def test_jump_inside_jump():
    src = """
        mov A, 00H
        jz FIRST
        mov A, FFH

    FIRST:
        mov B, 01H
        jmp SECOND

    SECOND:
        inc B
        nop
    """
    out = run_z70(src)
    assert "A=00H" in out
    assert "B=02H" in out


def test_memory_edge_address():
    src = """
        mov I, FFH
        mov A, 55H
        mov [I], A
        mov A, 00H
        mov A, [I]
    """
    out = run_z70(src)
    assert "A=55H" in out


def test_register_dual_role():
    src = """
        mov I, 40H
        mov A, 03H
    LOOP:
        mov [I], A
        dec A
        inc I
        jz END
        jmp LOOP
    END:
        dec I
        mov A, [I]
    """
    out = run_z70(src)
    assert "A=01H" in out


def test_flag_change_without_value_change():
    src = """
        mov A, 01H
        add A, 00H
    """
    out = run_z70(src)
    assert "A=01H" in out
    assert "ZF=0" in out


def test_nop_stability():
    src = """
        nop
        nop
        nop
        nop
    """
    out = run_z70(src)
    assert "REGS:" in out
    assert "FLAGS:" in out
