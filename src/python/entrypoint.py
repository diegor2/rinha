import sys

from rinha.lexical import lexer
from rinha.grammar import parser
from rinha.ast import dump
    

def interpret(filename, source):
    stream = lexer.lex(source)
    ast = parser.parse(stream)
    ast.eval()

if __name__ == "__main__":
    filename = sys.argv[1]
    with open(filename) as f:
        interpret(filename, f.read())
