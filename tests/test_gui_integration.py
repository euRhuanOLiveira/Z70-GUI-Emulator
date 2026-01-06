import pytest
from gui.main_window import Z70App


@pytest.fixture
def app():
    app = Z70App()
    app.withdraw()  # NÃO abre janela
    yield app
    app.destroy()


def test_gui_load_program(app):
    app.editor.set_code("""
        mov A, 05H
        mov B, 03H
        add A, B
    """)
    app.load_program()
    assert app.cpu is not None
    assert app.program_loaded is True


def test_gui_step_does_not_crash(app):
    app.editor.set_code("""
        mov A, 01H
        inc A
    """)
    app.load_program()
    app.step_program()
    assert app.cpu is not None


def test_gui_run_does_not_crash(app):
    app.editor.set_code("""
        mov A, 01H
        inc A
        inc A
    """)
    app.load_program()
    app.run_program()
    assert app.cpu is not None


def test_gui_reset(app):
    app.editor.set_code("mov A, 01H")
    app.load_program()
    app.reset_program()
    assert app.cpu is None
    assert app.program_loaded is False


def test_editing_code_invalidates_program(app):
    app.editor.set_code("mov A, 01H")
    app.load_program()
    app.editor.set_code("mov A, 02H")
    assert app.program_loaded is False
