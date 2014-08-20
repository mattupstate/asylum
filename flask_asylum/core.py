# -*- coding: utf-8 -*-
"""
    flask_asylum.core
    ~~~~~~~~~~~~~~~~~

    Core Flask-Asylum package
"""

from flask import g
from werkzeug.local import LocalProxy

current_identity = LocalProxy(lambda: g._current_identity)


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

    def __init__(self, app=None, identity_policy=None):
        self.app = app
        self._identity_policy = identity_policy
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
        g._current_identity = None

    @property
    def identity_policy(self):
        return self._identity_policy

    @identity_policy.setter
    def identity_policy(self, value):
        self._identity_policy = value

    def _before_request(self):
        self._set_identity(self.identity_policy.identify())

    def _after_request(self, response):
        if g._current_identity:
            self._identity_policy.remember(response, g._current_identity)
        else:
            self._identity_policy.forget(response)
        return response

    def _set_identity(self, identity):
        try:
            user_id, _ = identity
        except ValueError:
            identity = (identity, None)
        except TypeError:
            identity = None
        g._current_identity = identity

