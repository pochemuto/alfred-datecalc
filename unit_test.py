#!/usr/bin/env python3
# encoding=utf
from unittest import TestCase, main

from unit import *


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

    def test_my(self):
        t = Week(1) + Day(5)
        print(t)
        
if __name__ == '__main__':
    main()
