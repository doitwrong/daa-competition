import unittest

from pyramid import testing
from daacompetition.exceptions import SubmitTaskFailure
from daacompetition.constants import Register, Login
import os
import time

from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound,
    )


class ViewIntegrationTests(unittest.TestCase):
    ''' tova sa unit testove za python code-a samo za code
    (ne i za testove po resheniyata) tova tuka polzva mock obekti
    za se narichat integration
    '''

    @classmethod
    def setUpClass(cls):
        fn = os.path.join(os.path.dirname(__file__), 'data/test_results/student')
        with open(fn, 'r') as f:
            cls.results_data = f.read()

        fn = os.path.join(os.path.dirname(__file__), 'data/solutions/student.py')
        with open(fn, 'r') as f:
            cls.solution_data = f.read()

        fn = os.path.join(os.path.dirname(__file__), 'data/leaderboard')
        with open(fn, 'r') as f:
            cls.leaderboard_data = f.read()

    @classmethod
    def tearDownClass(cls):
        time.sleep(1)
        fn = os.path.join(os.path.dirname(__file__), 'data/test_results/student')
        with open(fn, 'w') as f:
            f.write(cls.results_data)

        fn = os.path.join(os.path.dirname(__file__), 'data/solutions/student.py')
        with open(fn, 'w') as f:
            f.write(cls.solution_data)

        fn = os.path.join(os.path.dirname(__file__), 'data/leaderboard')
        with open(fn, 'w') as f:
            f.write(cls.leaderboard_data)

    def setUp(self):
        self.config = testing.setUp()
        self.config.add_route("login", "http://localhost:6543/login")
        self.config.add_route("register", "http://localhost:6543/register")
        self.config.add_route("viewtests", "http://localhost:6543/viewtests")
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

    def test_bad_login(self):
        from .views import login
        request = testing.DummyRequest({'form.submitted': True})
        request.params['login'] = 'student'
        request.params['password'] = 'student1'
        self.assertEqual(login(request)['message'], Login.LOGIN_FAILED.value)

    def test_submit_before(self):
        '''dali shte vdigne greshka ako e predal predi vremetoza iztichane'''
        from .views import submit_task
        fake_conf = 'start_date|Jul 7 2015  9:30AM\nduration|3\n'
        original_conf = 'start_date|Jul 7 2015  9:30AM\nduration|300\n'
        fn = os.path.join(os.path.dirname(__file__), 'data/configuration')
        with open(fn, 'w') as f:
            f.write(fake_conf)
        request = testing.DummyRequest()
        with self.assertRaises(SubmitTaskFailure):
            submit_task(request)
        with open(fn, 'w') as f:
            f.write(original_conf)

    def test_catch_mischievous_input(self):
        test_code = "import subprocess\n" \
                    "def solution(da_set):\n" \
                    "    subprocess.call('ls', shell=True)\n" \
                    "        return da_set/2"
        from .views import submit_task
        request = testing.DummyRequest({'form.submitted': True})
        request.params['solution'] = test_code
        with self.assertRaises(SubmitTaskFailure):
            submit_task(request)

    def test_good_input(self):
        test_code = "def solution(da_set):\n" \
                    "    return da_set/2"
        from .views import submit_task
        request = testing.DummyRequest({'form.submitted': True})
        request.params['solution'] = test_code
        self.assertEqual(submit_task(request).status, '302 Found')

    def test_reg_empty_field(self):
        from .views import register
        request = testing.DummyRequest({'form.submitted': True})
        request.params['username'] = None
        request.params['password'] = 'dsadas'
        request.params['repassword'] = None
        self.assertEqual(register(request)['message'], Register.ALL_FIELDS_REQ.value)

    def test_reg_username_exists(self):
        from .views import register
        request = testing.DummyRequest({'form.submitted': True})
        request.params['username'] = "student"
        request.params['password'] = 'dsadas'
        request.params['repassword'] = "dsadas"
        self.assertEqual(register(request)['message'], Register.USERNAME_EXISTS.value)

    def test_reg_pass_not_match(self):
        from .views import register
        request = testing.DummyRequest({'form.submitted': True})
        request.params['username'] = "student"
        request.params['password'] = 'dsadas1'
        request.params['repassword'] = "dsadas"
        self.assertEqual(register(request)['message'], Register.PASSWORDS_NOT_MATCH.value)

    def test_reg_bad_characters(self):
        from .views import register
        request = testing.DummyRequest({'form.submitted': True})
        request.params['username'] = "student#"
        request.params['password'] = 'dsadas'
        request.params['repassword'] = "dsadas"
        self.assertEqual(register(request)['message'], Register.ALLOWED_CHARACTERS.value)

    def test_submit_empty(self):
        from .views import submit_task
        request = testing.DummyRequest({'form.submitted': True})
        request.params['solution'] = None
        with self.assertRaises(SubmitTaskFailure):
            submit_task(request)

    def test_add_new_solution(self):
        from .views import view_tests, submit_task
        request = testing.DummyRequest()
        reponse = view_tests(request)
        old_number_of_results = len(reponse['results'])
        test_code = "def solution(da_set):\n" \
                    "    return da_set/2"
        request = testing.DummyRequest({'form.submitted': True})
        request.params['solution'] = test_code
        submit_task(request)
        request = testing.DummyRequest()
        reponse = view_tests(request)
        new_number_of_results = len(reponse['results'])
        self.assertNotEqual(old_number_of_results, new_number_of_results)


class FunctionalTests(unittest.TestCase):
    def setUp(self):
        from daacompetition import main
        app = main({})
        from webtest import TestApp
        self.testapp = TestApp(app)

    def test_root(self):
        res = self.testapp.get('/leaderboard', status=200)
        self.assertEqual(res.body.decode("utf-8").count('<title>LEADERBOARD</title>'), 1)

    def test_not_loggged(self):
        res = self.testapp.get("/")
        self.assertEqual(res.body.decode("utf-8").count('<title>DAA COMPETITION LOGIN</title>'), 1)
