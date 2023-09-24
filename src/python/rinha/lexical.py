import re
from rply import LexerGenerator

__ignore = [
    r'\s+',                     # empty space
    r'[\n\r]+',                 # line break
    r'//.*[\n\r]+',             # single-line // comments
]

__ignore_with_flags = [
    (r'/\*.*\*/', re.DOTALL)    # multiline /* comments */
]

__lexicon_keywords = [
    ('EXTERNAL'          , 'external'),
    ('TRUE'              , 'true'),
    ('FALSE'             , 'false'),
    ('PRINT'             , 'print'),
    ('FIRST'             , 'first'),
    ('SECOND'            , 'second'),
    ('LET'               , 'let'),
    ('IF'                , 'if'),
    ('ELSE'              , 'else'),
    ('FN'                , 'fn'),
]

__lexicon_operators = [
    ('AND'              , '&&'),
    ('OR'               , '||'),
    ('EQ'               , '=='),
    ('NEQ'              , '!='),
    ('LTEQ'             , '<='),
    ('GTEQ'             , '>='),
    ('LT'               , '<'),
    ('GT'               , '>'),
    ('FN_ARROW'         , '=>'),
    ('OPEN_PARENS'      , '('),
    ('CLOSE_PARENS'     , ')'),
    ('OPEN_BRACES'      , '{'),
    ('CLOSE_BRACES'     , '}'),
    ('PLUS'             , '+'),
    ('MINUS'            , '-'),
    ('STAR'             , '*'),
    ('SLASH'            , '/'),
    ('PERCENT'          , '%'),
    ('COMMA'            , ','),
    ('SEMI_COLON'       , ';'),
    ('ASSIGN'           , '='),
]

__lexicon_regex = [
    ('STRING'           , r'"(\\\\|\\"|\\\w|[^"\\\n])*"'),
    ('DIGITS'           , r'\d+'),
    ('IDENTIFIER'       , r'[\w_$][\w\d_$]*'),
]

__lexicon_operators = (
    __lexicon_keywords + 
    __lexicon_operators + 
    __lexicon_regex
)

lexicon = [k for (k, v) in __lexicon_operators]

lg = LexerGenerator()

for regex in __ignore:
    lg.ignore(regex)

for regex, params in __ignore_with_flags:
    lg.ignore(regex, params)

for token, constant in __lexicon_keywords:
    lg.add(token, re.escape(constant))

for token, constant in __lexicon_operators:
    lg.add(token, re.escape(constant))

for token, regex in __lexicon_regex:
    lg.add(token, regex)

lexer = lg.build()
