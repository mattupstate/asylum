# -*- coding: utf-8 -*-
"""
    flask_asylum.identity
    ~~~~~~~~~~~~~~~~~~~~~

    Stock identity polcies
"""

import hmac

from datetime import datetime, timedelta
from hashlib import sha1

from flask import request, session
from werkzeug.security import safe_str_cmp

from .exceptions import AuthenticationError

IDENTITY_SESSION_KEY = 'identity'
REMEMBER_COOKIE_NAME = '_remember_me'
REMEMBER_COOKIE_DOMAIN = None
REMEMBER_COOKIE_DURATION = timedelta(days=365)


class IdentityPolicy(object):
    """And object representing an identity policy.
    """

    def identify(self):
        """Return the claimed identity of the user associated with the current request or ``None``
        if no identity can be found.
        """
        raise NotImplementedError

    def remember(self, response, identity, **kwargs):
        """Modify the response to remember ``identity`` for a subsequent request."""
        raise NotImplementedError

    def forget(self, response):
        """Modify the response to 'forget' the current identity on subsequent requests.
        """
        raise NotImplementedError


class RememberMeCookieIdentityPolicy(IdentityPolicy):
    """A "remember me" cookie identity policy. This identity policy loads an identity from a signed
    cookie if it exists.
    """

    def __init__(self, secret_key, name=None, domain=None, duration=None):
        if isinstance(secret_key, unicode):  # pragma: no cover
            secret_key = secret_key.encode('latin1')  # ensure bytes
        self._secret_key = secret_key
        self._name = name or REMEMBER_COOKIE_NAME
        self._domain = domain or REMEMBER_COOKIE_DOMAIN
        self._duration = duration or REMEMBER_COOKIE_DURATION

    def _cookie_digest(self, user_id):
        return hmac.new(self._secret_key, user_id.encode('utf-8'), sha1).hexdigest()

    def _encode_cookie(self, user_id):
        return u'{0}|{1}'.format(user_id, self._cookie_digest(user_id))

    def _decode_cookie(self, cookie):
        try:
            user_id, digest = cookie.rsplit(u'|', 1)
            if hasattr(digest, 'decode'):
                digest = digest.decode('ascii')  # pragma: no cover
        except ValueError:
            return

        if safe_str_cmp(self._cookie_digest(user_id), digest):
            return user_id

    def identify(self):
        cookie = request.cookies.get(self._name, None)
        if cookie:
            return self._decode_cookie(cookie)

    def remember(self, response, identity, **kwargs):
        user_id, _ = identity
        expires = datetime.utcnow() + self._duration
        response.set_cookie(self._name, value=self._encode_cookie(user_id), expires=expires,
                            domain=self._domain, secure=True, httponly=True)

    def forget(self, response):
        response.delete_cookie(self._name, domain=self._domain)


class SessionIdentityPolicy(IdentityPolicy):
    """A session identity policy. This policy loads the identity from the session if it exists.
    """

    def __init__(self, session_key=None):
        self._session_key = session_key or IDENTITY_SESSION_KEY

    def identify(self):
        return session.get(self._session_key, None)

    def remember(self, response, identity, **kwargs):
        user_id, _ = identity
        session[self._session_key] = user_id

    def forget(self, response):
        session.pop(self._session_key, None)


class AuthorizationHeaderIdentityPolicy(IdentityPolicy):
    """A base identity policy for `Authorization` header identity policies.
    """

    def __init__(self, auth_method, realm=None):
        self._auth_method = auth_method
        self._realm = realm or 'Login Required'

    def _decode_header(self, token):
        raise NotImplementedError

    def _validate_header(self, auth):
        parts = auth.split()
        total_parts = len(parts)
        return not any([
            total_parts <= 1, total_parts > 2,
            parts[0].lower() != self._auth_method.lower()
        ])

    def identify(self):
        auth = request.headers.get('Authorization', '')
        if auth and self._validate_header(auth):
            return self._decode_header(auth)

    def remember(self, *args, **kwargs):
        pass

    def forget(self, response):
        ctx = (self._auth_method, self._realm)
        response.headers['WWW-Authenticate'] = '%s realm=%s' % ctx


class BasicAuthIdentityPolicy(AuthorizationHeaderIdentityPolicy):
    """HTTP Basic authentication identity policy. This identity policy retrieves an untrusted
    username and password pair from a request.
    """

    def __init__(self, realm=None):
        AuthorizationHeaderIdentityPolicy.__init__(self, 'Basic', realm)

    def _decode_header(self, *args):
        auth = request.authorization
        if auth:
            return auth.username, auth.password


class MultiIdentityPolicy(IdentityPolicy):
    """An identity policy implementation that allows one to specify a list of policies to be
    checked, in order, and selecting the first identity to be found. For example, this allows one
    to use `SessionIdentityPolicy` and `RememberMeCookieIdentityPolicy` together.
    """

    def __init__(self, policies=None):
        self._policies = policies or []

    def add_policy(self, policy, index=None):
        if index:
            self._policies.insert(index, policy)
        else:
            self._policies.append(policy)

    def identify(self):
        for policy in self._policies:
            identity = policy.identify()
            if identity is None:
                continue
            return identity

    def remember(self, response, identity, **kwargs):
        for policy in self._policies:
            policy.remember(response, identity, **kwargs)

    def forget(self, response):
        for policy in self._policies:
            policy.forget(response)
