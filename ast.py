#coding=utf

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

class UnitConvert(AST):

  def __init__(self, child, unit):
    self.children = (child,)
    self.unit = unit

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

class Unit():

  def __init__(self, name):
    self.name = name

  def __str__(self):
    return self.__repr__()

  def __repr__(self):
    return self.name