#!/usr/bin/env python3
#encoding=utf
from unittest import TestCase, skip, main
from parser import Calculator, Result
from datetime import datetime, timedelta

@skip
class TestRussian(TestCase):

  def setUp(self):
    self.calc = Calculator()

  def test_unit(self):
    self.assertEqual(Result(day=1), self.calc.eval("1 день"))

class Test(TestCase):

  def setUp(self):
    self.calc = Calculator()

if __name__ == '__main__':
  main()