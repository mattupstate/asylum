# -*- coding: utf-8 -*-
"""
    flask_asylum.authn
    ~~~~~~~~~~~~~~~~~~

    Stock authentication providers
"""

from .core import Authentication


class AuthenticationProvider(object):

    def authenticate(self, authentication):
        raise NotImplementedError


class CollectionAuthenticationProvider(object):

    def __init__(self, collection):
        self._collection = collection

    def authenticate(self, identity):
        if identity.uid in self._collection:
            identity = Authentication(identity.uid, identity.credentials, True, None)
        return identity
