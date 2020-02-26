#!/usr/bin/env python
# -*- coding:utf-8 -*-


from unittest import mock
import unittest
from module import Count


class MockDemo(unittest.TestCase):

    def test_add(self):
        count = Count()
        count.add = mock.Mock(return_value=13, side_effect=count.add)
        result = count.add(8, 8)
        print(result)
        count.add.assert_called_with(8, 8)
        self.assertEqual(result, 16)


if __name__ == '__main__':
    unittest.main()


# 运行命令： python3 1.0_测试用例.py


"""
count.add = mock.Mock(return_value=13, side_effect=count.add)

side_effect参数和return_value是相反的。它给mock分配了可替换的结果，覆盖了return_value。
简单的说，一个模拟工厂调用将返回side_effect值，而不是return_value。

所以，设置side_effect参数为Count类add()方法，那么return_value的作用失效。

"""