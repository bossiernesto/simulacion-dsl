"""

"""

"""
This is the AST node class that will define the structure after the parsing process and will generate the python code to be performed later on.
"""
CONTEXT_OPEN_CHAR = "{"
CONTEXT_CLOSE_CHAR = "}"
DELIMITERS = [CONTEXT_CLOSE_CHAR, CONTEXT_OPEN_CHAR]


class ASTNode(object):
    def __init__(self, tokens):
        self.tokens = tokens
        self.assignFields()

    def __str__(self):
        return self.__class__.__name__ + ':' + str(self.__dict__)

    __repr__ = __str__


class EnviromentName(ASTNode):
    def assignFields(self):
        self.name = self.tokens[0]

    def get_name(self):
        return self.name


class Enviroment(ASTNode):
    def assignFields(self):
        self.delimiters = DELIMITERS
        self.enviroment_name = self.tokens[1]
        self.statements = []
        l = len(self.tokens)
        for token in self.tokens[2:l]:
            if token in self.delimiters:
                continue
            self.statements.append(token)
        print self.tokens

    def get_enviroment_name(self):
        return self.enviroment_name.get_name()


class Assignment(ASTNode):
    def assignFields(self):
        self.lhs, self.rhs = self.tokens
        del self.tokens


class MessagePassing(ASTNode):
    def assignFields(self):
        pass


class Arguments(ASTNode):
    def assignFields(self):
        self.arguments = self.tokens
        del (self.tokens)


class FunctionCall(ASTNode):
    def assignFields(self):
        self.fnName, self.args = self.tokens
        del self.tokens


