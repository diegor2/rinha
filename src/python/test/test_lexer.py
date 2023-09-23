from rply import LexingError
from rinha.lexer import makeLexer
from pytest import raises


def test_empty():
    lexer = makeLexer()
    stream = lexer.lex('')

    with raises(StopIteration):
        stream.next()


def test_blank_lines():
    lexer = makeLexer()
    stream = lexer.lex('\n\n\n\n')

    with raises(StopIteration):
        stream.next()


def test_print():
    lexer = makeLexer()
    stream = lexer.lex('print')
    token = stream.next()

    assert token.name == 'PRINT'
    assert token.value == 'print'

    with raises(StopIteration):
        stream.next()


def test_blank_header():
    lexer = makeLexer()
    stream = lexer.lex('\n\n\n\nprint')
    token = stream.next()

    assert token.name == 'PRINT'
    assert token.value == 'print'

    with raises(StopIteration):
        stream.next()


def test_blank_tail():
    lexer = makeLexer()
    stream = lexer.lex('print\n\n\n\n')
    token = stream.next()

    assert token.name == 'PRINT'
    assert token.value == 'print'

    with raises(StopIteration):
        stream.next()


def test_whitespaces():
    lexer = makeLexer()
    stream = lexer.lex('   \t  \t \r  print   \n  \t ')
    token = stream.next()

    assert token.name == 'PRINT'
    assert token.value == 'print'

    with raises(StopIteration):
        stream.next()


def test_single_line_comment():
    lexer = makeLexer()
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
    
    lexer = makeLexer()
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

    lexer = makeLexer()
    stream = lexer.lex(code)
    token = stream.next()

    assert token.name == 'PRINT'
    assert token.value == 'print'

    with raises(StopIteration):
        stream.next()
        


def test_midline_comment():
    lexer = makeLexer()
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
    lexer = makeLexer()
    stream = lexer.lex('"Lorem ipsum dolor sit amet"')
    
    token = stream.next()
    assert token.name == 'QUOTE'
    assert token.value == '"'
    
    token = stream.next()
    assert token.name == 'STRING'
    assert token.value == 'Lorem ipsum dolor sit amet'
    
    token = stream.next()
    assert token.name == 'QUOTE'
    assert token.value == '"'
    

def test_string_symbols():
    lexer = makeLexer()
    stream = lexer.lex('"~hE7L0 // w0rL> */* @@#$ !! 42.00f"')
    
    token = stream.next()
    assert token.name == 'QUOTE'
    assert token.value == '"'
    
    token = stream.next()
    assert token.name == 'STRING'
    assert token.value == '~hE7L0 // w0rL> */* @@#$ !! 42.00f'
    
    token = stream.next()
    assert token.name == 'QUOTE'
    assert token.value == '"'
    
    
def test_multiline_string():
    code = '''
        "Lorem ipsum dolor sit amet, 
         consectetur adipiscing elit, 
         sed do eiusmod tempor incididunt ut labore et dolore magna aliqua"
    '''

    lexer = makeLexer()
    stream = lexer.lex(code)
    token = stream.next()

    assert token.name == 'QUOTE'
    assert token.value == '"'

    with raises(LexingError):
        stream.next()


def test_print_something():
    lexer = makeLexer()
    stream = lexer.lex('print("hello")')
    
    token = stream.next()
    assert token.name == 'PRINT'
    assert token.value == 'print'
    
    token = stream.next()
    assert token.name == 'LEFT_PARENTESIS'
    assert token.value == '('
    
    token = stream.next()
    assert token.name == 'QUOTE'
    assert token.value == '"'
    
    token = stream.next()
    assert token.name == 'STRING'
    assert token.value == 'hello'
    
    token = stream.next()
    assert token.name == 'QUOTE'
    assert token.value == '"'
    
    token = stream.next()
    assert token.name == 'RIGHT_PARENTESIS'
    assert token.value == ')'

    with raises(StopIteration):
        stream.next()
    

def test_print_a_lot_of_things():
    lexer = makeLexer()
    stream = lexer.lex('print("~hE7L0 // w0rL> */* @@#$ !! 42.00f")')
    
    token = stream.next()
    assert token.name == 'PRINT'
    assert token.value == 'print'
    
    token = stream.next()
    assert token.name == 'LEFT_PARENTESIS'
    assert token.value == '('
    
    token = stream.next()
    assert token.name == 'QUOTE'
    assert token.value == '"'
    
    token = stream.next()
    assert token.name == 'STRING'
    assert token.value == '~hE7L0 // w0rL> */* @@#$ !! 42.00f'
    
    token = stream.next()
    assert token.name == 'QUOTE'
    assert token.value == '"'
    
    token = stream.next()
    assert token.name == 'RIGHT_PARENTESIS'
    assert token.value == ')'

    with raises(StopIteration):
        stream.next()

def test_function_call_with_spaces():
    lexer = makeLexer()
    stream = lexer.lex('  print \n(  \n  "~hE7L0 // w0rL> */* @@#$ !! 42.00f" \n\n)  \n')
    
    token = stream.next()
    assert token.name == 'PRINT'
    assert token.value == 'print'
    
    token = stream.next()
    assert token.name == 'LEFT_PARENTESIS'
    assert token.value == '('
    
    token = stream.next()
    assert token.name == 'QUOTE'
    assert token.value == '"'
    
    token = stream.next()
    assert token.name == 'STRING'
    assert token.value == '~hE7L0 // w0rL> */* @@#$ !! 42.00f'
    
    token = stream.next()
    assert token.name == 'QUOTE'
    assert token.value == '"'
    
    token = stream.next()
    assert token.name == 'RIGHT_PARENTESIS'
    assert token.value == ')'

    with raises(StopIteration):
        stream.next()