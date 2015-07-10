__author__ = 'kaloyan'
import unittest
import os
from importlib.machinery import SourceFileLoader
from daacompetition.util.parametrized_test import ParametrizedTestCase
from daacompetition.util.custom_decorators import timeout

class JudgeTest(ParametrizedTestCase):
    '''trybva testovete da ima suffix za da razbera koi test e gramnal '''

    solution_module = None

    def setUp(self):
        self.solution_module = SourceFileLoader("module.name", os.path.join(os.path.dirname(__file__),
                                                                            'solutions/',
                                                                            self.param + '.py')).load_module()

    @timeout(0.5)
    def test_something_0(self):
        self.assertEqual(4, self.solution_module.solution(8))

    @timeout(1)
    def test_something_1(self):
        self.assertEqual(2, self.solution_module.solution(4))
