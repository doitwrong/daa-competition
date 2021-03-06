from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from daacompetition.security import groupfinder


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    authn_policy = AuthTktAuthenticationPolicy(
        'sosecret', callback=groupfinder, hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()	
    config = Configurator(settings=settings,
                          root_factory='daacompetition.models.RootFactory')
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('viewtests', '/')
    config.add_route('submittask', '/submittask')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('leaderboard', '/leaderboard')
    config.add_route('register', '/register')
    config.scan()
    return config.make_wsgi_app()
