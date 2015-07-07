__author__ = 'kaloyan'
import unittest
from io import StringIO
import os
from importlib.machinery import SourceFileLoader
from daacompetition.data.generic_tests import JudgeTest
from daacompetition.util.parametrized_test import ParametrizedTestCase


class Judge:

    def run(self, username):
        '''podavash mu username-a i izplanyava code-a ot modula za tozi username'''
        from pprint import pprint
        stream = StringIO()
        runner = unittest.TextTestRunner(stream=stream)
        suite = unittest.TestSuite()
        suite.addTest(ParametrizedTestCase.parametrize(JudgeTest, param=username))
        '''result = runner.run(unittest.makeSuite(judge.JudgeTest))'''
        result = runner.run(suite)
        print('Tests run ', result.testsRun)
        print('Errors ', result.errors)
        pprint(result.failures)
        stream.seek(0)
        print('Test output\n', stream.read())

