from rinha.lexical import lexer
from rinha.grammar import parser

def interpret(filename, source):
    stream = lexer.lex(source)
    ast = parser.parse(stream)
    ast.eval()