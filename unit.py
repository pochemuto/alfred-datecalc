# coding=utf
from ast import Unit, Atom

units_names = {}


class unit:
    def __init__(self, *names):
        self.names = names

    def __call__(self, cls):
        cls.names = self.names
        for name in self.names:
            units_names[name] = cls

        def init(self, value):
            self.value = value

        cls.__init__ = init
        return cls


class ScaleUnit(Unit):
    multiplicator = 1
    
    def __add__(self, other):
        if not self._compatible_with(other):
            raise ArithmeticError("Cannot add {1} to {0}, {2} + {3}".format(self, other, self.domain(), other.domain()))
        
        smaller, bigger, k = self._order_arguments(other)
        return smaller.__class__(bigger.value * k + smaller.value)

    def __sub__(self, other):
        if not self._compatible_with(other):
            raise ArithmeticError("Cannot subtract {1} from {0}, {2} + {3}".format(self, other, self.domain(), other.domain()))

        smaller, bigger, k = self._order_arguments(other)
        sign = -1 if smaller == self else 1
        return smaller.__class__((bigger.value * k - smaller.value) * sign)

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
        cls = self.__class__
        while True:
            base = cls.__base__
            if not base.is_domain:
                break

            cls = base
        return cls

    def k(self):
        cls = self.__class__
        k = 1
        while cls != ScaleUnit:
            k *= cls.multiplicator
            cls = cls.__base__
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
    d = Atom(2, Day())
    ms = Atom(1000 * 60, Millis())
    print(d, ms)
