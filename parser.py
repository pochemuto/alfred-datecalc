#!/usr/bin/env python3
# coding=utf
from funcparserlib.lexer import make_tokenizer, Token
from funcparserlib.parser import (some, a, maybe, many, finished, skip,
                                  forward_decl, NoParseError)
import token
from functools import reduce
from pprint import pprint

from ast import *


class Parser:
    def parse(self, text):
        tokens = self._tokenize(text)
        return self._parse(tokens)

    def _tokenize(self, str):
        specs = [
            ('WORD', (r'[a-zA-Zа-яА-Я]+',)),
            ('BR', (r'\(|\)',)),
            ('SPACE', (r'[ \t\r\n]+',)),
            ('NUMBER', (r'[0-9]+\.[0-9]+|\.?[0-9]+',)),
            ('COMMA', (r',',)),
            ('OP', (r'[*/+-]',)),
        ]
        useless = ['SPACE']
        tokenizer = make_tokenizer(specs)
        return [t for t in tokenizer(str) if t.type not in useless]

    def _parse(self, seq):
        operator = some(lambda t: t.type == 'OP')
        word = some(lambda t: t.type == 'WORD')
        comma = some(lambda t: t.type == 'COMMA')
        open_brace = skip(a(Token('BR', '(')))
        close_brace = skip(a(Token('BR', ')')))

        def tokval(token):
            return token.value

        def words(tokens):
            return " ".join(map(tokval, tokens))

        def make_atom(data):
            value, unit, left = data
            right = Atom(value.value, unit)
            if left:
                return AddOperator([right, left[0]])
            return right

        def make_operator(data):
            arg1, lst = data
            for f, arg2 in lst:
                arg1 = f([arg1, arg2])

            return arg1

        def make_unit(tokens):
            if not tokens:
                return None
            unit_name = words(tokens)
            return Unit(name=unit_name)

        def make_unit_define(tokens):
            expr, unit = tokens
            if unit:
                return UnitDefine(expr, unit)
            else:
                return expr

        def operator(symbol, node):
            return a(Token('OP', symbol)) >> (lambda _: node)

        def make_root(tokens):
            return Root(tokens)

        add = operator('+', AddOperator)
        sub = operator('-', SubOperator)
        mul = operator('*', MulOperator)
        div = operator('/', DivOperator)
        now = a(Token('WORD', 'now')) >> (lambda _: Now())
        yesterday = a(Token('WORD', 'yesterday')) >> (lambda _: Yesterday())
        keyword = now | yesterday
        add_op = add | sub
        mul_op = mul | div
        unit = many(word) >> make_unit
        number = some(lambda t: t.type == 'NUMBER')
        expr = forward_decl()

        raw_value = number >> (lambda t: Atom(t.value, None))
        value = forward_decl()
        value_r = number + unit + many(value) >> make_atom
        value.define(value_r)
        in_braces = open_brace + expr + close_brace + maybe(unit) >> make_unit_define
        basexpr = in_braces | keyword | value | raw_value
        mulexpr = basexpr + many(mul_op + basexpr) >> make_operator
        addexp = mulexpr + many(add_op + mulexpr) >> make_operator

        expr.define(addexp)

        # format = word + many(word) >> (lambda tokens: Text(tokens[0].value + words(tokens[1])))
        # toplevel = expr + maybe(skip(comma) + format) + skip(finished) >> make_root
        toplevel = expr + skip(finished) >> make_root

        return toplevel.parse(seq)


if __name__ == '__main__':
    parser = Parser()
    inp = "(2 + 3 nasta ) * ( 4 week - 1 day )"
    print("input:", inp)
    print("tokens:")

    tokens = parser._tokenize(inp)
    print(tokens)
    print("---- PARSING ----")
    tree = parser._parse(tokens)
    print("tree:")
    print(tree)
    print("result:", tree.eval())
