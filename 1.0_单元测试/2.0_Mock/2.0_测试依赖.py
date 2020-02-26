#!/usr/bin/env python
# -*- coding:utf-8 -*-


import unittest
import function


class MyTestCase(unittest.TestCase):

    def test_add_and_multiply(self):
        x = 3
        y = 5
        addition, multiple = function.add_and_multiply(x, y)
        self.assertEqual(8, addition)
        self.assertEqual(15, multiple)


if __name__ == "__main__":
    unittest.main()


# 运行命令： python3 2.0_测试依赖.py
