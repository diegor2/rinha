import re
from rply import LexerGenerator

def makeLexer():
    lg = LexerGenerator()
    lg.ignore(r'\s+')  # skip whitespace
    lg.ignore(r'//.*$')  # skip // comments
    lg.ignore(r'/\*.*\*/', re.DOTALL)  # skip // comments
    lg.add('PRINT', r'print')
    return lg.build()