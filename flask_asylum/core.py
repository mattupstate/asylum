# -*- coding: utf-8 -*-
"""
    flask_asylum.core
    ~~~~~~~~~~~~~~~~~

    Core Flask-Asylum package
"""

from flask import current_app, has_request_context, _request_ctx_stack
from werkzeug.local import LocalProxy

from . import acl

current_identity = LocalProxy(lambda: _get_identity())


def _get_identity():
    if has_request_context() and not hasattr(_request_ctx_stack.top, 'identity'):
        current_app.extensions['asylum']._load_identity()
    return _request_ctx_stack.top.identity


class Authentication(object):

    def __init__(self, uid, credentials=None, authenticated=False, details=None):
        self.uid = uid
        self.credentials = credentials
        self.authenticated = authenticated
        self.details = details

    def __repr__(self):
        return 'Authentication(uid=%r, credentials=%r, authenticated=%r, details=%r)' % (
            self.uid, self.credentials, self.authenticated, self.details)


class Asylum(object):
    """The Flask-Asylum extension class provides an API for configuring an application with a
    desired identity provider. Additionally, it provides an API to remember or forget the current
    identity so that it may be retreived later if the identity provider supports it. An "identity"
    as known by Flask-Asylum takes two forms:

    1. A tuple containing a unique user id followed by `None`: ('abc123', None)
    2. A tuple containing a unique user attribute followed by a passphrase: ('joe', 'pazzwerd')

    In the first case the identity has been provided by a trusted mechanism provided by
    Flask-Asylum. Two such examples are a signed cookie or a client session property. In the second
    case the identity has been provided by a client and isn't necessarily trusted.
    """

    def __init__(self, app=None, identity_provider=None, authn_provider=None,
                 authz_provider=None, anonymous_identity=None):
        self.app = app
        self.identity_provider = identity_provider
        self.authz_provider = authz_provider
        self.authn_provider = authn_provider
        self.anonymous_identity = anonymous_identity or Authentication(acl.Anonymous)

        if self.app:
            self.init_app(self.app)

    def init_app(self, app):
        app.after_request(self._after_request)
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['asylum'] = self

    def can(self, permission, identity=None, **kwargs):
        identity = identity or current_identity
        return self.authz_provider.can(identity, permission, **kwargs)

    def cannot(self, *args, **kwargs):
        return not self.can(*args, **kwargs)

    def set_identity(self, identity):
        _request_ctx_stack.top.identity = identity or self.anonymous_identity

    def _load_identity(self):
        identity = self.identity_provider.identify()
        if identity and self.authn_provider:
            identity = self.authn_provider.authenticate(identity)
        self.set_identity(identity)

    def _after_request(self, response):
        if current_identity.authenticated:
            self.identity_provider.remember(response, current_identity)
        else:
            self.identity_provider.forget(response)
        return response
