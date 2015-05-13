from pyramid.security import (
    Allow,
    Everyone,
    )


class RootFactory(object):
    __acl__ = [ (Allow, Everyone, 'view'),
                (Allow, 'group:students', 'student') ]
    def __init__(self, request):
        pass

