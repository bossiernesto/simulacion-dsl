import re
import logging
from re import VERBOSE
from pprint import pformat
from funcparserlib.lexer import make_tokenizer, Token, LexerError
from funcparserlib.parser import (some, a, maybe, many, finished, skip,
                                  forward_decl, NoParseError)
from collections import namedtuple
from ast import *
from src.all_exceptions import DSLLexerException, DSLParserException

debug = True
ENCODING = u'UTF-8'
regexps = {
    u'escaped': ur'''
        \\                                  # Escape
          ((?P<standard>["\\/bfnrt])        # Standard escapes
        | (u(?P<unicode>[0-9A-Fa-f]{4})))   # uXXXX
        ''',
    u'unescaped': ur'''
        [^"\\]                              # Unescaped: avoid ["\\]
        ''',
}
re_esc = re.compile(regexps[u'escaped'], VERBOSE)


def unescape(s):
    std = {
        u'"': u'"', u'\\': u'\\', u'/': u'/', u'b': u'\b', u'f': u'\f',
        u'n': u'\n', u'r': u'\r', u't': u'\t',
    }

    def sub(m):
        if m.group(u'standard') is not None:
            return std[m.group(u'standard')]
        else:
            return unichr(int(m.group(u'unicode'), 16))

    return re_esc.sub(sub, s)


def tokenize(str):
    """str -> Sequence(Token)"""
    specs = [
        (u'keyword', (ur'({|}|def|context|environment|\.|\(|\))',)),
        (u'Space', (ur'[ \t\r\n]+',)),
        (u'String', (ur'"(%(unescaped)s | %(escaped)s)*"' % regexps, VERBOSE)),
        (u'Number', (ur'''
            -?                  # Minus
            (0|([1-9][0-9]*))   # Int
            (\.[0-9]+)?         # Frac
            ([Ee][+-][0-9]+)?   # Exp
            ''', VERBOSE)),
        (u'Eq', (ur'=',)),
        (u'Sep', (ur',',)),
        (u'Op', (ur'[{}\[\]\-,:]',)),
        (u'Name', (ur'[A-Za-z_][A-Za-z_0-9]*',))
    ]
    useless = [u'Space']
    t = make_tokenizer(specs)
    return [x for x in t(str) if x.type not in useless]


def parse(seq):
    Attr = namedtuple('Attr', 'name value')

    """Sequence(Token) -> object"""
    keyword = lambda s: a(Token(u'keyword', s))
    sep = lambda s: a(Token(u'Sep', s))

    context_open = skip(keyword(u'{'))
    context_close = skip(keyword(u'}'))
    call_open = skip(keyword(u'('))
    call_close = skip(keyword(u')'))
    def_keyword = skip(keyword(u'def'))
    context_keywork = skip(keyword(u'context'))
    eq_keyword = a(Token(u'Eq', '='))
    environment_keyword = skip(keyword(u'environment'))
    delegation_keyword = skip(keyword(u'.'))
    comma = sep(u',')


    ## Helpers
    # skipped values
    def make_number(n):
        try:
            return int(n)
        except ValueError:
            return float(n)

    def unescape_string(value):
        return unescape(value[1:-1])

    def make_string(value):
        return value

    unarg = lambda f: lambda args: f(*args)
    a_ = lambda x: skip(a(x))
    isContextOpenClose = lambda s: some(s.value in [context_open, context_close])
    const = lambda x: lambda _: x
    tokval = lambda x: x.value
    toktype = lambda type: some(lambda x: x.type == type) >> tokval

    # types
    eq = toktype(u'Eq') >> make_string
    id = toktype(u'Name') >> make_string
    string = toktype(u'String') >> unescape_string
    number = toktype(u'Number') >> make_number
    value = id | number
    name = lambda s: a(Token(u'Name', s)) >> tokval
    accessor = forward_decl()
    argument = accessor | value | string
    function = id
    argument_list = (
        argument +
        maybe(skip(eq_keyword) + argument) +
        skip(maybe(comma))
        >> unarg(Attr))

    # rules
    assignment = id + skip(eq) + argument >> Assignment
    functionCall = function + call_open + many(argument_list) + call_close >> FunctionCall
    environmentCall = environment_keyword + delegation_keyword + id + call_open + many(
        argument_list) + call_close >> EnvironmentCall
    accessor.define(id + delegation_keyword + id >> Accessor)

    context_block = many(assignment | functionCall)
    contextDefinition = def_keyword + context_keywork + id + context_open + maybe(
        context_block) + context_close >> ContextDefinition

    enviro_block = many(assignment | contextDefinition)
    environment = environment_keyword + context_open + maybe(enviro_block) + context_close >> Environment

    simulacion_line = assignment | environment | environmentCall | functionCall
    simulacion_program = many(simulacion_line) + skip(finished)

    return simulacion_program.parse(seq)


def parse_all(s):
    """str -> object"""
    try:
        return parse(tokenize(s))
    except LexerError, e:
        raise DSLLexerException(e)
    except NoParseError, e:
        relevant = e.msg.split(':')[1:]
        line_offset, token = relevant
        raise DSLParserException("Unable to find parser for expression on {0} that contains token {1}".format(line_offset, token), e.state)