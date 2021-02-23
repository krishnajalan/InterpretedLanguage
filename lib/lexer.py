from .errors import *
from .tokens import *
import string
##################################
# CONSTANTS
##################################

DIGITS = '0123456789'
LETTERS = string.ascii_letters
LETTERS_DIGITS = LETTERS + DIGITS + "_"

##################################
# POSITION
##################################


class Position:
    def __init__(self, index, line, column, fileName, fileText):
        self.idx = index
        self.ln = line
        self.col = column
        self.fn = fileName
        self.ftxt = fileText

    def advance(self, current_char=None):
        self.idx += 1
        self.col += 1
        if current_char == '\n':
            self.ln += 1
            self.col = 0
        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)


##################################
# LEXER
##################################


class Lexer:
    def __init__(self, text, fileName):
        self.fn = fileName
        self.text = text
        self.pos = Position(-1, 0, -1, fileName, text)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(
            self.text) else None

    def make_token(self):
        tokens = []

        while self.current_char != None:
            if self.current_char in '\t ':
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.makeNumber())
            elif self.current_char in LETTERS:
                tokens.append(self.makeIdentifier())
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS, startPos=self.pos))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS, startPos=self.pos))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL, startPos=self.pos))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV, startPos=self.pos))
                self.advance()
            elif self.current_char == '^':
                tokens.append(Token(TT_POW, startPos=self.pos))
                self.advance()
            elif self.current_char == '=':
                tokens.append(Token(TT_EQ, startPos=self.pos))
                self.advance()    
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN, startPos=self.pos))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN, startPos=self.pos))
                self.advance()
            else:
                posStart = self.pos.copy()
                character = self.current_char
                self.advance()
                return [], IllegalCharacterError(posStart, self.pos, "'"+character+"'")

        tokens.append(Token(TT_EOF, startPos=self.pos))
        return tokens, None

    def makeNumber(self):
        num = ''
        dotCount = 0
        startPos = self.pos.copy()

        while self.current_char != None and self.current_char in DIGITS + ".":
            if self.current_char == '.':
                if dotCount == 1:
                    break
                dotCount += 1
                num += '.'
            else:
                num += self.current_char
            self.advance()

        if dotCount == 0:
            return Token(TT_INT, int(num), startPos, self.pos)
        else:
            return Token(TT_FLOAT, float(num), startPos, self.pos)

    def makeIdentifier(self):
        id = ''
        startPos = self.pos.copy()

        while self.current_char != None and self.current_char in LETTERS_DIGITS:
            id += self.current_char
            self.advance()
        
        tokType = TT_KEYWORD if id in KEYWORDS else TT_IDENTIFIER
        return Token(tokType, id, startPos, self.pos)