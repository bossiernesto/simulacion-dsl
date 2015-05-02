from pyparsing import *
from src.parser.ast import *

# extended definitions
decimal = Regex(r'-?0|[1-9]\d*').setParseAction(lambda t: int(t[0]))
real = Regex(r"[+-]?\d+\.\d*([eE][+-]?\d+)?").setParseAction(lambda tokens: float(tokens[0]))
token = Word(alphanums + "-./_:*+=!<>")
id = Word(alphanums)
string = Optional(token)

SPACE_CHARS = ' \t\s\r'
word = CharsNotIn(SPACE_CHARS)
space = Word(SPACE_CHARS)

CONTEXT_OPEN_CHAR = "{"
context_open = Word(CONTEXT_OPEN_CHAR)
CONTEXT_CLOSE_CHAR = "}"
context_close = word(CONTEXT_CLOSE_CHAR)

ARG_OPEN = "("
ARG_CLOSE = ")"
arg_open = word(ARG_OPEN)
arg_close = word(ARG_CLOSE)

message_name = id
arguments = ZeroOrMore(Suppress(",") + id).setParseAction(Arguments)
message = Combine(id + '.' + message_name + arg_open + arguments + arg_close).setParseAction(MessagePassing)

assignment = (id + "=" + token).setParseAction(Assignment)
printstatement = Combine(Keyword('print') + arg_open + string + arg_close)

innerstatement = assignment
defstatement = (Keyword('def context') + id + context_open + ZeroOrMore(innerstatement) + context_close)

statement = assignment | defstatement

label = delimitedList(word, delim=space, combine=True)

enviroment = (
    Keyword("enviroment") + Optional(":" + token, "enviroment").setParseAction(
        EnviromentName) + context_open + ZeroOrMore(
        statement) + context_close).setParseAction(Enviroment)

simple_parser = Forward()
simple_parser << Optional(enviroment | assignment | message)


class Parser(object):
    def parse(self, input):
        return simple_parser.parseString(input)
