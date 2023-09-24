from rply import ParserGenerator

from rinha.lexical import lexicon
from rinha import ast

pg = ParserGenerator(
    tokens=lexicon
)
  
@pg.production('term : STRING')
def term_string(tokens):
    string, = tokens
    return ast.Str(string.getstr())

@pg.production('term : DIGITS')
def term_number(tokens):
    digits, = tokens
    return ast.Int(int(digits.getstr()))

@pg.production('term : PRINT OPEN_PARENS term CLOSE_PARENS')
def print_term(tokens):
    print_call, lparen, term, rparen = tokens
    return ast.Print(term)

parser = pg.build()
