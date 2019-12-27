# coding=utf

import format
from inspect import getmro


def pretty_float(number):
    if int(number) == number:
        return str(int(number))
    else:
        return str(number)

class AST(object):
    children = ()

    def repr(self):
        return repr(self)

class Root(AST):
    def __init__(self, expr, fmt=None):
        self.children = (expr, )
        self.expr = expr
        self.format = fmt

    def __repr__(self):
        return "Root( %s, format='%s' )" % (self.expr, self.format)

    def repr(self):
        return "Root format='%s'" % self.format

    def eval(self):
        result = self.expr.eval()
        if self.format:
            return result.format(self.format)
        else:
            return result


class Operator(AST):
    value = None

    def __init__(self, children):
        self.children = children

    def __repr__(self):
        return "%s( %s )" % (self.__class__.__name__, (" " + self.value + " ").join(map(repr, self.children)))

    def repr(self):
        return self.__class__.__name__

    def action(self, a, b):
        pass
    
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


class Text(AST):
    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return self.text

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


class UnitDefine(AST):
    def __init__(self, child, unit):
        self.children = (child,)
        self.unit = unit

    def __repr__(self):
        return "UnitDefine( %s %s )" % (self.children[0], self.unit)

    def repr(self):
        return "UnitDefine %s" % self.unit

    def eval(self):
       return self.children[0].eval().cast(self.unit)


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


class Unit:
    names = []
    multiplicator = 1
    weight = 1
    is_domain = False

    def __init__(self, value=None, name=None):
        if name:
            self.names = (name,)
        self.value = value

    def __add__(self, other):
        return NotImplemented

    def __sub__(self, other):
        return NotImplemented

    def __mul__(self, other):
        return NotImplemented
        
    def __div__(self, other):
        return NotImplemented
        
    def cast(self, unit):
        raise NotImplementedError()
        
    def __lt__(self, other):
        return NotImplemented
        
    def __gt__(self, other):
        return NotImplemented
        
    def __eq__(self, other):
        return NotImplemented
        
    def __hash__(self):
        return NotImplemented

    def eval(self):
        return self

    def format(self, fmt):
        return format.decimal(fmt, self.value) or self._unknown_format(fmt)

    def _unknown_format(self, fmt):
        raise Exception('unknown format "' + fmt + '"')
    
    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        if self.value is not None:
            return "{0}({1})".format(self._default_name(), pretty_float(self.value))
        else:
            return self._default_name()

    def repr(self):
        return repr(self)

    def domain(self):
        domain = self.__class__
        for cls in getmro(self.__class__):
            if cls.is_domain:
                domain = cls
            else:
                break
        return domain

    def _compatible_with(self, other):
        return self.domain() == other.domain()

    def is_zero(self):
        return self.value == 0
    
    def _default_name(self):
        if self.names:
            return self.names[0]
        else:
            return self.__class__
