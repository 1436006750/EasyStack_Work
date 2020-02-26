#!/usr/bin/env python
# -*- coding:utf-8 -*-


import unittest


class TestStringMethods(unittest.TestCase):
    # 每个测试类继承于unittest.TestCase类

    def setUp(self):
        print('setUp...')
    # 每个testXXX函数运行前会先运行setUp函数

    def tearDown(self):
        print('tearDown...')
    # 每个testXXX函数运行后会运行tearDown函数

    # 每个测试函数必须以test开头,否则不会被当成测试函数
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)


# 使本py文件可以直接$ python test.py执行测试
if __name__ == '__main__':
    unittest.main()



