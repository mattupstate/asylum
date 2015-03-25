# -*- coding: utf-8 -*-
"""
    flask_asylum.authz
    ~~~~~~~~~~~~~~~~~~

    Stock authorization providers
"""


class AuthorizationProvider(object):
    """An object representing an authorization provider.
    """

    def can(self, identity, permission, **kwargs):
        raise NotImplementedError

    def cannot(self, *args, **kwargs):
        return not self.can(*args, **kwargs)


class MultiAuthorizationProvider(AuthorizationProvider):

    def __init__(self, providers):
        self._providers = providers

    def can(self, identity, permission, **kwargs):
        for provider in self._providers:
            if provider.permits(identity, permission, **kwargs):
                return True
        return False
