from .lexer import *
from .errors import *
from .nodes import *
##################################
# PARSER
##################################

class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
    
    def register(self, res):
        if isinstance(res, ParseResult):
            if res.error: self.error = res.error
            return res.node
        return res

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tokenIndex = -1
        self.currentToken = None
        self.advance()

    def advance(self):
        self.tokenIndex += 1
        if self.tokenIndex < len(self.tokens):
            self.currentToken = self.tokens[self.tokenIndex]
        return self.currentToken

    def atom(self):
        res = ParseResult()
        tok = self.currentToken
        
        # Numbers
        if tok.type in (TT_INT, TT_FLOAT):
            res.register(self.advance())
            return res.success(NumberNode(tok))

        
        # Identifier
        if tok.type == TT_IDENTIFIER:
            res.register(self.advance())
            return res.success(VarAccessNode(tok))
        
        # Parenthesis
        elif tok.type == TT_LPAREN:
            res.register(self.advance())
            expr = res.register(self.expr())
            if res.error: return res
            if self.currentToken.type == TT_RPAREN:
                res.register(self.advance())
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(
                    self.currentToken.startPos, self.currentToken.endPos,
                    "Expected ')'"
                    ))

        return res.failure(InvalidSyntaxError(
            tok.startPos, tok.endPos, 
            "Expected Int or Float, '+', '-' or '(' "
        ))

    def power(self):
        return self.binaryOperation(self.atom, (TT_POW), self.factor)


    def factor(self):
        res = ParseResult()
        tok = self.currentToken
        
        # Unary Operation
        if tok.type in (TT_PLUS, TT_MINUS):
            res.register(self.advance())
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOperationNode(tok, factor))
        
        return self.power()

    def binaryOperation(self, lfunc, operators, rfunc=None):
        if rfunc==None: rfunc = lfunc

        res = ParseResult()
        left = res.register(lfunc())
        if res.error: return res

        while self.currentToken.type in operators:
            opToken = self.currentToken
            res.register(self.advance())
            right = res.register(rfunc())
            if res.error: return res
            left = BinaryOperationNode(left, opToken, right)

        return res.success(left)

    def term(self):
        return self.binaryOperation(self.factor, (TT_MUL, TT_DIV))

    def expr(self):
        res = ParseResult()
        if self.currentToken.matches(TT_KEYWORD, 'var'):
            res.register(self.advance())

            if self.currentToken.type != TT_IDENTIFIER:
                return res.failure(InvalidSyntaxError(
                    self.currentToken.startPos, self.currentToken.endPos,
                    "Expected identifier"
                ))
            
            varName = self.currentToken
            res.register(self.advance())

            if self.currentToken.type != TT_EQ:
                return res.failure(InvalidSyntaxError(
                    self.currentToken.startPos, self.currentToken.endPos,
                    "Expected '='"
                ))
            
            res.register(self.advance())
            expr = res.register(self.expr())
            if res.error: return res
            return res.success(VarAssignNode(varName, expr))

        return self.binaryOperation(self.term, (TT_PLUS, TT_MINUS))

    def parse(self):
        res = self.expr()
        if not res.error and self.currentToken.type != TT_EOF:
            return res.failure(InvalidSyntaxError(
                    self.currentToken.startPos, self.currentToken.endPos,
                    "Expected '+', '-', '*', or '/'"
                )
            )
        return res