#!/usr/bin/env python3
#coding=utf
from funcparserlib.lexer import make_tokenizer, Token
from funcparserlib.parser import (some, a, maybe, many, finished, skip,
                                  forward_decl, NoParseError)
import token
from functools import reduce
from pprint import pprint

def tokenize(str):
  specs = [
    ('WORD', (r'[a-zA-Zа-яА-Я]+', )),
    ('BR', (r'\(|\)',)),
    ('SPACE', (r'[ \t\r\n]+',)),
    ('NUMBER', (r'[0-9]+\.[0-9]+|\.?[0-9]+',)),
    ('OP', (r'[*/+-]',)),
  ]
  useless = ['SPACE']
  tokenizer = make_tokenizer(specs)
  return [t for t in tokenizer(str) if t.type not in useless]

def parse(seq):
  operator = some(lambda t: t.type == 'OP')
  word = some(lambda t: t.type == 'WORD')
  open_brace = skip(a(Token('BR', '(')))
  close_brace = skip(a(Token('BR', ')')))
  endmark = a(Token(token.ENDMARKER, ''))

  def tokval(token):
    return token.value

  def words(tokens):
    return " ".join(map(tokval, tokens)) or None

  def make_atom(data):
    value, unit, left = data
    right = Atom(value.value, words(unit))
    if left:
      return AddOperator([right, left[0]])
    return right

  def make_operator(data):
    arg1, lst = data
    for f, arg2 in lst:
      arg1 = f([arg1, arg2])

    return arg1

  def operator(symbol, node):
    return a(Token('OP', symbol)) >> (lambda _: node)

  def make_root(data):
    fst, left = data
    unit = words(left)

    return Root(fst, unit)

  add = operator('+', AddOperator)
  sub = operator('-', SubOperator)
  mul = operator('*', MulOperator)
  div = operator('/', DivOperator)
  now = a(Token('WORD', 'now')) >> (lambda _: Now())
  yesterday = a(Token('WORD', 'yesterday')) >> (lambda _: Yesterday())
  keyword = now | yesterday
  add_op = add | sub
  mul_op = mul | div
  unit = many(word)
  number = some(lambda t: t.type == 'NUMBER')
  expr = forward_decl()

  value = number >> (lambda t: Atom(t.value, None))
  datetime = forward_decl()
  datetime_r = number + unit + many(datetime) >> make_atom
  datetime.define(datetime_r)
  basexpr = open_brace + expr + close_brace | keyword | datetime | value
  mulexpr = basexpr + many(mul_op + basexpr) >> make_operator
  addexp = mulexpr + many(add_op + mulexpr) >> make_operator

  expr.define(addexp)

  # formatexp = expr + maybe(unit) + endmark >> make_root
  formatexp = expr + maybe(unit) >> make_root

  return formatexp.parse(seq)

class AST(object):
  children = ()

class Root(AST):
  def __init__(self, expr, format=None):
    self.expr = expr
    self.format = format

  def __repr__(self):
    return "Root(%s, %s)" % (self.expr, self.format)

  def eval(self):
    return self.expr.eval()

class Operator(AST):
  value = None

  def __init__(self, children):
    self.children = children

  def __repr__(self):
    return "%s %s (%s)" % (self.__class__.__name__, self.value, list(map(repr, self.children)))

  def eval(self):
    assert len(self.children) == 2
    return self.action(self.children[0].eval(), self.children[1].eval())

class Keyword(AST):
  def __repr__(self):
    return "Keyword(%s)" % self.__class__.__name__

class Now(Keyword):
  def eval(self):
    return 42  

class Yesterday(Keyword):
  def eval(self):
    return 13

class Atom(AST):
  def __init__(self, value, unit):
    self.value = value
    self.unit = unit

  def __repr__(self):
    if self.unit is None:
      return "Atom(%s)" % self.value
    else:
      return "Atom(%s %s)" % (self.value, self.unit)

  def eval(self):
    try:
      return int(self.value)
    except ValueError:
      return float(self.value)

class AddOperator(Operator):
  value = '+'
  def action(self, x, y):
    return x + y

class SubOperator(Operator):
  value = '-'
  def action(self, x, y):
    return x - y


class MulOperator(Operator):
  value = '*'
  def action(self, x, y):
    return x * y

class DivOperator(Operator):
  value = '/'
  def action(self, x, y):
    return x / y

class Calculator(object):

  def eval(self, text):
    tree = self._parse(text)
    return self._eval_tree(tree)

  def _parse(self, text):
    # parse_tree = ExprParser.parse(text)
    pass
    # return parse_tree

  def _repr_tree(self, text):
    return ExprParser.repr_parse_tree(self._parse(text))

  def _eval_tree(self, tree):
    pass

c = Calculator()

inp = "1 year + 1 month + 3 days * 2"
print("input:", inp)
print("tokens:")
print(tokenize(inp))
print("---- PARSING ----")
tree = parse(tokenize(inp))
print("tree:")
print(tree)
print("result:", tree.eval())

class Result(object):

  def __init__(self, 
          year=None, 
          month=None,
          day=None,
          time=None,
          format=None):
    self.year = year
    self.month = month
    self.day = day
    self.time = time
    self.format = format

  def __eq__(self, other):
    if isinstance(other, self.__class__):
      return self.year == other.year and \
        self.month == other.month and \
        self.day == other.day and \
        self.time == other.time and \
        self.format == other.format

  def __repr__(self):
    return "Result[y={year}, m={month}, d={day}, t={time}, f={format}]".format(**vars(self))

  def __ne__(self, other):
    return not self.__eq__(self, other)