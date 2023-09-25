from rinha.lexical import lexer
from rinha.grammar import parser
from rinha.ast import Nil

def interpret(filename, source):
    global_scope = {'' : Nil()}
    stream = lexer.lex(source)
    ast = parser.parse(stream)
    ast.eval(global_scope)