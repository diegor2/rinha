from rply import LexingError
from rinha.lexical import lexer
from pytest import raises


def test_empty():
    stream = lexer.lex('')

    with raises(StopIteration):
        stream.next()


def test_blank_lines():
    stream = lexer.lex('\n\n\n\n')

    with raises(StopIteration):
        stream.next()


def test_print():
    stream = lexer.lex('print')
    token = stream.next()

    assert token.name == 'PRINT'
    assert token.value == 'print'

    with raises(StopIteration):
        stream.next()


def test_blank_header():
    stream = lexer.lex('\n\n\n\nprint')
    token = stream.next()

    assert token.name == 'PRINT'
    assert token.value == 'print'

    with raises(StopIteration):
        stream.next()


def test_blank_tail():
    stream = lexer.lex('print\n\n\n\n')
    token = stream.next()

    assert token.name == 'PRINT'
    assert token.value == 'print'

    with raises(StopIteration):
        stream.next()


def test_whitespaces():
    stream = lexer.lex('   \t  \t \r  print   \n  \t ')
    token = stream.next()

    assert token.name == 'PRINT'
    assert token.value == 'print'

    with raises(StopIteration):
        stream.next()


def test_single_line_comment():
    stream = lexer.lex('print // show text on the screen! \n')
    token = stream.next()

    assert token.name == 'PRINT'
    assert token.value == 'print'

    with raises(StopIteration):
        stream.next()


def test_continue_after_single_line_comment():
    code = r'''
    print//print
    print
    '''
    
    stream = lexer.lex(code)
    
    token = stream.next()
    assert token.name == 'PRINT'
    assert token.value == 'print'

    token = stream.next()
    assert token.name == 'PRINT'
    assert token.value == 'print'

    with raises(StopIteration):
        stream.next()


def test_multiline_comment():
    code = r'''
    
    print /* 
        show text
    
            on the screen! 

    */

    '''

    stream = lexer.lex(code)
    token = stream.next()

    assert token.name == 'PRINT'
    assert token.value == 'print'

    with raises(StopIteration):
        stream.next()
        


def test_midline_comment():
    stream = lexer.lex('print /* TODO */ print')

    token = stream.next()
    assert token.name == 'PRINT'
    assert token.value == 'print'

    token = stream.next()
    assert token.name == 'PRINT'
    assert token.value == 'print'

    with raises(StopIteration):
        stream.next()


def test_simple_string():
    stream = lexer.lex('"Lorem ipsum dolor sit amet"')
    token = stream.next()

    assert token.name == 'STRING'
    assert token.value == 'Lorem ipsum dolor sit amet'
    

def test_string_symbols():
    stream = lexer.lex('"~hE7L0 // w0rL> */* @@#$ !! 42.00f"')
    token = stream.next()
    assert token.name == 'STRING'
    assert token.value == '~hE7L0 // w0rL> */* @@#$ !! 42.00f'
    
    
def test_multiline_string():
    code = '''
        "Lorem ipsum dolor sit amet, 
         consectetur adipiscing elit, 
         sed do eiusmod tempor incididunt ut labore et dolore magna aliqua"
    '''
    stream = lexer.lex(code)
    with raises(LexingError):
        stream.next()


def test_print_something():
    stream = lexer.lex('print("hello")')
    
    token = stream.next()
    assert token.name == 'PRINT'
    assert token.value == 'print'
    
    token = stream.next()
    assert token.name == 'OPEN_PARENS'
    assert token.value == '('
    
    token = stream.next()
    assert token.name == 'STRING'
    assert token.value == 'hello'
    
    token = stream.next()
    assert token.name == 'CLOSE_PARENS'
    assert token.value == ')'

    with raises(StopIteration):
        stream.next()
    

def test_print_a_lot_of_things():
    stream = lexer.lex('print("~hE7L0 // w0rL> */* @@#$ !! 42.00f")')
    
    token = stream.next()
    assert token.name == 'PRINT'
    assert token.value == 'print'
    
    token = stream.next()
    assert token.name == 'OPEN_PARENS'
    assert token.value == '('
    
    token = stream.next()
    assert token.name == 'STRING'
    assert token.value == '~hE7L0 // w0rL> */* @@#$ !! 42.00f'
    
    token = stream.next()
    assert token.name == 'CLOSE_PARENS'
    assert token.value == ')'

    with raises(StopIteration):
        stream.next()

def test_function_call_with_spaces():
    stream = lexer.lex('  print \n(  \n  "~hE7L0 // w0rL> */* @@#$ !! 42.00f" \n\n)  \n')
    
    token = stream.next()
    assert token.name == 'PRINT'
    assert token.value == 'print'
    
    token = stream.next()
    assert token.name == 'OPEN_PARENS'
    assert token.value == '('
    
    token = stream.next()
    assert token.name == 'STRING'
    assert token.value == '~hE7L0 // w0rL> */* @@#$ !! 42.00f'
    
    token = stream.next()
    assert token.name == 'CLOSE_PARENS'
    assert token.value == ')'

    with raises(StopIteration):
        stream.next()