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

    @timeout(2)
    def test_something_1(self):
        self.assertEqual(5, self.solution_module.solution(2))

    def test_kor(self):
        print('dasdas')
