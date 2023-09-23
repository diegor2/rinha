import re
from rply import LexerGenerator

def makeLexer():
    lg = LexerGenerator()
    lg.ignore(r'\s+') # empty space
    lg.ignore(r'[\n\r]+') # line break
    lg.ignore(r'//.*[\n\r]+')  # single-line // comments
    lg.ignore(r'/\*.*\*/', re.DOTALL)  # multiline /* comments */ 
    lg.add('LINE_BREAK', r'[\n\r]+') 
    lg.add('PRINT', r'print')
    lg.add('QUOTE', r'"')    
    lg.add('STRING', r'(?<=").+(?=")')
    lg.add('LEFT_PARENTESIS', r'\(')
    lg.add('RIGHT_PARENTESIS', r'\)')
    return lg.build()