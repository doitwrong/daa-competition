import unittest

from pyramid import testing
from daacompetition.exceptions import SubmitTaskFailure

from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound,
    )


class ViewIntegrationTests(unittest.TestCase):
    ''' tova sa unit testove za python code-a samo za code
    (ne i za testove po resheniyata)
    '''

    def setUp(self):
        self.config = testing.setUp()
        self.config.add_route("login", "http://localhost:6543/login")
        self.config.testing_securitypolicy(userid='student',
                                           permissive=True)

    def tearDown(self):
        testing.tearDown()

    def test_login(self):
        from .views import login
        request = testing.DummyRequest({'form.submitted': True})
        request.params['login'] = 'student'
        request.params['password'] = 'student'
        self.assertEqual(login(request).status, '302 Found')

    def test_submit_before(self):
        '''dali shte vdigne greshka ako e predal predi vremetoza iztichane'''
        from .views import submit_task
        request = testing.DummyRequest()
        # with self.assertRaises(SubmitTaskFailure):
        # submit_task(request)

    def test_catch_mischievous_input(self):
        test_code = "import subprocess\n" \
                    "def solution(da_set):\n" \
                    "    subprocess.call('ls', shell=True)\n" \
                    "        return 5"
        from .views import submit_task
        request = testing.DummyRequest({'form.submitted': True})
        request.params['solution'] = test_code
        with self.assertRaises(SubmitTaskFailure):
            submit_task(request)

    def test_good_input(self):
        test_code = "def solution(da_set):\n" \
                    "    return 5"
        from .views import submit_task
        request = testing.DummyRequest({'form.submitted': True})
        request.params['solution'] = test_code
        print(submit_task(request).status)


class FunctionalTests(unittest.TestCase):
    def setUp(self):
        from daacompetition import main
        app = main({})
        from webtest import TestApp
        self.testapp = TestApp(app)

    def test_root(self):
        res = self.testapp.get('/leaderboard', status=200)
        self.assertEqual(res.body.decode("utf-8").count('<title>LEADERBOARD</title>'), 1)
