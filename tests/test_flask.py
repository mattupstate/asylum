# -*- coding: utf-8 -*-
"""
    test_flask
    ~~~~~~~~~~

    Flask integration tests
"""

from flask import session

from asylum.contrib.flask import FlaskAsylum


# def test_extension():
#     ext = FlaskAsylum()

# def test_session_provider(app, client, asylum):
#     asylum.identity_provider = SessionIdentityProvider()

#     with client as c:
#         c.get('/')
#         assert 'identity' not in session
#         assert current_identity.uid == acl.Anonymous

#     with client as c:
#         response = client.get('/login?user=mary')
#         assert response.status_code == 200
#         assert session['identity'] == 'mary'

#     with client as c:
#         c.get('/')
#         assert session['identity'] == 'mary'
#         assert c.cookie_jar._cookies['localhost.local']['/']['session'] is not None
#         assert isinstance(current_identity._get_current_object(), Authentication)
#         assert current_identity.uid == 'mary'
#         assert current_identity.credentials is None

#     with client as c:
#         c.get('/logout')
#         assert 'identity' not in session
#         assert 'session' not in c.cookie_jar._cookies['localhost.local']['/']
#         assert current_identity.uid == acl.Anonymous


# def test_remember_me_cookie_provider(app, client, asylum):
#     asylum.identity_provider = RememberMeCookieIdentityProvider('secret')

#     with client as c:
#         c.get('/')
#         assert 'localhost.local' not in c.cookie_jar._cookies
#         assert current_identity.uid == acl.Anonymous

#     response = client.get('/login?user=mary')
#     assert response.status_code == 200
#     assert 'Set-Cookie' in response.headers

#     with client as c:
#         c.get('/')
#         assert isinstance(current_identity._get_current_object(), Authentication)
#         assert current_identity.uid == 'mary'
#         assert current_identity.credentials is None
#         cookie = c.cookie_jar._cookies['localhost.local']['/']['_remember_me']
#         assert cookie.value.startswith('mary|')

#     with client as c:
#         c.get('/logout')
#         assert current_identity.uid == acl.Anonymous
#         assert '_remember_me' not in c.cookie_jar._cookies['localhost.local']['/']


# def test_http_basic_auth_provider(app, client, asylum):
#     asylum.identity_provider = BasicAuthIdentityProvider()

#     with client as c:
#         response = c.get('/')
#         assert current_identity.uid == acl.Anonymous
#         assert 'WWW-Authenticate' in response.headers

#     with client as c:
#         identity = base64.b64encode(b"mary:password").decode('utf-8')
#         response = c.get('/', headers={'Authorization': 'Basic %s' % identity})
#         assert isinstance(current_identity._get_current_object(), Authentication)
#         assert current_identity.uid == 'mary'
#         assert current_identity.credentials == 'password'


# def test_multi_provider(app, client, asylum):
#     asylum.identity_provider = MultiIdentityProvider([
#         SessionIdentityProvider(),
#         RememberMeCookieIdentityProvider('secret')
#     ])

#     with client as c:
#         c.get('/')
#         assert 'identity' not in session
#         assert current_identity.uid == acl.Anonymous

#     response = client.get('/login?user=mary')
#     assert response.status_code == 200

#     with client as c:
#         c.get('/')
#         assert session['identity'] == 'mary'
#         assert isinstance(current_identity._get_current_object(), Authentication)
#         assert current_identity.uid == 'mary'
#         assert current_identity.credentials is None
#         assert c.cookie_jar._cookies['localhost.local']['/']['session'] is not None
#         cookie = c.cookie_jar._cookies['localhost.local']['/']['_remember_me']
#         assert cookie.value.startswith('mary|')

#     with client as c:
#         c.get('/logout')
#         assert current_identity.uid == acl.Anonymous
#         assert 'identity' not in session
#         assert 'session' not in c.cookie_jar._cookies['localhost.local']['/']
#         assert '_remember_me' not in c.cookie_jar._cookies['localhost.local']['/']
