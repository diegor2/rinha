from rply import ParserGenerator

from rinha.lexical import lexicon
from rinha import ast

pg = ParserGenerator(
    tokens=lexicon
)
  
@pg.production('term : DIGITS')
def term_digits(tokens):
    digits, = tokens
    return ast.Int(int(digits.getstr()))

@pg.production('term : STRING')
def term_string(tokens):
    string, = tokens
    return ast.Str(string.getstr())

# Call

@pg.production('term : PRINT OPEN_PARENS term CLOSE_PARENS')
def term_print(tokens):
    print_call, lparen, term, rparen = tokens
    return ast.Print(term)

parser = pg.build()
