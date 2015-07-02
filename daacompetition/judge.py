__author__ = 'kaloyan'
from unittest.case import TestCase
import unittest
from io import StringIO
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'data'))


class Judge:
    def run(self):
        stream = StringIO()
        print('KORO')

var = Judge()
var.run()
