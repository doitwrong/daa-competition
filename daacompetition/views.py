__author__ = 'kaloyan'
from pyramid.view import view_config
import os
from .security import USERS
from daacompetition.judge import Judge
from daacompetition.data.judge_configuration import TimeConfiguration
from daacompetition.exceptions import SubmitTaskFailure
from pyramid.response import Response
from datetime import datetime

from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound,
    )

from pyramid.view import (
    view_config,
    forbidden_view_config,
    )

from pyramid.security import (
    remember,
    forget,
    )


@view_config(route_name='viewtests', renderer='templates/viewtests.pt',
             permission='student')
def view_tests(request):
    """ logika ot pregleda na test rezultatite ot tekushtoto sastezanie """
    username = "<b>" + request.authenticated_userid + "</b>"
    pagename = 'submit'
    edit_url = request.route_url('viewtests', pagename=pagename)
    fn = os.path.join(os.path.dirname(__file__), 'data/test_results/'+request.authenticated_userid)
    results = []
    with open(fn, 'r') as f:
        results = f.readlines()

    return dict(pagename=pagename,
                results=results,
                edit_url=edit_url,
                username=username,
                logged_in=request.authenticated_userid)


@view_config(route_name='submittask', renderer='templates/submittask.pt',
             permission='student')
def submit_task(request):
    """ logika predavane na zadacha """
    if datetime.now() > TimeConfiguration.expires:
        raise SubmitTaskFailure('MINA VREMETO ZA PREDAVENE')

    pagename = 'SUBMIT TASK'
    referrer = request.url
    came_from = request.params.get('came_from', referrer)
    solution = ''
    if 'form.submitted' in request.params:
        fn = os.path.join(os.path.dirname(__file__), 'data/solutions/'+request.authenticated_userid+'.py')
        f = open(fn, 'w')
        f.write(request.params['solution'])
        f.close()
        judge = Judge()
        judge.run(request.authenticated_userid)  # request.params['solution']
        url = request.application_url
        return HTTPFound(location=url)

    return dict(pagename=pagename,
                came_from=came_from,
                url=request.application_url + '/submittask',
                solution=solution,
                logged_in=request.authenticated_userid)


@view_config(route_name='login', renderer='templates/login.pt')
@forbidden_view_config(renderer='templates/login.pt')
def login(request):
    print("LOGIN")
    login_url = request.route_url('login')
    referrer = request.url
    if referrer == login_url:
        referrer = '/'  # never use the login form itself as came_from
    came_from = request.params.get('came_from', referrer)
    message = ''
    login = ''
    password = ''
    if 'form.submitted' in request.params:
        login = request.params['login']
        password = request.params['password']
        if USERS.get(login) == password:
            headers = remember(request, login)
            return HTTPFound(location=came_from,
                             headers=headers)
        message = 'Failed login'

    return dict(
        message=message,
        url=request.application_url + '/login',
        came_from=came_from,
        login=login,
        password=password,
        )


@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(location=request.route_url('submit'),
                     headers=headers)


@view_config(context=SubmitTaskFailure)
def failed_submit(exc, request):
    response = Response('Failed validation: %s' % exc.msg)
    response.status_int = 500
    return response
