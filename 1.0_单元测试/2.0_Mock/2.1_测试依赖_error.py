#!/usr/bin/env python
# -*- coding:utf-8 -*-


import unittest
import function_change


class MyTestCase(unittest.TestCase):

    def test_add_and_multiply(self):
        x = 3
        y = 5
        addition, multiple = function_change.add_and_multiply(x, y)
        self.assertEqual(8, addition)
        self.assertEqual(15, multiple)


if __name__ == "__main__":
    unittest.main()


"""
F
======================================================================
FAIL: test_add_and_multiply (__main__.MyTestCase)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "2.1_测试依赖_error.py", line 16, in test_add_and_multiply
    self.assertEqual(15, multiple)
AssertionError: 15 != 16

----------------------------------------------------------------------
Ran 1 test in 0.001s

FAILED (failures=1)
"""


"""
测试用例运行失败了，然而，add_and_multiply()函数以及它的测试用例并没有做任何修改，
罪魁祸首是multiply()函数引起的，我们应该把 multiply()函数mock掉。
"""