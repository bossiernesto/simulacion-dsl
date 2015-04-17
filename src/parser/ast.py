"""

"""

"""
This is the AST node class that will define the structure after the parsing process and will generate the python code to be performed later on.
"""
class ASTNode(object):
    def __init__(self, tokens):
        self.tokens = tokens
        self.assignFields()

    def __str__(self):
        return self.__class__.__name__ + ':' + str(self.__dict__)

    __repr__ = __str__


class Assignment(ASTNode):
    def assignFields(self):
        self.lhs, self.rhs = self.tokens
        del self.tokens


class FunctionCall(ASTNode):
    def assignFields(self):
        self.fnName, self.args = self.tokens
        del self.tokens


