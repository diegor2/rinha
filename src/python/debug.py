import sys

from rinha.lexical import lexer
from rinha.grammar import parser
from rinha.ast import dump
    
if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        dump(parser.parse(lexer.lex(f.read())))
