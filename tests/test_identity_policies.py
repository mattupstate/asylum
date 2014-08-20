# -*- coding: utf-8 -*-
"""
    test_identity_policies
    ~~~~~~~~~~~~~~~~~~~~~~

    Stock identity policy tests
"""

import base64

from flask import session

from flask_asylum import current_identity, SessionIdentityPolicy, RememberMeCookieIdentityPolicy, \
    BasicAuthIdentityPolicy, MultiIdentityPolicy


def test_session_policy(app, client, asylum):
    @app.route('/login')
    def login():
        asylum.remember('abc123')
        return "logged in"

    @app.route('/logout')
    def logout():
        asylum.forget()
        return "logged out"

    @app.route('/')
    def index():
        return 'index'

    asylum.identity_policy = SessionIdentityPolicy()

    with client as c:
        c.get('/')
        assert 'identity' not in session
        assert current_identity._get_current_object() is None

    response = client.get('/login')

    with client as c:
        c.get('/')
        assert session['identity'] == 'abc123'
        assert c.cookie_jar._cookies['localhost.local']['/']['session'] is not None
        assert current_identity._get_current_object() == ('abc123', None)

    with client as c:
        c.get('/logout')
        assert 'identity' not in session
        assert 'session' not in c.cookie_jar._cookies['localhost.local']['/']
        assert current_identity._get_current_object() is None


def test_remember_me_cookie_policy(app, client, asylum):
    @app.route('/login')
    def login():
        asylum.remember('abc123')
        return 'logged in'

    @app.route('/logout')
    def logout():
        asylum.forget()
        return "logged out"

    @app.route('/')
    def index():
        return 'index'

    asylum.identity_policy = RememberMeCookieIdentityPolicy('secret')

    with client as c:
        c.get('/')
        assert 'localhost.local' not in c.cookie_jar._cookies
        assert current_identity._get_current_object() is None

    response = client.get('/login')

    with client as c:
        c.get('/')
        assert current_identity._get_current_object() == ('abc123', None)
        assert c.cookie_jar._cookies['localhost.local']['/']['_remember_me'].value.startswith('abc123|')


    with client as c:
        c.get('/logout')
        assert current_identity._get_current_object() is None
        assert '_remember_me' not in c.cookie_jar._cookies['localhost.local']['/']


def test_http_basic_auth_policy(app, client, asylum):
    @app.route('/')
    def index():
        return 'index'

    asylum.identity_policy = BasicAuthIdentityPolicy()

    with client as c:
        response = c.get('/')
        assert current_identity._get_current_object() is None
        assert 'WWW-Authenticate' in response.headers

    with client as c:
        identity = base64.b64encode(b"abc123:password").decode('utf-8')
        response = c.get('/', headers={'Authorization': 'Basic %s' % identity})
        assert current_identity._get_current_object() == ('abc123', 'password')


def test_multi_policy(app, client, asylum):
    @app.route('/login')
    def login():
        asylum.remember('abc123')
        return 'logged in'

    @app.route('/logout')
    def logout():
        asylum.forget()
        return "logged out"

    @app.route('/')
    def index():
        return 'index'

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
        assert session['identity'] == 'abc123'
        assert current_identity._get_current_object() == ('abc123', None)
        assert c.cookie_jar._cookies['localhost.local']['/']['session'] is not None
        assert c.cookie_jar._cookies['localhost.local']['/']['_remember_me'].value.startswith('abc123|')

    with client as c:
        c.get('/logout')
        assert current_identity._get_current_object() is None
        assert 'identity' not in session
        assert 'session' not in c.cookie_jar._cookies['localhost.local']['/']
        assert '_remember_me' not in c.cookie_jar._cookies['localhost.local']['/']
