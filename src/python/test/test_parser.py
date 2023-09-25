from rinha import ast
from rinha.grammar import parser
from rply.token import Token

def test_string():
    tokens = iter([Token('STRING', '"Lorem ipsum"')])

    expr = parser.parse(tokens)
    
    assert isinstance(expr, ast.Str)
    assert expr.value == 'Lorem ipsum'


def test_print_string(capfd):
    tokens = iter([
        Token('PRINT', 'print'),
        Token('OPEN_PARENS', '('),
        Token('STRING', '"Lorem ipsum"'),
        Token('CLOSE_PARENS', ')'),
    ])

    expr = parser.parse(tokens)
    result = expr.eval()

    assert isinstance(result, ast.Str)
    assert result.value == 'Lorem ipsum'

    out, err = capfd.readouterr()
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

    assert isinstance(result, ast.Int)
    assert result.value == 123
    assert out == '123\n'
    assert err == ''

def test_print_boolean_true(capfd):
    tokens = iter([
        Token('PRINT', 'print'),
        Token('OPEN_PARENS', '('),
        Token('TRUE', 'true'),
        Token('CLOSE_PARENS', ')'),
    ])

    expr = parser.parse(tokens)
    result = expr.eval()
    out, err = capfd.readouterr()

    assert isinstance(result, ast.Bool)
    assert result.value == True
    assert out == 'true\n'
    assert err == ''

def test_print_boolean_false(capfd):
    tokens = iter([
        Token('PRINT', 'print'),
        Token('OPEN_PARENS', '('),
        Token('FALSE', 'false'),
        Token('CLOSE_PARENS', ')'),
    ])

    expr = parser.parse(tokens)
    result = expr.eval()
    out, err = capfd.readouterr()

    assert isinstance(result, ast.Bool)
    assert result.value == False
    assert out == 'false\n'
    assert err == ''

def test_sum():
    tokens = iter([
        Token('DIGITS', '123'),
        Token('PLUS', '+'),
        Token('DIGITS', '456'),
    ])

    expr = parser.parse(tokens)
    result = expr.eval()
    
    assert isinstance(expr.left, ast.Int)
    assert isinstance(expr.right, ast.Int)
    assert isinstance(result, ast.Int)
    
    assert expr.left.value == 123
    assert expr.right.value == 456
    assert result.value == 579

def test_print_sum(capfd):
    tokens = iter([
        Token('PRINT', 'print'),
        Token('OPEN_PARENS', '('),
        Token('DIGITS', '123'),
        Token('PLUS', '+'),
        Token('DIGITS', '456'),
        Token('CLOSE_PARENS', ')'),
    ])

    expr = parser.parse(tokens)
    result = expr.eval()
    
    assert isinstance(result, ast.Int)
    assert result.value == 579

    out, err = capfd.readouterr()
    assert out == '579\n'
    assert err == ''
