#!/usr/bin/env python3
# encoding=utf
from unittest import TestCase, main

from unit import *

class TestToString(TestCase):

    def test_number(self):
        self.assertEquals(str(Number(12)), "12")
        self.assertEquals(str(Number(-12)), "-12")

    def test_number_float(self):
        self.assertEquals(str(Number(float(12))), "12")
        self.assertEquals(str(Number(float(-15))), "-15")

class TestUnitMul(TestCase):

    def test_simple_mul(self):
        self.assertEqual(Number(7) * Number(3), Number(21))

    def test_mul_unit_after(self):
        self.assertEqual(Number(6) * Day(2), Day(12))

    def test_mul_unit_before(self):
        self.assertEqual(Day(2) * Number(3), Day(6))

class TestUnitAdd(TestCase):

    def test_simple_sum(self):
        self.assertEqual(Day(2) + Week(3), Day(3 * 7 + 2))

    def test_simple_sum_false(self):
        self.assertNotEqual(Day(2) + Week(2), Day(3 * 7 + 2))

    def test_add_bigger_first(self):
        self.assertEqual(Week(4) + Day(3), Day(4 * 7 + 3))


class TestUnitSub(TestCase):

    def test_simple_sub(self):
        self.assertEqual(Day(5) - Day(2), Day(3))

    def test_simple_sub_cross_unit(self):
        self.assertEqual(Week(2) - Day(3), Day(11))

    
class TestUnitCore(TestCase):

    def test_k(self):
        self.assertEqual(Day(2).k(), 1000 * 60 * 60 * 24)
        self.assertEqual(Day(42).k(), 1000 * 60 * 60 * 24)

    def test_k_week(self):
        self.assertEqual(Week(42).k(), 1000 * 60 * 60 * 24 * 7)

    def test_raw(self):
        self.assertEqual(Day(3).raw(), 1000 * 60 * 60 * 24 * 3)
        self.assertEqual(Week(42).raw(), 1000 * 60 * 60 * 24 * 7 * 42)

    def test_k_relative(self):
        self.assertEqual(Week(1).k(), Day(1).k() * 7)

    def test_domain(self):
        self.assertEqual(Week(15).domain(), Duration)
        self.assertEqual(Day(15).domain(), Duration)
        self.assertNotEqual(Day(15).domain(), DateTime)

    def test_cast_to_number(self):
        self.assertEqual(Week(4).cast(Number), Number(4))
        self.assertEqual(Hour(3.1415).cast(Number), Number(3.1415))

class TestComplexUnit(TestCase):

    def testEquals(self):
        self.assertEqual(ComplexUnit(), ComplexUnit())
        self.assertEqual(ComplexUnit(Number(4)), ComplexUnit(Number(4)))
        self.assertNotEqual(ComplexUnit(Number(4)), ComplexUnit(Number(8)))
    
    def testSimpleAdd(self):
        self.assertEqual(
            ComplexUnit(Number(4)) + ComplexUnit(Number(8)), 
            ComplexUnit(Number(12))
        )
        self.assertEqual(
            ComplexUnit(Month(1), Day(5)) + ComplexUnit(Month(3), Day(9)), 
            ComplexUnit(Month(4), Day(14))
        )
        self.assertEqual(
            ComplexUnit(Month(1), Day(5)) + ComplexUnit(Month(3), Week(4)), 
            ComplexUnit(Month(4), Day(4 * 7 + 5))
        )
        self.assertEqual(
            ComplexUnit(Month(4), Day(2)) + ComplexUnit(Year(7), Day(3)), 
            ComplexUnit(Year(7), Month(4), Day(5))
        )
    
    def testSimpleSub(self):
        self.assertEqual(
            ComplexUnit(Number(4)) - ComplexUnit(Number(7)), 
            ComplexUnit(Number(-3))
        )
        self.assertEqual(
            ComplexUnit(Month(1), Day(5)) - ComplexUnit(Month(3), Day(9)), 
            ComplexUnit(Month(-2), Day(-4))
        )
        self.assertEqual(
            ComplexUnit(Month(1), Day(5)) - ComplexUnit(Month(3), Week(4)), 
            ComplexUnit(Month(-2), Day(-4 * 7 + 5))
        )
        self.assertEqual(
            ComplexUnit(Month(4), Day(2)) - ComplexUnit(Year(7), Day(3)), 
            ComplexUnit(Year(-7), Month(4), Day(-1))
        )

    def testSimpleMul(self):
        self.assertEqual(
            ComplexUnit(Number(8)) * Number(2),
            ComplexUnit(Number(16))
        )
        self.assertEqual(
            ComplexUnit(Number(8)) * Number(-1),
            ComplexUnit(Number(-8))
        )
        self.assertEqual(
            ComplexUnit(Year(1), Month(2)) * Number(3),
            ComplexUnit(Year(3), Month(6))
        )

    def testSimpleDiv(self):
        self.assertEqual(
            ComplexUnit(Number(7)) / Number(-2),
            ComplexUnit(Number(-3.5))
        )
        self.assertEqual(
            ComplexUnit(Year(9), Month(2)) / Number(3),
            ComplexUnit(Year(3), Month(2/3.0))
        )

    def testMultipleNumberFirst(self):
        self.assertEqual(
            Number(-2) * ComplexUnit(Year(2), Day(7)),
            ComplexUnit(Year(-4), Day(-14))
        )

if __name__ == '__main__':
    main()
