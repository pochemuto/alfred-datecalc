from parser import Parser
from unittest import TestCase, main

def eval(text):
    parser = Parser()
    tree = parser.parse(text)
    return str(tree.eval())

class NumberOperations(TestCase):
    def test_number(self):
        self.assertEquals(eval("13"), "13")

    def test_negative(self):
        self.assertEquals(eval("-14"), "-14")
        
    def test_negative_float(self):
        self.assertEquals(eval("-14.7"), "-14.7")

    def test_float(self):
        self.assertEquals(eval("11.2"), "11.2")

    def test_add(self):
        self.assertEquals(eval("3.1 + 9.3"), "12.4")

    def test_add_sequence(self):
        self.assertEquals(eval("3.1 + 9.3 + 123.456"), "135.856")

    def test_sub(self):
        self.assertEquals(eval("14.6 - 12.4"), "2.2")

if __name__ == '__main__':
    main()