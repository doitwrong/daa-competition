__author__ = 'kaloyan'
import unittest
import os
from importlib.machinery import SourceFileLoader

'''
param_test = SourceFileLoader("module.name", os.path.join(os.path.dirname(__file__),
                                                          'parametrized_test.py')).load_module()'''

from daacompetition.parametrized_test import ParametrizedTestCase


class JudgeTest(ParametrizedTestCase):

    solution_module = None

    def setUp(self):
        self.solution_module = SourceFileLoader("module.name", os.path.join(os.path.dirname(__file__),
                                                                            'solutions/',
                                                                            self.param + '.py')).load_module()

    def test_something(self):
        self.assertEqual(5, self.solution_module.solution(2))

