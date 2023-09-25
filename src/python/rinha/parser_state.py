from rply.token import BaseBox

class ParserState(object):
    def __init__(self, filename):
        self.filename = filename
        self.context = {
            'nil': BaseBox()
        }