"""

"""

"""
This is the AST node class that will define the structure after the parsing process and will generate the python code to be performed later on.
"""
class ASTNode(object):
    pass

class ContextDefinition(ASTNode):
    def __init__(self, values):
        context_name, inner_block = values
        self.context_name = context_name
        self.inner_block = inner_block

class Environment(ASTNode):
    def __init__(self, inner_block):
        self.inner_block = inner_block

class Assignment(ASTNode):
    def __init__(self, values):
        id, value = values
        self.id = id
        self.value = value

class AbstractMethodCall(ASTNode):
    def __init__(self, values):
        function_name, arguments = values
        self.arguments = []
        self.function_name = function_name
        for argument in arguments:
            new_argument = Argument(argument.name, None) if not argument.value else Argument(argument.value, argument.name)
            self.arguments.append(new_argument)

class FunctionCall(AbstractMethodCall):
    pass

class EnvironmentCall(AbstractMethodCall):
    pass

class Argument(ASTNode):
    def __init__(self, value, name):
        self.value = value
        self.name = name

class Accessor(ASTNode):
    def __init__(self, values):
        self.receptor, self.attr = values

