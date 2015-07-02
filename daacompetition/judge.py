__author__ = 'kaloyan'
from unittest.case import TestCase
import unittest
from io import StringIO
import os
import sys
from importlib.machinery import SourceFileLoader


judge = SourceFileLoader("module.name", os.path.join(os.path.dirname(__file__),
                                                     'data/tests/generic_tests.py')).load_module()


class Judge:
    def run(self):
        from pprint import pprint
        stream = StringIO()
        runner = unittest.TextTestRunner(stream=stream)
        result = runner.run(unittest.makeSuite(judge.JudgeTest))
        print('Tests run ', result.testsRun)
        print('Errors ', result.errors)
        pprint(result.failures)
        stream.seek(0)
        print('Test output\n', stream.read())

var = Judge()
var.run()
