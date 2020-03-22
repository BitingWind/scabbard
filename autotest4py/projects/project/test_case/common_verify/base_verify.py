# encoding: utf-8
import unittest


class BaseVerify(unittest.TestCase):
    """ 通用校验 """
    def verify_1(self, param):
        self.assertEqual(1, param)