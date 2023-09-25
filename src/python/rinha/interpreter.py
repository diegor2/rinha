from rinha.lexical import lexer
from rinha.grammar import parser

def interpret(source):
    stream = lexer.lex(source)
    ast = parser.parse(stream)
    ast.eval()