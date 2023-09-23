from rinha.lexer import makeLexer
from pytest import raises


def test_print():
    lexer = makeLexer()
    stream = lexer.lex('print')
    token = stream.next()

    assert token.name == 'PRINT'
    assert token.value == 'print'

def test_whitespaces():
    lexer = makeLexer()
    stream = lexer.lex('   \t  \t   print   \n  \t ')
    token = stream.next()

    assert token.name == 'PRINT'
    assert token.value == 'print'

    with raises(StopIteration):
        stream.next()


def test_end_of_line_comment():
    lexer = makeLexer()
    stream = lexer.lex('print // show text on the screen! \n')
    token = stream.next()

    assert token.name == 'PRINT'
    assert token.value == 'print'

    with raises(StopIteration):
        stream.next()


def test_multiline_comment():
    lexer = makeLexer()
    stream = lexer.lex('print /* show text \n on the screen! */\n')
    token = stream.next()

    assert token.name == 'PRINT'
    assert token.value == 'print'

    with raises(StopIteration):
        stream.next()


def test_print_something():
    lexer = makeLexer()
    stream = lexer.lex('print("hello")')
    token = stream.next()

    assert token.name == 'PRINT'
    assert token.value == 'print'