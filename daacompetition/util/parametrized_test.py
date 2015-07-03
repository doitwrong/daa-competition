__author__ = 'kaloyan'
import unittest


class ParametrizedTestCase(unittest.TestCase):
    """ TestCase classovete tryabva da nasledyavat tozi
    """
    def __init__(self, method_name='runTest', param=None):
        super(ParametrizedTestCase, self).__init__(method_name)
        self.param = param

    @staticmethod
    def parametrize(testcase_klass, param=None):
        """ Sazdavam suite sadarjasht vsichki testove ot given
            subclass, podavaiki im 'param'.
        """
        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(testcase_klass)
        suite = unittest.TestSuite()
        for name in testnames:
            suite.addTest(testcase_klass(name, param=param))
        return suite
