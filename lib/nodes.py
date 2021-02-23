##################################
# NODES
##################################

class NumberNode:
    def __init__(self, token):
        self.token = token
        self.startPos = token.startPos
        self.endPos = token.endPos

    def __repr__(self):
        return f'{self.token}'


class BinaryOperationNode:
    def __init__(self, leftNode, opToken, rightNode):
        self.leftNode = leftNode
        self.opToken = opToken
        self.rightNode = rightNode

        self.startPos = self.leftNode.startPos
        self.endPos = self.rightNode.endPos

    def __repr__(self):
        return f'({self.leftNode}, {self.opToken}, {self.rightNode})'

class UnaryOperationNode:
    def __init__(self, opToken, node):
        self.opToken = opToken
        self.node = node
        self.startPos = self.opToken.startPos
        self.endPos = self.node.endPos

    def __repr__(self):
        return f'({self.opToken}, {self.node})'

class VarAssignNode:
    def __init__(self, varNameToken, nodeValue):
        self.varNameToken = varNameToken
        self.nodeValue = nodeValue

        self.startPos = self.varNameToken.startPos
        self.endPos = self.varNameToken.endPos

class VarAccessNode:
    def __init__(self, varNameToken):
        self.varNameToken = varNameToken
        self.startPos = varNameToken.startPos
        self.endPos = varNameToken.endPos