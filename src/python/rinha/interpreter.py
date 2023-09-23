from rinha.lexical import lexer
from rinha.parsing import parser

def interpret(source):
    stream = lexer.lex(source)
    file = parser.parse(stream)
    file.eval()