from rply import ParserGenerator

from rinha.lexical import lexicon
from rinha import ast

pg = ParserGenerator(
    tokens=lexicon
)

## Parens
@pg.production('term : OPEN_PARENS term CLOSE_PARENS')
def term_parens(tokens):
    return tokens[1]

## Literals
@pg.production('term : literal')
def term_literal(tokens):
    return tokens[0]

@pg.production('literal : int')
def literal_int(tokens):
    return tokens[0]

@pg.production('int : DIGITS')
def int_digits(tokens):
    return ast.Int(int(tokens[0].getstr()))

@pg.production('literal : STRING')
def literal_string(tokens):
    string = tokens[0].getstr()
    return ast.Str(string[1:][:-1])

@pg.production('literal : bool')
def literal_bool(tokens):
    return tokens[0]

@pg.production('bool : TRUE')
def bool_true(tokens):
    return ast.Bool(True)

@pg.production('bool : FALSE')
def bool_false(tokens):
    return ast.Bool(False)

## Binary

@pg.production('term : expression')
def term_expression(tokens):
    return tokens[0]

@pg.production('expression : binary')
def expression_binary_op(tokens):
    return tokens[0]

@pg.production('binary : term PLUS term')
def binary_sum(tokens):
    left, _, right = tokens
    return ast.Add(left, right)

# TODO: Call

## Print

@pg.production('term : print')
def term_print(tokens):
    return tokens[0]

@pg.production('print : PRINT OPEN_PARENS term CLOSE_PARENS')
def print_term_call(tokens):
    return ast.Print(tokens[2])

## Error

parser = pg.build()
