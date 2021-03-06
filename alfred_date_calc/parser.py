#!/usr/bin/env python2.7
# coding=utf
from __future__ import print_function
from funcparserlib.lexer import make_tokenizer, Token
from funcparserlib.parser import (some, a, maybe, many, finished, skip,
                                  forward_decl, NoParseError)
from funcparserlib.util import pretty_tree

import token
from functools import reduce
from pprint import pprint

from ast import *
from unit import select_unit, Number, DateTime


class Parser:
    def parse(self, text):
        tokens = self._tokenize(text)
        return self._parse(tokens)

    def _tokenize(self, str):
        specs = [
            ('WORD', (r'[a-zA-Zа-яА-Я]+',)),
            ('BR', (r'\(|\)',)),
            ('SPACE', (r'[ \t\r\n]+',)),
            ('NUMBER', (r'[0-9]+\.[0-9]+|\.?[0-9]+(?!\.)',)),
            ('COMMA', (r',',)),
            ('OP', (r'[*/+-]',)),
            ('FORMAT', (r'[^ ]+',)),
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

        def make_raw_value(data):
            value = data
            return Atom(t.value, None)

        def make_atom(data):
            value, unit, left = data
            try:
                value = int(value.value)
            except:
                value = float(value.value)
            if not unit:
                unit = Number
            right = unit(value)
            if left:
                return AddOperator([right, left[0]])
            return right

        def make_signed_atom(data):
            sign, atom = data            
            if sign.value == '-':
                return MulOperator([Number(-1), atom])
            else: 
                return atom
            
        def make_operator(data):
            arg1, lst = data
            for f, arg2 in lst:
                arg1 = f([arg1, arg2])

            return arg1

        def make_unit(tokens):
            if not tokens:
                return None
            unit_name = words(tokens)
            return select_unit(unit_name)

        def make_unit_define(tokens):
            expr, unit = tokens
            if unit:
                return UnitDefine(expr, unit)
            else:
                return expr

        def operator(symbol, node):
            return a(Token('OP', symbol)) >> (lambda _: node)

        def make_root(tokens):
            ast, fmt = tokens
            if fmt:
                fmt = fmt.value
            return Root(ast, fmt=fmt)

        add = operator('+', AddOperator)
        sub = operator('-', SubOperator)
        mul = operator('*', MulOperator)
        div = operator('/', DivOperator)
        sign = lambda t: t.type == 'OP' and t.value == '-'
        now = a(Token('WORD', 'now')) >> (lambda _: DateTime())
        yesterday = a(Token('WORD', 'yesterday')) >> (lambda _: Yesterday())
        keyword = now | yesterday
        add_op = add | sub
        mul_op = mul | div
        unit = many(word) >> make_unit
        number = some(lambda t: t.type == 'NUMBER')
        expr = forward_decl()

        raw_value = number >> make_raw_value
        signed_raw_value = some(sign) + number >> make_signed_atom
        value = forward_decl()
        value_r = number + unit + many(value) >> make_atom
        value.define(value_r)
        signed_value = some(sign) + value >> make_signed_atom
        in_braces = open_brace + expr + close_brace + maybe(unit) >> make_unit_define
        signed_in_braces = some(sign) + in_braces >> make_signed_atom
        basexpr = in_braces | signed_in_braces | keyword | signed_value | value | signed_raw_value | raw_value
        mulexpr = basexpr + many(mul_op + basexpr) >> make_operator
        addexp = mulexpr + many(add_op + mulexpr) >> make_operator

        expr.define(addexp)

        # format = word + many(word) >> (lambda tokens: Text(tokens[0].value + words(tokens[1])))
        # toplevel = expr + maybe(skip(comma) + format) + skip(finished) >> make_root

        format_delim = comma | a(Token('WORD', 'to'))
        format = some(lambda t: t.type == 'FORMAT') | number

        toplevel = expr + maybe(skip(format_delim) + format) + skip(finished) >> make_root

        return toplevel.parse(seq)

def pretty(ast):

    def kids(node):
        if isinstance(node, AST):
            return node.children
        else:
            return []
    
    def show(node):
        return node.repr()
    
    return pretty_tree(ast, kids, show)

if __name__ == '__main__':
    parser = Parser()
    
    inp = "1 month + now"
    print("input:", inp)
    print("tokens:")

    tokens = parser._tokenize(inp)
    print(tokens)
    print("---- PARSING ----")
    tree = parser._parse(tokens)
    print("tree:")
    print(pretty(tree))
    print("result:", tree.eval())
