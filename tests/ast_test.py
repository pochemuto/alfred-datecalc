from alfred_date_calc.ast import pretty_float
from unittest import TestCase, main


class TestNumberRepresantetion(TestCase):

    def test_simple(self):
        self.assertEquals(pretty_float(124), "124")
        self.assertEquals(pretty_float(124.123), "124.123")
        self.assertEquals(pretty_float(124.0), "124")


if __name__ == '__main__':
    main()
