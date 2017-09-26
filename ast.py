# coding=utf


class AST(object):
    children = ()


class Root(AST):
    def __init__(self, expr, fmt=None):
        self.expr = expr
        self.format = fmt

    def __repr__(self):
        return "Root( %s, format='%s' )" % (self.expr, self.format)

    def eval(self):
        return self.expr.eval()


class Operator(AST):
    value = None

    def __init__(self, children):
        self.children = children

    def __repr__(self):
        return "%s( %s )" % (self.__class__.__name__, (" " + self.value + " ").join(map(repr, self.children)))

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

    def eval(self):
        # todo: implement
        return self.children[0].eval()


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
    is_domain = False

    def eval(self):
        return self

    def __init__(self, value=None, name=None):
        if name:
            self.names = (name,)
        self.value = None

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        if self.value:
            return "{0}({1})".format(self.names[0] if self.names else "", self.value)
        else:
            return self.names[0] if self.names else ""
