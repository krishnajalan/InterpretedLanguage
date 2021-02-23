##################################
# TOKEN
##################################

TT_INT = 'INT'
TT_FLOAT = 'FLOAT'
TT_IDENTIFIER = 'IDENTIFIER'
TT_KEYWORD = 'KEYWORD'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_EQ = 'EQ'
TT_POW = 'POW'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'
TT_EOF = 'EOF'

KEYWORDS = [
    'var'
]

class Token:
    def __init__(self, type_, value=None, startPos=None, endPos=None):
        self.type = type_
        self.value = value
        if startPos:
            self.startPos = startPos.copy()
            self.endPos = startPos.copy()
            self.endPos.advance()

        if endPos:
            self.endPos = endPos

    def __repr__(self):
        if self.value:
            return f'{self.type}:{self.value}'
        return f'{self.type}'

    def matches(self, type_, value):
        return self.type == type_ and self.value == value