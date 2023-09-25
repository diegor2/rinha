from rply import ParserGenerator

from rinha.lexical import lexicon
from rinha import ast

pg = ParserGenerator(
    tokens=lexicon
)

## Optionals

@pg.production('term : OPEN_PARENS term CLOSE_PARENS')
def term_parens(tokens):
    return tokens[1]

@pg.production('term : term SEMI_COLON')
def term_semi(tokens):
    return tokens[0]

## Literals

@pg.production('term : DIGITS')
def term_digits(tokens):
    return ast.Int(int(tokens[0].getstr()))

@pg.production('term : STRING')
def term_string(tokens):
    string = tokens[0].getstr()
    return ast.Str(string[1:][:-1])

@pg.production('term : bool')
def term_bool(tokens):
    return tokens[0]

@pg.production('bool : TRUE | FALSE')
def bool_literal(tokens):
    return ast.Bool(tokens[0].gettokentype() == 'TRUE')

## Collections

@pg.production('term : OPEN_PARENS term COMMA term CLOSE_PARENS')
def term_tuple(tokens):
    _, left, _, right, _ = tokens
    return ast.Tuple((left, right))

## Binary

@pg.production('term : expression')
def term_expression(tokens):
    return tokens[0]

@pg.production('expression : binary')
def expression_binary_op(tokens):
    return tokens[0]

@pg.production('binary : term AND term')
def binary_sum(tokens):
    left, _, right = tokens
    return ast.And(left, right)

@pg.production('binary : term OR term')
def binary_sum(tokens):
    left, _, right = tokens
    return ast.Or(left, right)

@pg.production('binary : term EQ term')
def binary_sum(tokens):
    left, _, right = tokens
    return ast.Eq(left, right)

@pg.production('binary : term NEQ term')
def binary_sum(tokens):
    left, _, right = tokens
    return ast.Neq(left, right)

@pg.production('binary : term LTEQ term')
def binary_sum(tokens):
    left, _, right = tokens
    return ast.Lte(left, right)

@pg.production('binary : term GTEQ term')
def binary_sum(tokens):
    left, _, right = tokens
    return ast.Gte(left, right)

@pg.production('binary : term LT term')
def binary_sum(tokens):
    left, _, right = tokens
    return ast.Lt(left, right)

@pg.production('binary : term GT term')
def binary_sum(tokens):
    left, _, right = tokens
    return ast.Gt(left, right)

@pg.production('binary : term PLUS term')
def binary_sum(tokens):
    left, _, right = tokens
    return ast.Add(left, right)

@pg.production('binary : term MINUS term')
def binary_sum(tokens):
    left, _, right = tokens
    return ast.Sub(left, right)

@pg.production('binary : term STAR term')
def binary_sum(tokens):
    left, _, right = tokens
    return ast.Mul(left, right)

@pg.production('binary : term SLASH term')
def binary_sum(tokens):
    left, _, right = tokens
    return ast.Div(left, right)

@pg.production('binary : term PERCENT term')
def binary_sum(tokens):
    left, _, right = tokens
    return ast.Rem(left, right)

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
