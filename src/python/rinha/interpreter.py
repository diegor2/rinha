from rinha.lexical import lexer
from rinha.grammar import parser
from rinha.ast import Reference

def interpret(filename, source):
    global_scope = {None : Reference(None)}
    stream = lexer.lex(source)
    ast = parser.parse(stream)
    ast.eval(global_scope)