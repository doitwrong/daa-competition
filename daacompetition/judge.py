__author__ = 'kaloyan'
import unittest
from io import StringIO
import os
from daacompetition.data.generic_tests import JudgeTest
from daacompetition.util.parametrized_test import ParametrizedTestCase
from daacompetition.exceptions import TimeoutError
import time


class Judge:
    JUDGING = "judging..."
    OK = "ok"
    WA = "wa"
    CE = "ce"
    TL = "tl"

    def get_method_index(self, param):
        return int(str(param).split(' ')[0].split('_')[-1])

    def run(self, username):
        '''podavash mu username-a i izplanyava code-a ot modula za tozi username'''
        from pprint import pprint
        stream = StringIO()
        runner = unittest.TextTestRunner(stream=stream)
        suite = unittest.TestSuite()
        suite.addTest(ParametrizedTestCase.parametrize(JudgeTest, param=username))
        result = runner.run(suite)
        print('Tests run ', result.testsRun)

        test_results = []
        for v in range(result.testsRun):
            test_results.append(self.OK)

        # ako ima greshki znachi ili ima compilacionna greshka ili bavno reshenieto
        for v in result.errors:
            test_index = self.get_method_index(v[0])
            cause = ""
            if TimeoutError.__name__ in v[1]:
                cause = self.TL
            else:
                cause = self.CE
            test_results[test_index] = cause

        for v in result.failures:
            test_index = self.get_method_index(v[0])
            test_results[test_index] = self.WA

        # pprint(result.failures)
        stream.seek(0)
        # print('Test output---------------------\n', stream.read())
        fn = os.path.join(os.path.dirname(__file__), 'data/test_results/'+username)
        file_lines = []
        with open(fn, 'r') as f:
            file_lines = f.readlines()
        filtered = [v for v in file_lines if v != self.JUDGING]

        str_to_append = " ".join(test_results)

        # ako tekushtiya rezultat e po-malak ot noviya go update-vame
        number_of_oks = str_to_append.count(self.OK)
        if int(filtered[0]) < number_of_oks:
            filtered[0] = str(number_of_oks)+"\n"

        f = open(fn, 'w')
        filtered.append(str_to_append)
        f.write(''.join(filtered))

        # TUKA POLZVAM os.access koeto mai samo za unix raboti
        progress = ''
        if 1 < len(filtered):
            progress = str(int(100 / (filtered[1].count(' ')+1) * int(filtered[0])))
            fn = os.path.join(os.path.dirname(__file__), 'data/leaderboard')
            time_to_sleep = 0.5
            while not os.access(fn, os.R_OK | os.W_OK):
                time.sleep(time_to_sleep)
            # f = open(fn, os.R_OK | os.W_OK)
            f = open(fn, 'w+')
            lines = f.readlines()
            d = {}
            for line in lines:
                (key, val) = line.split(' ')
                d[key] = val

            d[username] = progress+"%\n"
            new_list = []
            for key, value in d.items():
                new_list.append(key+" "+value)

            f.write(''.join(new_list))
