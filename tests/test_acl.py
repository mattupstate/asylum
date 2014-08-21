# -*- coding: utf-8 -*-
"""
    test_acl
    ~~~~~~~~

    ACL tests
"""

from flask import abort

from flask_asylum import ACL, AuthorizationPolicy, SessionIdentityPolicy, current_identity
from flask_asylum.acl import Allow, Read, Any


class PrincipaledDictionaryAuthorizationPolicy(AuthorizationPolicy):
    def __init__(self, acl):
        self._acl = acl
        self._users = {
            'mary': {'groups': ['admin', 'editor']},
            'tina': {'groups': ['editor']}
        }

    def permits(self, identity, permission, context=None):
        user =  self._users.get(identity.user_id, None)
        if user is None:
            return False

        principals = ['user:' + identity.user_id] + ['group:' + g for g in user.get('groups', [])]
        return self._acl.permits(principals, permission)

    def authorized_userid(self, identity):
        if identity.user_id in self._users:
            return identity.user_id


def test_acl_decorator(app, client, asylum):
    acl = ACL()

    asylum.identity_policy = SessionIdentityPolicy()
    asylum.authorization_policy = PrincipaledDictionaryAuthorizationPolicy(acl)

    @app.route('/allow')
    @acl.protected_by((Allow, 'group:admin', Read))
    def allow():
        if asylum.authorization_policy.permits(current_identity, Read):
            return 'allow'
        else:
            abort(401)

    client.get('/login/mary')

    with client as c:
        response = c.get('/allow')
        assert response.status_code == 200

    client.get('/login/tina')
    with client as c:
        response = c.get('/allow')
        assert response.status_code == 401
