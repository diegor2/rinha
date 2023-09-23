import re
from rply import LexerGenerator

__ignore = [
    r'\s+',                     # empty space
    r'[\n\r]+',                 # line break
    r'//.*[\n\r]+',             # single-line // comments
    r'"',                       # quotes 
]

__ignore_with_params = [
    (r'/\*.*\*/', re.DOTALL)    # multiline /* comments */
]

__lexicon_rules = {    
    'PRINT'             : r'print',
    'STRING'            : r'(?<=").+(?=")',
    'OPEN_PARENS'   : r'\(',
    'CLOSE_PARENS'  : r'\)',
}

lexicon = __lexicon_rules.keys()

lg = LexerGenerator()

for regex in __ignore:
    lg.ignore(regex)

for regex, params in __ignore_with_params:
    lg.ignore(regex, params)

for token, regex in __lexicon_rules.items():
    lg.add(token, regex) 

lexer = lg.build()
