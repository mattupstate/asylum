# -*- coding: utf-8 -*-
"""
    flask_asylum.core
    ~~~~~~~~~~~~~~~~~

    Core Flask-Asylum package
"""

from flask import g
from werkzeug.local import LocalProxy
from werkzeug.utils import cached_property

from .identity import Identity

current_identity = LocalProxy(lambda: g._current_identity)
current_authorization_ctx = LocalProxy(lambda: g._current_authorization_ctx)

Everyone = 'Everyone'
Authenticated = 'Authenticated'
Allow = 'Allow'
Deny = 'Deny'


class Asylum(object):
    """The Flask-Asylum extension class provides an API for configuring an application with a
    desired identity policy. Additionally, it provides an API to remember or forget the current
    identity so that it may be retreived later if the identity policy supports it. An "identity"
    as known by Flask-Asylum takes two forms:

    1. A tuple containing a unique user id followed by `None`: ('abc123', None)
    2. A tuple containing a unique user attribute followed by a passphrase: ('joe', 'pazzwerd')

    In the first case the identity has been provided by a trusted mechanism provided by
    Flask-Asylum. Two such examples are a signed cookie or a client session property. In the second
    case the identity has been provided by a client and isn't necessarily trusted.
    """

    def __init__(self, app=None, identity_policy=None, authorization_policy=None):
        self.app = app
        self._identity_policy = identity_policy
        self._authorization_policy = authorization_policy

        if self.app:
            self.init_app(self.app)

    def init_app(self, app):
        app.before_request(self._before_request)
        app.after_request(self._after_request)

    def remember(self, identity):
        """Persist the identity to be loaded on subsequent requests.
        :param identity: The identity of the user
        """
        self._set_identity(identity)

    def forget(self):
        """Invalidate the current identity.
        """
        self._set_identity(None)

    @property
    def identity_policy(self):
        return self._identity_policy

    @identity_policy.setter
    def identity_policy(self, value):
        self._identity_policy = value

    @property
    def authorization_policy(self):
        return self._authorization_policy

    @authorization_policy.setter
    def authorization_policy(self, value):
        self._authorization_policy = value

    def _before_request(self):
        identity = self.identity_policy.identify()
        self._set_identity(identity)

    def _after_request(self, response):
        if g._current_identity:
            self._identity_policy.remember(response, g._current_identity)
        else:
            self._identity_policy.forget(response)
        return response

    def _set_identity(self, identity):
        if identity:
            if isinstance(identity, (list, tuple)):
                credentials = identity[1:]
                if len(credentials) == 1:
                    credentials = credentials[0]
                identity = Identity(identity[:1][0], credentials=credentials)
            else:
                identity = Identity(identity)
        g._current_identity = identity
