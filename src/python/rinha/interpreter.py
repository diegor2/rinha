from rinha.lexical import lexer
from rinha.grammar import parser
from rinha.parser_state import ParserState

def interpret(filename, source):
    stream = lexer.lex(source)
    ast = parser.parse(stream, state = ParserState(filename))
    ast.eval()