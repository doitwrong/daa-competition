import unittest

from pyramid import testing


class CommonTests(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_login(self):
        # TODO toya test ne raboti

        # from .views import my_view
        # request = testing.DummyRequest()
        # info = my_view(request)
        # self.assertEqual(info['project'], 'daa-competition')
        from .views import login
        request = testing.DummyRequest()
        request.params['login'] = 'student'
        request.params['password'] = 'student'

        # request.route_url()
        # request.route_url('login') = 'http://localhost:6543/login'
        print("CCCCCC")
        print(login(request))
