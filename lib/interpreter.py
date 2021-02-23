from .tokens import *
from .errors import RTError
from .symbols import SymbolTable

class Context:
    def  __init__(self, displayName, parent=None, parentEntry=None):
        self.displayName = displayName
        self.parent = parent
        self.parentEntry = parentEntry
        self.symbolTable = None

class RTResult:
    def __init__(self):
        self.value = None
        self.error = None
    
    def success(self, value):
        self.value = value
        return self

    def failure(self, error):
        self.error = error
        return self

    def register(self, res):
        if isinstance(res, RTResult):
            if res.error: self.error = res.error
            return res.value
        return res

class Number:
    def __init__(self, value):
        self.value = value
        self.setPos()
        self.setContext()

    def setContext(self, context=None):
        self.context = context
        return self

    def setPos(self, startPos=None, endPos=None):
        self.startPos = startPos
        self.endPos   = endPos
        return self
    
    def addedTo(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).setContext(self.context), None
        
    def subbtractedBy(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).setContext(self.context), None

    def multipliedBy(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).setContext(self.context), None

    def poweredBy(self, other):
        if isinstance(other, Number):
            return Number(self.value ** other.value).setContext(self.context), None

    def dividedBy(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError(
                    other.startPos, other.endPos,
                    "Division by Zero", self.context
                )
            return Number(self.value / other.value).setContext(self.context), None

    def __repr__(self):
        return f'{self.value}'


##################################
# Interpreter
##################################

class Interpreter:
    def visit(self, node, context):
        methodType = f'visit{type(node).__name__}'
        method = getattr(self, methodType, self.noVisitMethod)
        return method(node, context)
    
    def noVisitMethod(self, node):
        raise Exception(f'No visit{type(node).__name__} method defined')

    def visitNumberNode(self, node, context):
        return RTResult().success(
            Number(node.token.value).setPos(node.startPos, node.endPos).setContext(context)
        )

    def visitVarAssignNode(self, node, context):
        res = RTResult()
        varName = node.varNameToken.value
        value = res.register(self.visit(node.nodeValue, context))
        if res.error: return res

        context.symbolTable.set(varName, value)
        return res.success(value)

    def visitVarAccessNode(self, node, context):
        res = RTResult()
        varName = node.varNameToken.value
        value = context.symbolTable.get(varName)
        
        if not value:
            return res.failure(RTError(
                node.startPos, node.endPos,
                f"'{varName}' is not defined", context
            ))
        value = value.copy().setPos(node.startPos, node.endPos)
        return res.success(value)

    def visitBinaryOperationNode(self, node, context):
        res = RTResult()
        left = res.register(self.visit(node.leftNode, context))
        if res.error: return res
        right = res.register(self.visit(node.rightNode, context))
        if res.error: return res
        

        if node.opToken.type == TT_PLUS:
            result, error = left.addedTo(right)
        elif node.opToken.type == TT_MINUS:
            result, error = left.subbtractedBy(right)
        elif node.opToken.type == TT_MUL:
            result, error = left.multipliedBy(right)
        elif node.opToken.type == TT_DIV:
            result, error = left.dividedBy(right)
        elif node.opToken.type == TT_POW:
            result, error = left.poweredBy(right)
        
        if error: return res.failure(error)
        return res.success(result.setPos(node.startPos, node.endPos))

    def visitUnaryOperationNode(self, node, context):
        
        res = RTResult()
        error = None
        number = res.register(self.visit(node.node, context))
        if res.error: return res
        
        if node.opToken.type == TT_MINUS:
            number, error = number.multipliedBy(Number(-1))

        if error: return res.failure(error)
        return res.success(number.setPos(node.startPos, node.endPos))