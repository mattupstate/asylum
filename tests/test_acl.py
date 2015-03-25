# -*- coding: utf-8 -*-
"""
    test_acl
    ~~~~~~~~

    ACL tests
"""

from flask import abort

from flask_asylum import acl
from flask_asylum.authz import AuthorizationProvider
from flask_asylum.ident import SessionIdentityProvider


class PrincipaledDictionaryAuthorizationProvider(AuthorizationProvider):
    def __init__(self):
        self._user_groups = {
            'mary': ['admin', 'editor'],
            'tina': ['editor']
        }

    def can(self, identity, permission, **kwargs):
        groups = self._user_groups[identity.uid]

        principals = [
            'user:' + identity.uid
        ] + [
            'group:' + g for g in groups
        ]
        return acl.can(principals, permission, **kwargs)


def test_acl_decorator(app, client, asylum):
    asylum.identity_provider = SessionIdentityProvider()
    asylum.authz_provider = PrincipaledDictionaryAuthorizationProvider()

    class MockObj(object):
        __acl__ = [
            (acl.Allow, 'group:admin', acl.Read)
        ]

    @app.route('/protected')
    def protected():
        if asylum.can(acl.Read, obj=MockObj):
            return 'protected'
        abort(401)

    client.get('/login?user=mary')

    with client as c:
        response = c.get('/protected')
        assert response.status_code == 200

    client.get('/login?user=tina')
    with client as c:
        response = c.get('/protected')
        assert response.status_code == 401
