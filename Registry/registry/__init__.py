from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.security import Allow, forget, remember

class HelloFactory(object):
    def __init__(self, request):
        self.__acl__ = [
            (Allow, 'vasya', 'view'),
            (Allow, 'group:editors', 'add'),
            (Allow, 'group:editors', 'edit'),
        ]

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    authn_policy = AuthTktAuthenticationPolicy('seekrit', hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.include('pyramid_jinja2')
    config.include('.models')
    config.include('.routes')
    config.scan()
    return config.make_wsgi_app()

