from pyramid.view import view_config
import os

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

from .security import USERS


"""
@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'project': 'daa-competition'}
"""

@view_config(route_name='submit', renderer='templates/submittask.pt',
             permission='student')
def submit(request):
    """ logika ot stranicata za predvane na zadachi"""
    print("SUBMIT")
    pagename = 'submit'
    edit_url = request.route_url('submit', pagename=pagename)
    content='<h1> THIS CAME FROM submit() </h1>'
    fn = os.path.join(os.path.dirname(__file__), 'data/users')
    with open(fn , 'r') as f:
        read_data = f.read()
        print(read_data)
    return dict(pagename=pagename,
                content=content,
                edit_url=edit_url, 
                logged_in = request.authenticated_userid )


@view_config(route_name='login', renderer='templates/login.pt')
@forbidden_view_config(renderer='templates/login.pt')
def login(request):
    print("LOGIN")
    login_url = request.route_url('login')
    referrer = request.url
    if referrer == login_url:
        referrer = '/' # never use the login form itself as came_from
    came_from = request.params.get('came_from', referrer)
    message = ''
    login = ''
    password = ''
    if 'form.submitted' in request.params:
        login = request.params['login']
        password = request.params['password']
        if USERS.get(login) == password:
            headers = remember(request, login)
            return HTTPFound(location = came_from,
                             headers = headers)
        message = 'Failed login'

    return dict(
        message = message,
        url = request.application_url + '/login',
        came_from = came_from,
        login = login,
        password = password,
        )

@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(location = request.route_url('submit'),
                     headers = headers)


