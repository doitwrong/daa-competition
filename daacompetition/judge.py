__author__ = 'kaloyan'
import unittest
from io import StringIO
import os
from importlib.machinery import SourceFileLoader
from daacompetition.data.generic_tests import JudgeTest
from daacompetition.util.parametrized_test import ParametrizedTestCase
from daacompetition.exceptions import TimeoutError

class Judge:
    JUDGING = "judging..."
    OK = "ok"
    WA = "wa"
    CE = "ce"
    TL = "tl"

    def get_method_index(self, param):
        return str(param).split(' ')[0].split('_')[-1]

    def run(self, username):
        '''podavash mu username-a i izplanyava code-a ot modula za tozi username'''
        from pprint import pprint
        stream = StringIO()
        runner = unittest.TextTestRunner(stream=stream)
        suite = unittest.TestSuite()
        suite.addTest(ParametrizedTestCase.parametrize(JudgeTest, param=username))
        result = runner.run(suite)
        print('Tests run ', result.testsRun)

        # ako ima greshki znachi ili ima compilacionna greshka ili bavno reshenieto
        for v in result.errors:
            test_index = self.get_method_index(v[0])
            cause = ""
            if TimeoutError.__name__ in v[1]:
                cause = self.TL
            else:
                cause = self.CE
            print(test_index, cause)

        for v in result.failures:
            test_index = self.get_method_index(v[0])
            print('FAILURE:', test_index)

        # pprint(result.failures)
        stream.seek(0)
        # print('Test output---------------------\n', stream.read())
        fn = os.path.join(os.path.dirname(__file__), 'data/test_results/'+username)
        file_lines = []
        with open(fn, 'r') as f:
            file_lines = f.readlines()
        filtered = [v for v in file_lines if v != self.JUDGING]

        # print(runner.descriptions)

        f = open(fn, 'w')
        f.write(''.join(filtered))
