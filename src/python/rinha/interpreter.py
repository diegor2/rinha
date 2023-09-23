
from rinha.lexer import makeLexer

lexer = makeLexer()

def interpret(source):
    stream = lexer.lex(source)
    for token in stream:
        print(token)
    