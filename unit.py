# coding=utf
from __future__ import print_function
from ast import Unit, Atom
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


def select_unit(name):
    if name in units_names:
        return units_names[name]
    else:
        raise UndefinedUnitException(name)


class UndefinedUnitException(Exception):
    def __init__(self, unit_definition):
        super().__init__("Unknown unit definition: '{}'".format(unit_definition))
        

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

    def _order_arguments(self, other):
        smaller, bigger = sorted((self, other), key=lambda item: item.k())
        k = int(bigger.k() / smaller.k())
        return smaller, bigger, k

    def _compatible_with(self, other):
        return self.domain() == other.domain()

    def raw(self):
        return self.value * self.k()

    def _same_domain(self, other):
        return self.domain() == other.domain()

    def domain(self):
        domain = self.__class__
        for cls in getmro(self.__class__):
            if cls.is_domain:
                domain = cls
            else:
                break
        return domain

    def k(self):
        k = 1
        for cls in getmro(self.__class__):
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


class DateTime(Unit):
    is_domain = True


class Duration(ScaleUnit):
    is_domain = True


@unit()
class Number(ScaleUnit):
    is_domain = True


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
class Month(Millis):
    pass


@unit("year", "years", "y")
class Year(Millis):
    pass


if __name__ == '__main__':
    a = Day()
    print(a.k())
    d = Atom(2, Day())
    ms = Atom(1000 * 60, Millis())
    print(d, ms)
