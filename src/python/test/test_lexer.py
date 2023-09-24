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
    assert token.value == '"Lorem ipsum dolor sit amet"'

    with raises(StopIteration):
        stream.next()


def test_string_symbols():
    stream = lexer.lex('"~hE7L0 // w0rL> */* @@#$ !! 42.00f"')
    token = stream.next()
    assert token.name == 'STRING'
    assert token.value == '"~hE7L0 // w0rL> */* @@#$ !! 42.00f"'


def test_escaped_string():
    stream = lexer.lex(r'"Lorem \"ipsum\" \"dolor \n sit\" \\ amet"')
    token = stream.next()

    assert token.name == 'STRING'
    assert token.value == r'"Lorem \"ipsum\" \"dolor \n sit\" \\ amet"'

    with raises(StopIteration):
        stream.next()


def test_empty_string():
    stream = lexer.lex('""')
    token = stream.next()

    assert token.name == 'STRING'
    assert token.value == '""'

    with raises(StopIteration):
        stream.next()


def test_string_missing_closing_quote():
    stream = lexer.lex('"Lorem ipsum dolor sit amet')

    with raises(LexingError):
        stream.next()


def test_multiline_string():
    code = '''
        "Lorem ipsum dolor sit amet,
         consectetur adipiscing elit"
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
    assert token.value == '"hello"'

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
    assert token.value == '"~hE7L0 // w0rL> */* @@#$ !! 42.00f"'

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
    assert token.value == '"~hE7L0 // w0rL> */* @@#$ !! 42.00f"'

    token = stream.next()
    assert token.name == 'CLOSE_PARENS'
    assert token.value == ')'

    with raises(StopIteration):
        stream.next()

def test_reserved_words():
    stream = lexer.lex('external true false print first second let if else fn')

    token = stream.next()
    assert token.name == 'EXTERNAL'
    assert token.value == 'external'

    token = stream.next()
    assert token.name == 'TRUE'
    assert token.value == 'true'

    token = stream.next()
    assert token.name == 'FALSE'
    assert token.value == 'false'

    token = stream.next()
    assert token.name == 'PRINT'
    assert token.value == 'print'

    token = stream.next()
    assert token.name == 'FIRST'
    assert token.value == 'first'

    token = stream.next()
    assert token.name == 'SECOND'
    assert token.value == 'second'

    token = stream.next()
    assert token.name == 'LET'
    assert token.value == 'let'

    token = stream.next()
    assert token.name == 'IF'
    assert token.value == 'if'

    token = stream.next()
    assert token.name == 'ELSE'
    assert token.value == 'else'

    token = stream.next()
    assert token.name == 'FN'
    assert token.value == 'fn'

    with raises(StopIteration):
        stream.next()

def test_operators():
    stream = lexer.lex('&&||==!=<=>=<> =>(){}+-*/%,;=')

    token = stream.next()
    assert token.name == 'AND'
    assert token.value == '&&'

    token = stream.next()
    assert token.name == 'OR'
    assert token.value == '||'

    token = stream.next()
    assert token.name == 'EQ'
    assert token.value == '=='

    token = stream.next()
    assert token.name == 'NEQ'
    assert token.value == '!='

    token = stream.next()
    assert token.name == 'LTEQ'
    assert token.value == '<='

    token = stream.next()
    assert token.name == 'GTEQ'
    assert token.value == '>='

    token = stream.next()
    assert token.name == 'LT'
    assert token.value == '<'

    token = stream.next()
    assert token.name == 'GT'
    assert token.value == '>'

    token = stream.next()
    assert token.name == 'FN_ARROW'
    assert token.value == '=>'
    
    token = stream.next()
    assert token.name == 'OPEN_PARENS'
    assert token.value == '('

    token = stream.next()
    assert token.name == 'CLOSE_PARENS'
    assert token.value == ')'

    token = stream.next()
    assert token.name == 'OPEN_BRACES'
    assert token.value == '{'

    token = stream.next()
    assert token.name == 'CLOSE_BRACES'
    assert token.value == '}'

    token = stream.next()
    assert token.name == 'PLUS'
    assert token.value == '+'

    token = stream.next()
    assert token.name == 'MINUS'
    assert token.value == '-'

    token = stream.next()
    assert token.name == 'STAR'
    assert token.value == '*'

    token = stream.next()
    assert token.name == 'SLASH'
    assert token.value == '/'

    token = stream.next()
    assert token.name == 'PERCENT'
    assert token.value == '%'

    token = stream.next()
    assert token.name == 'COMMA'
    assert token.value == ','

    token = stream.next()
    assert token.name == 'SEMI_COLON'
    assert token.value == ';'

    token = stream.next()
    assert token.name == 'ASSIGN'
    assert token.value == '='

    with raises(StopIteration):
        stream.next()

def test_digits():
    stream = lexer.lex('123456')

    token = stream.next()
    assert token.name == 'DIGITS'
    assert token.value == '123456'

    with raises(StopIteration):
        stream.next()

def test_positive_integer():
    stream = lexer.lex('+123456')

    token = stream.next()
    assert token.name == 'PLUS'
    assert token.value == '+'

    token = stream.next()
    assert token.name == 'DIGITS'
    assert token.value == '123456'

    with raises(StopIteration):
        stream.next()

def test_negative_integer():
    stream = lexer.lex('-123456')

    token = stream.next()
    assert token.name == 'MINUS'
    assert token.value == '-'

    token = stream.next()
    assert token.name == 'DIGITS'
    assert token.value == '123456'

    with raises(StopIteration):
        stream.next()

def test_let_declaration_number():
    stream = lexer.lex('let x = 3;')

    token = stream.next()
    assert token.name == 'LET'
    assert token.value == 'let'

    token = stream.next()
    assert token.name == 'IDENTIFIER'
    assert token.value == 'x'

    token = stream.next()
    assert token.name == 'ASSIGN'
    assert token.value == '='

    token = stream.next()
    assert token.name == 'DIGITS'
    assert token.value == '3'

    token = stream.next()
    assert token.name == 'SEMI_COLON'
    assert token.value == ';'

    with raises(StopIteration):
        stream.next()

def test_let_declaration_string():
    stream = lexer.lex('let hello = "world";')

    token = stream.next()
    assert token.name == 'LET'
    assert token.value == 'let'

    token = stream.next()
    assert token.name == 'IDENTIFIER'
    assert token.value == 'hello'

    token = stream.next()
    assert token.name == 'ASSIGN'
    assert token.value == '='

    token = stream.next()
    assert token.name == 'STRING'
    assert token.value == '"world"'

    token = stream.next()
    assert token.name == 'SEMI_COLON'
    assert token.value == ';'

    with raises(StopIteration):
        stream.next()

def test_let_declaration_if_boolean():
    code = '''let triangle = 
                if (side_a == side_b && side_b == side_c) { 
                    print("equilateral")
                } else {
                    if (
                        side_a == side_b || 
                        side_b == side_c || 
                        side_c == side_a
                    ) {
                        print("isoceles")
                    } else {
                        print("scalene")
                    }
                } ; // TODO: check for right triangle :D
                    print(triangle)
                }
            '''
    stream = lexer.lex(code)

    token = stream.next()
    assert token.name == 'LET'
    assert token.value == 'let'

    token = stream.next()
    assert token.name == 'IDENTIFIER'
    assert token.value == 'triangle'

    token = stream.next()
    assert token.name == 'ASSIGN'
    assert token.value == '='

    token = stream.next()
    assert token.name == 'IF'
    assert token.value == 'if'

    token = stream.next()
    assert token.name == 'OPEN_PARENS'
    assert token.value == '('

    token = stream.next()
    assert token.name == 'IDENTIFIER'
    assert token.value == 'side_a'

    token = stream.next()
    assert token.name == 'EQ'
    assert token.value == '=='
    
    token = stream.next()
    assert token.name == 'IDENTIFIER'
    assert token.value == 'side_b'

    token = stream.next()
    assert token.name == 'AND'
    assert token.value == '&&'

    token = stream.next()
    assert token.name == 'IDENTIFIER'
    assert token.value == 'side_b'

    token = stream.next()
    assert token.name == 'EQ'
    assert token.value == '=='
    
    token = stream.next()
    assert token.name == 'IDENTIFIER'
    assert token.value == 'side_c'

    token = stream.next()
    assert token.name == 'CLOSE_PARENS'
    assert token.value == ')'

    token = stream.next()
    assert token.name == 'OPEN_BRACES'
    assert token.value == '{'

    token = stream.next()
    assert token.name == 'PRINT'
    assert token.value == 'print'

    token = stream.next()
    assert token.name == 'OPEN_PARENS'
    assert token.value == '('

    token = stream.next()
    assert token.name == 'STRING'
    assert token.value == '"equilateral"'

    token = stream.next()
    assert token.name == 'CLOSE_PARENS'
    assert token.value == ')'

    token = stream.next()
    assert token.name == 'CLOSE_BRACES'
    assert token.value == '}'

    token = stream.next()
    assert token.name == 'ELSE'
    assert token.value == 'else'    

    token = stream.next()
    assert token.name == 'OPEN_BRACES'
    assert token.value == '{'
    
    token = stream.next()
    assert token.name == 'IF'
    assert token.value == 'if'

    token = stream.next()
    assert token.name == 'OPEN_PARENS'
    assert token.value == '('

    token = stream.next()
    assert token.name == 'IDENTIFIER'
    assert token.value == 'side_a'

    token = stream.next()
    assert token.name == 'EQ'
    assert token.value == '=='
    
    token = stream.next()
    assert token.name == 'IDENTIFIER'
    assert token.value == 'side_b'

    token = stream.next()
    assert token.name == 'OR'
    assert token.value == '||'

    token = stream.next()
    assert token.name == 'IDENTIFIER'
    assert token.value == 'side_b'

    token = stream.next()
    assert token.name == 'EQ'
    assert token.value == '=='
    
    token = stream.next()
    assert token.name == 'IDENTIFIER'
    assert token.value == 'side_c'

    token = stream.next()
    assert token.name == 'OR'
    assert token.value == '||'

    token = stream.next()
    assert token.name == 'IDENTIFIER'
    assert token.value == 'side_c'

    token = stream.next()
    assert token.name == 'EQ'
    assert token.value == '=='
    
    token = stream.next()
    assert token.name == 'IDENTIFIER'
    assert token.value == 'side_a'

    token = stream.next()
    assert token.name == 'CLOSE_PARENS'
    assert token.value == ')'

    token = stream.next()
    assert token.name == 'OPEN_BRACES'
    assert token.value == '{'

    token = stream.next()
    assert token.name == 'PRINT'
    assert token.value == 'print'

    token = stream.next()
    assert token.name == 'OPEN_PARENS'
    assert token.value == '('

    token = stream.next()
    assert token.name == 'STRING'
    assert token.value == '"isoceles"'

    token = stream.next()
    assert token.name == 'CLOSE_PARENS'
    assert token.value == ')'

    token = stream.next()
    assert token.name == 'CLOSE_BRACES'
    assert token.value == '}'

    token = stream.next()
    assert token.name == 'ELSE'
    assert token.value == 'else'    

    token = stream.next()
    assert token.name == 'OPEN_BRACES'
    assert token.value == '{'

    token = stream.next()
    assert token.name == 'PRINT'
    assert token.value == 'print'

    token = stream.next()
    assert token.name == 'OPEN_PARENS'
    assert token.value == '('

    token = stream.next()
    assert token.name == 'STRING'
    assert token.value == '"scalene"'

    token = stream.next()
    assert token.name == 'CLOSE_PARENS'
    assert token.value == ')'

    token = stream.next()
    assert token.name == 'CLOSE_BRACES'
    assert token.value == '}'

    token = stream.next()
    assert token.name == 'CLOSE_BRACES'
    assert token.value == '}'

    token = stream.next()
    assert token.name == 'SEMI_COLON'
    assert token.value == ';'

    token = stream.next()
    assert token.name == 'PRINT'
    assert token.value == 'print'

    token = stream.next()
    assert token.name == 'OPEN_PARENS'
    assert token.value == '('

    token = stream.next()
    assert token.name == 'IDENTIFIER'
    assert token.value == 'triangle'

    token = stream.next()
    assert token.name == 'CLOSE_PARENS'
    assert token.value == ')'

    token = stream.next()
    assert token.name == 'CLOSE_BRACES'
    assert token.value == '}'

    with raises(StopIteration):
        stream.next()