# -*- coding: utf-8 -*-
"""
    test_identity_policies
    ~~~~~~~~~~~~~~~~~~~~~~

    Stock identity policy tests
"""

import base64

from flask import session

from flask_asylum import current_identity, SessionIdentityPolicy, RememberMeCookieIdentityPolicy, \
    BasicAuthIdentityPolicy, MultiIdentityPolicy, Identity


def test_session_policy(app, client, asylum):
    asylum.identity_policy = SessionIdentityPolicy()

    with client as c:
        c.get('/')
        assert 'identity' not in session
        assert current_identity._get_current_object() is None

    response = client.get('/login')

    with client as c:
        c.get('/')
        assert session['identity'] == 'mary'
        assert c.cookie_jar._cookies['localhost.local']['/']['session'] is not None
        assert isinstance(current_identity._get_current_object(), Identity)
        assert current_identity.user_id == 'mary'
        assert current_identity.credentials == None

    with client as c:
        c.get('/logout')
        assert 'identity' not in session
        assert 'session' not in c.cookie_jar._cookies['localhost.local']['/']
        assert current_identity._get_current_object() is None


def test_remember_me_cookie_policy(app, client, asylum):
    asylum.identity_policy = RememberMeCookieIdentityPolicy('secret')

    with client as c:
        c.get('/')
        assert 'localhost.local' not in c.cookie_jar._cookies
        assert current_identity._get_current_object() is None

    response = client.get('/login')

    with client as c:
        c.get('/')
        assert isinstance(current_identity._get_current_object(), Identity)
        assert current_identity.user_id == 'mary'
        assert current_identity.credentials == None
        assert c.cookie_jar._cookies['localhost.local']['/']['_remember_me'].value.startswith('mary|')

    with client as c:
        c.get('/logout')
        assert current_identity._get_current_object() is None
        assert '_remember_me' not in c.cookie_jar._cookies['localhost.local']['/']


def test_http_basic_auth_policy(app, client, asylum):
    asylum.identity_policy = BasicAuthIdentityPolicy()

    with client as c:
        response = c.get('/')
        assert current_identity._get_current_object() is None
        assert 'WWW-Authenticate' in response.headers

    with client as c:
        identity = base64.b64encode(b"mary:password").decode('utf-8')
        response = c.get('/', headers={'Authorization': 'Basic %s' % identity})
        assert isinstance(current_identity._get_current_object(), Identity)
        assert current_identity.user_id == 'mary'
        assert current_identity.credentials == 'password'


def test_multi_policy(app, client, asylum):
    asylum.identity_policy = MultiIdentityPolicy([
        SessionIdentityPolicy(),
        RememberMeCookieIdentityPolicy('secret')
    ])

    with client as c:
        c.get('/')
        assert 'identity' not in session
        assert current_identity._get_current_object() is None

    response = client.get('/login')

    with client as c:
        c.get('/')
        assert session['identity'] == 'mary'
        assert isinstance(current_identity._get_current_object(), Identity)
        assert current_identity.user_id == 'mary'
        assert current_identity.credentials == None
        assert c.cookie_jar._cookies['localhost.local']['/']['session'] is not None
        assert c.cookie_jar._cookies['localhost.local']['/']['_remember_me'].value.startswith('mary|')

    with client as c:
        c.get('/logout')
        assert current_identity._get_current_object() is None
        assert 'identity' not in session
        assert 'session' not in c.cookie_jar._cookies['localhost.local']['/']
        assert '_remember_me' not in c.cookie_jar._cookies['localhost.local']['/']
