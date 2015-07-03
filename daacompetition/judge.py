__author__ = 'kaloyan'
import unittest
from io import StringIO
import os
from importlib.machinery import SourceFileLoader

judge = SourceFileLoader("module.name", os.path.join(os.path.dirname(__file__),
                                                     'data/generic_tests.py')).load_module()

param_test = SourceFileLoader("module.name", os.path.join(os.path.dirname(__file__),
                                                          'util/parametrized_test.py')).load_module()

class Judge:
    def run(self):
        from pprint import pprint
        stream = StringIO()
        runner = unittest.TextTestRunner(stream=stream)
        suite = unittest.TestSuite()
        suite.addTest(param_test.ParametrizedTestCase.parametrize(judge.JudgeTest, param=42333))
        '''result = runner.run(unittest.makeSuite(judge.JudgeTest))'''
        result = runner.run(suite)
        print('Tests run ', result.testsRun)
        print('Errors ', result.errors)
        pprint(result.failures)
        stream.seek(0)
        print('Test output\n', stream.read())

var = Judge()
var.run()
