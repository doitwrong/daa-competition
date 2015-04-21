from pyramid.view import view_config

from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound,
    )

@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'project': 'daa-competition'}


@view_config(route_name='submit', renderer='templates/submittask.pt')
def submit(request):
    pagename = 'submit'
    edit_url = request.route_url('submit', pagename=pagename)
    content='dasdasdasd'
    return dict(pagename=pagename, content=content, edit_url=edit_url)


