from unittest import TestCase, main
from alfred_date_calc.parser import Parser


def eval(text):
    parser = Parser()
    tree = parser.parse(text)
    return str(tree.eval())


class NumberOperations(TestCase):
    def test_number(self):
        self.assertEquals(eval("13"), "13")

    def test_float(self):
        self.assertEquals(eval("7.0"), "1")
        self.assertEquals(eval("-12.0"), "-12")

    def test_negative(self):
        self.assertEquals(eval("-14"), "-14")

    def test_braces(self):
        self.assertEquals(eval("(42)"), "42")

    def test_braces_negative(self):
        self.assertEquals(eval("(-42)"), "-42")
        self.assertEquals(eval("-(42)"), "-42")
        self.assertEquals(eval("-(-42)"), "42")

    def test_negative_float(self):
        self.assertEquals(eval("-14.7"), "-14.7")

    def test_float(self):
        self.assertEquals(eval("11.2"), "11.2")

    def test_add(self):
        self.assertEquals(eval("3.1 + 9.3"), "12.4")

    def test_add_negative(self):
        self.assertEquals(eval("-0.15 + 19"), "18.85")

    def test_add_sequence(self):
        self.assertEquals(eval("3.1 + 9.3 + 123.456"), "135.856")

    def test_sub(self):
        self.assertEquals(eval("14.6 - 12.4"), "2.2")

    def test_mul(self):
        self.assertEquals(eval("6 * 8"), "48")
        self.assertEquals(eval("6 * 8 * 3"), "144")
        self.assertEquals(eval("6.2 * 4.1"), "25.42")
        self.assertEquals(eval("6 * 4.1"), "24.6")
        self.assertEquals(eval("39.0625 * 2.56"), "100")
        self.assertEquals(eval("3 * (-2)"), "-6")

    def test_div(self):
        self.assertEquals(eval("10 / 2"), "5")
        self.assertEquals(eval("10 / 4"), "2.5")
        self.assertEquals(eval("10 / 2.5"), "4")
        self.assertAlmostEquals(float(eval("1 / 3")), 1 / 3.0, 5)


if __name__ == '__main__':
    main()
