__author__ = 'kaloyan'
from pyramid.view import view_config
import os
from .security import get_users
from daacompetition.judge import Judge
from daacompetition.data.judge_configuration import TimeConfiguration
from .exceptions import DAAException, SubmitTaskFailure
from pyramid.response import Response
from datetime import datetime
import threading
import re
from daacompetition.constants import Register, Login, SubmtiTask

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
    username = "<b>" + request.authenticated_userid + "</b>"  # tova ne hubavo no sam slojil ako mi se naloji da vidya
    pagename = 'submit'
    edit_url = request.route_url('viewtests', pagename=pagename)
    fn = os.path.join(os.path.dirname(__file__), 'data/test_results/' + request.authenticated_userid)
    results = []
    with open(fn, 'r') as f:
        results = f.readlines()

    progress = ''
    if 1 < len(results):
        progress = str(int(100 / (results[1].count(' ') + 1) * int(results[0])))
    else:
        progress = "0"

    return dict(pagename=pagename,
                results=results[1:],
                edit_url=edit_url,
                username=username,
                logged_in=request.authenticated_userid,
                progress=progress)


@view_config(route_name='submittask', renderer='templates/submittask.pt',
             permission='student')
def submit_task(request):
    """ logika predavane na zadacha """
    if datetime.now() > TimeConfiguration().expires:
        raise SubmitTaskFailure(SubmtiTask.TIME_EXPIRES.value)

    blacklisted = [r'\bsubprocess|eval|system\b.*\(', r'exec']

    pagename = 'SUBMIT TASK'
    referrer = request.url
    came_from = request.params.get('came_from', referrer)
    solution = ''
    if 'form.submitted' in request.params:
        raw_input = request.params['solution']
        for v in blacklisted:
            # raw_input = re.sub(v, '', raw_input)
            matched = re.search(v, raw_input)
            if matched:
                raise SubmitTaskFailure(SubmtiTask.MISCHIEVOUS_CODE.value+': ' + matched.group(0))

        fn = os.path.join(os.path.dirname(__file__), 'data/solutions/' + request.authenticated_userid + '.py')
        with open(fn, 'w') as f:
            f.write(raw_input)
        # appendvam judging preda da se izvikat testovete
        fn = os.path.join(os.path.dirname(__file__), 'data/test_results/' + request.authenticated_userid)
        with open(fn, 'a') as f:
            f.write('\n' + Judge.JUDGING)
        # puskam v thread test suite-a mi
        judge = Judge()
        thread = threading.Thread(target=judge.run, args=(request.authenticated_userid,))
        thread.start()
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
        if get_users().get(login) == password:
            headers = remember(request, login)
            return HTTPFound(location=came_from,
                             headers=headers)
        message = Login.LOGIN_FAILED.value

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


@view_config(context=DAAException)
def exception_handler(exc, request):
    response = Response('Caught exception: %s' % exc.msg)
    response.status_int = 500
    return response


@view_config(route_name='leaderboard', renderer='templates/leaderboard.pt')
def leaderboard(request):
    fn = os.path.join(os.path.dirname(__file__), 'data/leaderboard')
    results = []
    with open(fn, 'r') as f:
        results = f.readlines()
    return dict(results=results,
                )


STUDENTS_GROUP = "group:students"


@view_config(route_name='register', renderer='templates/register.pt')
def register(request):
    register_url = request.route_url('register')
    came_from = request.params.get('came_from', register_url)
    register, password, repassword, message, username = ["", "", "", "", ""]

    while True:
        if 'form.submitted' in request.params:

            if not request.params['username'] or \
                    not request.params['password'] or \
                    not request.params['repassword']:
                message = Register.ALL_FIELDS_REQ.value
                break

            if request.params['password'] != request.params['repassword']:
                message = Register.PASSWORDS_NOT_MATCH.value
                break

            if not re.search(r'^[a-z0-9_]+$', request.params['username']):
                message = Register.ALLOWED_CHARACTERS.value
                break

            fn = os.path.join(os.path.dirname(__file__), 'data/users')
            f = open(fn, 'r')
            lines = f.readlines()
            f.close()
            users = {}
            for line in lines:
                (key, val) = line.split(' ')
                users[key] = val

            if request.params['username'] in users:
                message = Register.USERNAME_EXISTS.value
                break

            fn = os.path.join(os.path.dirname(__file__), 'data/users')
            with open(fn, 'a') as f:
                f.write("\n" + request.params['username'] + " "
                        + request.params['password'])

            fn = os.path.join(os.path.dirname(__file__), 'data/leaderboard')
            with open(fn, 'a') as f:
                f.write(request.params['username'] + " 0%")

            fn = os.path.join(os.path.dirname(__file__), 'data/users_permissions')
            with open(fn, 'a') as f:
                f.write("\n" + request.params['username'] + " "
                        + STUDENTS_GROUP)

            with open(os.path.join(os.path.dirname(__file__),
                                   'data/solutions/' + request.params['username'] + '.py'), 'a') as f:
                f.close()

            with open(os.path.join(os.path.dirname(__file__),
                                   'data/test_results/' + request.params['username']), 'a') as f:
                f.write("0")

        break

    return dict(message=message,
                url=request.application_url + '/register',
                came_from=came_from,
                register=register,
                password=password,
                repassword=repassword,
                username=username,
                )
