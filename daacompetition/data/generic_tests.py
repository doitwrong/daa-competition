__author__ = 'kaloyan'
import unittest
import os
from importlib.machinery import SourceFileLoader


param_test = SourceFileLoader("module.name", os.path.join(os.path.dirname(__file__),
                                                          '../util/parametrized_test.py')).load_module()


class JudgeTest(param_test.ParametrizedTestCase):

    def test_something(self):
        print(self.param)
        assert True
