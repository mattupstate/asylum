# -*- coding: utf-8 -*-
"""
    asylum.core
    ~~~~~~~~~~~

    Core Asylum module
"""

from . import acl


class AuthenticationError(RuntimeError):
    pass


class Authentication(object):

    def __init__(self, identity, credentials=None, authenticated=False, principals=None):
        self._identity = identity
        self._credentials = credentials
        self._authenticated = authenticated
        self._principals = principals

    @property
    def identity(self):
        return self._identity

    @property
    def credentials(self):
        return self._credentials

    @property
    def authenticated(self):
        return self._authenticated

    @property
    def principals(self):
        return self._principals

    def __str__(self):
        return "Authentication(%s, authenticated=%s, principals=%s)" % (
            self.identity, self.authenticated, self.principals)


class AuthenticationProvider(object):

    def authenticate(self, authentication):
        raise NotImplementedError


class IdentityProvider(object):

    def identify(self):
        raise NotImplementedError

    def remember(self):
        raise NotImplementedError

    def forget(self):
        raise NotImplementedError


class AuthorizationProvider(object):

    def can(self, authentication, permission, **kwargs):
        raise NotImplementedError

    def cannot(self, *args, **kwargs):
        return not self.can(*args, **kwargs)


class AsylumContext(object):

    def __init__(self, identity_provider, authn_provider, authz_provider):
        self._identity_provider = identity_provider
        self._authn_provider = authn_provider
        self._authz_provider = authz_provider
        self._authentication = None

    def can(self, permission, **kwargs):
        return self._authz_provider.can(
            self.authentication, permission, **kwargs)

    def cannot(self, *args, **kwargs):
        return not self.can(*args, **kwargs)

    def authenticate(self):
        return self._authn_provider.authenticate(
            self._identity_provider.identify())

    @property
    def authentication(self):
        if self._authentication is None:
            self._authentication = self.authenticate()
        return self._authentication

    # def __enter__(self):
    #     self.authenticate()
    #     return self

    # def __exit__(self, *args):
    #     if self.authentication.authenticated:
    #         self._identity_provider.remember()
    #     else:
    #         self._identity_provider.forget()
