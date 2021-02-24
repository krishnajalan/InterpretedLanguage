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

    def advance(self, currentChar=None):
        self.idx += 1
        self.col += 1
        if currentChar == '\n':
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
        self.currentChar = None
        self.advance()

    def advance(self):
        self.pos.advance(self.currentChar)
        self.currentChar = self.text[self.pos.idx] if self.pos.idx < len(
            self.text) else None

    def make_token(self):
        tokens = []

        while self.currentChar != None:
            if self.currentChar in '\t ':
                self.advance()
            elif self.currentChar in DIGITS:
                tokens.append(self.makeNumber())
            elif self.currentChar in LETTERS:
                tokens.append(self.makeIdentifier())
            elif self.currentChar == '+':
                tokens.append(Token(TT_PLUS, startPos=self.pos))
                self.advance()
            elif self.currentChar == '-':
                tokens.append(Token(TT_MINUS, startPos=self.pos))
                self.advance()
            elif self.currentChar == '*':
                tokens.append(Token(TT_MUL, startPos=self.pos))
                self.advance()
            elif self.currentChar == '/':
                tokens.append(Token(TT_DIV, startPos=self.pos))
                self.advance()
            elif self.currentChar == '^':
                tokens.append(Token(TT_POW, startPos=self.pos))
                self.advance()
            elif self.currentChar == '=':
                tok, error = self.makeEquals()
                if error: return [], error
                tokens.append(tok)
            elif self.currentChar == '!':
                tok, error = self.makeNotEquals()
                if error: return [], error
                tokens.append(tok)
            elif self.currentChar == '>':
                tok, error = self.makeGreaterThan()
                if error: return [], error
                tokens.append(tok)
            elif self.currentChar == '<':
                tok, error = self.makeLessThan()
                if error: return [], error
                tokens.append(tok)
            elif self.currentChar == '(':
                tokens.append(Token(TT_LPAREN, startPos=self.pos))
                self.advance()
            elif self.currentChar == ')':
                tokens.append(Token(TT_RPAREN, startPos=self.pos))
                self.advance()
            else:
                startPos = self.pos.copy()
                character = self.currentChar
                self.advance()
                return [], IllegalCharacterError(startPos, self.pos, "'"+character+"'")

        tokens.append(Token(TT_EOF, startPos=self.pos))
        return tokens, None

    def makeNumber(self):
        num = ''
        dotCount = 0
        startPos = self.pos.copy()

        while self.currentChar != None and self.currentChar in DIGITS + ".":
            if self.currentChar == '.':
                if dotCount == 1:
                    break
                dotCount += 1
                num += '.'
            else:
                num += self.currentChar
            self.advance()

        if dotCount == 0:
            return Token(TT_INT, int(num), startPos, self.pos)
        else:
            return Token(TT_FLOAT, float(num), startPos, self.pos)

    def makeIdentifier(self):
        id = ''
        startPos = self.pos.copy()

        while self.currentChar != None and self.currentChar in LETTERS_DIGITS:
            id += self.currentChar
            self.advance()
        
        tokType = TT_KEYWORD if id in KEYWORDS else TT_IDENTIFIER
        return Token(tokType, id, startPos, self.pos)

    def makeEquals(self):
        tokType = TT_EQ
        startPos = self.pos.copy()
        self.advance()

        if self.currentChar == '=':
            self.advance()
            tokType = TT_EE

        print("debug again:", tokType)
        return  Token(tokType, startPos=startPos, endPos=self.pos), None
    
    def makeNotEquals(self):
        startPos = self.pos.copy()
        self.advance()

        if self.currentChar == '=':
            self.advance()
            return Token(TT_NE, startPos=startPos, endPos=self.pos), None
        
        self.advance()
        return None, ExpectedCharError(startPos, self.pos, "'=' (after '!')")

    def makeGreaterThan(self):
        tokType = TT_GT
        startPos = self.pos.copy()
        self.advance()

        if self.currentChar == '=':
            self.advance()
            tokType = TT_GTE
        
        return Token(tokType, startPos=startPos, endPos=self.pos)

    def makeLessThan(self):
        tokType = TT_LT
        posStart = self.pos.copy()
        self.advance()

        if self.currentChar == '=':
            self.advance()
            tokType = TT_LTE
        
        return Token(tokType, startPos=posStart, endPos=self.pos)