from rinha import ast
from rinha.parsing import parser
from rply.token import Token

def test_string():
    tokens = iter([Token('STRING', 'Lorem ipsum')])

    expr = parser.parse(tokens)
    result = expr.eval()
    
    assert isinstance(expr, ast.Str)
    assert result == 'Lorem ipsum'


def test_print_string(capfd):
    tokens = iter([
        Token('PRINT', 'print'),
        Token('OPEN_PARENS', '('),
        Token('STRING', 'Lorem ipsum'),
        Token('CLOSE_PARENS', ')'),
    ])

    expr = parser.parse(tokens)
    result = expr.eval()
    out, err = capfd.readouterr()

    assert isinstance(expr, ast.Print)
    assert isinstance(expr.expr, ast.Str)
    assert result == 'Lorem ipsum'
    assert out == 'Lorem ipsum\n'
    assert err == ''


def test_print_number(capfd):
    tokens = iter([
        Token('PRINT', 'print'),
        Token('OPEN_PARENS', '('),
        Token('DIGITS', '123'),
        Token('CLOSE_PARENS', ')'),
    ])

    expr = parser.parse(tokens)
    result = expr.eval()
    out, err = capfd.readouterr()

    assert isinstance(expr, ast.Print)
    assert isinstance(expr.expr, ast.Int)
    assert result == 123
    assert out == '123\n'
    assert err == ''
