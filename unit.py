# coding=utf
from __future__ import print_function
from ast import Unit, Atom, pretty_float
from inspect import getmro

units_names = {}

class unit:
    def __init__(self, *names):
        self.names = names

    def __call__(self, cls):
        cls.names = self.names
        for name in self.names:
            units_names[name] = cls

        return cls

def complex(cls):
    add_orig = cls.__add__
    sub_orig = cls.__sub__

    def add(self, other):
        if self.weight != other.weight:
            return ComplexUnit(self, other)
        else:
            return add_orig(self, other)
    
    def sub(self, other):
        if self.weight != other.weight:
            return ComplexUnit(self, other * Number(-1))
        else:
            return sub_orig(self, other)
    
    cls.__add__ = add
    cls.__sub__ = sub
    return cls

def select_unit(name):
    if name in units_names:
        return units_names[name]
    else:
        raise UndefinedUnitException(name)


class UndefinedUnitException(Exception):
    def __init__(self, unit_definition):
        super(Exception, self).__init__("Unknown unit definition: '{}'".format(unit_definition))
        

class OperationError(Exception):
    def __init__(self, message):
        super(OperationError, self).__init__(message)


class ScaleUnit(Unit):
    multiplicator = 1
    
    def __add__(self, other):
        if not self._compatible_with(other):
            raise OperationError("Cannot add {1} to {0}, {2} + {3}".format(self, other, self.domain(), other.domain()))
        
        smaller, bigger, k = self._order_arguments(other)
        return smaller.__class__(bigger.value * k + smaller.value)

    def __sub__(self, other):
        if not self._compatible_with(other):
            raise ArithmeticError("Cannot subtract {1} from {0}, {2} + {3}".format(self, other, self.domain(), other.domain()))

        smaller, bigger, k = self._order_arguments(other)
        sign = -1 if smaller == self else 1
        return smaller.__class__((bigger.value * k - smaller.value) * sign)

    def __mul__(self, other):
        if self.domain() == Number:
            # 1 * 4 days
            return other.__class__(self.value * other.value)
        elif other.domain() == Number:
            # 7 days * 19
            return self.__class__(self.value * other.value)
        else:
            raise ArithmeticError("Cannot multiply {1} and {0}, {2} * {3}".format(self, other, self.domain(), other.domain()))

    def __rmul__(self, other):
        return self * other

    def __div__(self, other):
        if other.domain() == Number:
            # 7 days / 2
            return self.__class__(self.value / float(other.value))
        else:
            raise ArithmeticError("Cannot multiply {1} and {0}, {2} * {3}".format(self, other, self.domain(), other.domain())) 

    def _order_arguments(self, other):
        smaller, bigger = sorted((self, other), key=lambda item: item.k())
        k = int(bigger.k() / smaller.k())
        return smaller, bigger, k

    def raw(self):
        return self.value * self.k()

    def cast(self, unit):
        if unit == Number:
            return Number(self.value)
        if not issubclass(unit, self.domain()):
            raise OperationError("Cannot cast {0} to {1}".format(self, unit))
        else:
            return unit(self.raw() / float(ScaleUnit._k_of_unit(unit)))

    def _same_domain(self, other):
        return self.domain() == other.domain()

    def k(self):
        return ScaleUnit._k_of_unit(self.__class__)

    @staticmethod
    def _k_of_unit(unit):
        k = 1
        for cls in getmro(unit):
            if cls == ScaleUnit:
                break
            k *= cls.multiplicator
        return k
            
    def __lt__(self, other):
        return self.raw() < other.raw()

    def __gt__(self, other):
        return self.raw() > other.raw()

    def __eq__(self, other):
        return self.raw() == other.raw() and self._same_domain(other)
    
    def __hash__(self):
        return self.raw()


class ComplexUnit(Unit):
    def __init__(self, *parts):
        if len(parts) == 0:
            raise Exception("empty complex unit")
        if isinstance(parts[0], dict):
            self._parts = parts[0]
        else:
            self._parts = {u.weight: u for u in parts}
        self._reduce()

    def _compose(self, other, operation):
        result = self._parts.copy()
        for part in other._parts:
            if part in result:
                result[part] = operation(result[part], other._parts[part])
            else:
                result[part] = other._parts[part]
        return ComplexUnit(result)

    def _op(self, other, operation):
        if not isinstance(other, ComplexUnit):
            other = ComplexUnit({other.weight: other})
        return self._compose(other, operation)

    def __add__(self, other):
        if not self._compatible_with(other):
            raise OperationError("Cannot add {1} to {0}, {2} + {3}".format(self, other, self.domain(), other.domain()))
        return self._op(other, lambda a, b: a + b)

    def __sub__(self, other):
        if not self._compatible_with(other):
            raise OperationError("Cannot remove {1} from {0}, {2} + {3}".format(self, other, self.domain(), other.domain()))
        return self + other * Number(-1)

    def _reduce(self):
        parts = self._parts
        self._parts = {k: u for k, u in parts.items() if not u.is_zero()}
        if len(self._parts) == 0:
            w = min(parts.keys())
            self._parts[w] = parts[w]

    def _each(self, other, operation):
        result = self._parts.copy()
        for part in result:
            result[part] = operation(result[part], other)
        return ComplexUnit(result)
        
    def __mul__(self, other):
        if isinstance(other, Number):
            return self._each(other, lambda a, b: a * b)
        else:
            raise ArithmeticError("Cannot multiply {1} and {0}, {2} * {3}".format(self, other, self.domain(), other.domain()))

    def __rmul__(self, other):
        return self * other
        
    def __div__(self, other):
        if isinstance(other, Number):
            return self._each(other, lambda a, b: a / b)
        else:
            raise ArithmeticError("Cannot divide {0} to {1}, {2} / {3}".format(self, other, self.domain(), other.domain()))
        
    def cast(self, unit):
        raise NotImplementedError()

    def domain(self):
        return self._parts.itervalues().next().domain()

    def __lt__(self, other):
        return NotImplemented
        
    def __gt__(self, other):
        return NotImplemented
        
    def __eq__(self, other):
        return self._parts == other._parts
        
    def __repr__(self):
        return repr(self._parts.values())

    def __hash__(self):
        return hash(self._parts)

class DateTime(Unit):
    is_domain = True


@complex
class Duration(ScaleUnit):
    is_domain = True


@unit("number")
class Number(Unit):
    is_domain = True

    def __str__(self):
        return pretty_float(self.value)

    def __add__(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value)
        else:
            return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value)
        else:
            return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value)
        else:
            return NotImplemented

    def __div__(self, other):
        if isinstance(other, Number):
            return Number(self.value / float(other.value))
        else:
            return NotImplemented

    def __eq__(self, other):
        return isinstance(other, Number) and self.value == other.value


@unit("millisecond", "milliseconds", "ms")
class Millis(Duration):
    multiplicator = 1


@unit("second", "seconds", "s")
class Second(Millis):
    multiplicator = 1000


@unit("minute", "minutes", "m")
class Minute(Second):
    multiplicator = 60


@unit("hours", "hour", "h")
class Hour(Minute):
    multiplicator = 60


@unit("day", "days", "d")
class Day(Hour):
    multiplicator = 24


@unit("week", "weeks", "w")
class Week(Day):
    multiplicator = 7


@unit("month", "months", "m")
class Month(Duration):
    weight = 2

@unit("year", "years", "y")
class Year(Duration):
    weight = 3


if __name__ == '__main__':
    a = Day()
    print(a.k())
    d = Atom(2, Day())
    ms = Atom(1000 * 60, Millis())
    print(d, ms)
