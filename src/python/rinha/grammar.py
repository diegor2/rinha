from rply import ParserGenerator

from rinha.lexical import lexicon
from rinha import ast

pg = ParserGenerator(
    tokens=lexicon
)

## Optionals

@pg.production('term : OPEN_PARENS term CLOSE_PARENS')
def term_parens(_, tokens):
    return tokens[1]

@pg.production('term : term SEMI_COLON')
def term_semi(_, tokens):
    return tokens[0]

## Literals

@pg.production('term : DIGITS')
def term_digits(_, tokens):
    return ast.Int(int(tokens[0].getstr()))

@pg.production('term : STRING')
def term_string(_, tokens):
    string = tokens[0].getstr()
    return ast.Str(string[1:][:-1])

@pg.production('term : bool')
def term_bool(_, tokens):
    return tokens[0]

@pg.production('bool : TRUE | FALSE')
def bool_literal(_, tokens):
    return ast.Bool(tokens[0].gettokentype() == 'TRUE')

## Collections

@pg.production('term : OPEN_PARENS term COMMA term CLOSE_PARENS')
def term_tuple(_, tokens):
    _, left, _, right, _ = tokens
    return ast.Tuple(left, right)

@pg.production('term : FIRST OPEN_PARENS IDENTIFIER CLOSE_PARENS')
def term_first(state, tokens):
    identifier = tokens[2].getstr()

    target = state.context[identifier]
    assert isinstance(target, ast.Tuple)
    
    return ast.First(target)
    
## Binary

@pg.production('term : binary')
def term_binary(_, tokens):
    return tokens[0]

@pg.production('binary : term AND term')
def binary_sum(_, tokens):
    left, _, right = tokens
    return ast.And(left, right)

@pg.production('binary : term OR term')
def binary_sum(_, tokens):
    left, _, right = tokens
    return ast.Or(left, right)

@pg.production('binary : term EQ term')
def binary_sum(_, tokens):
    left, _, right = tokens
    return ast.Eq(left, right)

@pg.production('binary : term NEQ term')
def binary_sum(_, tokens):
    left, _, right = tokens
    return ast.Neq(left, right)

@pg.production('binary : term LTEQ term')
def binary_sum(_, tokens):
    left, _, right = tokens
    return ast.Lte(left, right)

@pg.production('binary : term GTEQ term')
def binary_sum(_, tokens):
    left, _, right = tokens
    return ast.Gte(left, right)

@pg.production('binary : term LT term')
def binary_sum(_, tokens):
    left, _, right = tokens
    return ast.Lt(left, right)

@pg.production('binary : term GT term')
def binary_sum(_, tokens):
    left, _, right = tokens
    return ast.Gt(left, right)

@pg.production('binary : term PLUS term')
def binary_sum(_, tokens):
    left, _, right = tokens
    return ast.Add(left, right)

@pg.production('binary : term MINUS term')
def binary_sum(_, tokens):
    left, _, right = tokens
    return ast.Sub(left, right)

@pg.production('binary : term STAR term')
def binary_sum(_, tokens):
    left, _, right = tokens
    return ast.Mul(left, right)

@pg.production('binary : term SLASH term')
def binary_sum(_, tokens):
    left, _, right = tokens
    return ast.Div(left, right)

@pg.production('binary : term PERCENT term')
def binary_sum(_, tokens):
    left, _, right = tokens
    return ast.Rem(left, right)

# TODO: Call

## Print

@pg.production('term : print')
def term_print(_, tokens):
    return tokens[0]

@pg.production('print : PRINT OPEN_PARENS term CLOSE_PARENS')
def print_term_call(_, tokens):
    return ast.Print(tokens[2])

## Error

parser = pg.build()
