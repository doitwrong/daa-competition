__author__ = 'kaloyan'
import unittest
import os
from importlib.machinery import SourceFileLoader

'''
param_test = SourceFileLoader("module.name", os.path.join(os.path.dirname(__file__),
                                                          'parametrized_test.py')).load_module()'''

from daacompetition.parametrized_test import ParametrizedTestCase


class JudgeTest(ParametrizedTestCase):

    def test_something(self):
        print(self.param)
        assert True
