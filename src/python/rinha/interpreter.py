from rinha.lexical import lexer
from rinha.grammar import parser
from rinha.ast import Reference

def interpret(filename, source):
    stream = lexer.lex(source)
    ast = parser.parse(stream)
    ast.eval()