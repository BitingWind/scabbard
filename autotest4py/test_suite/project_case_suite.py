# encoding: utf-8
import unittest

from projects.project.test_case.type_case.case_collection_1 import CaseClass1
from projects.project.test_case.type_case.case_collection_2 import CaseClass2


def pack_suite():
    suiteTest = unittest.TestSuite()

    # ------------已经跑通的case：-----------------------

    # 单个case添加
    suiteTest.addTest(CaseClass1("test_1"))

    # 整体case集添加
    suiteTest.addTest(unittest.TestLoader().loadTestsFromTestCase(CaseClass2))

    return suiteTest


