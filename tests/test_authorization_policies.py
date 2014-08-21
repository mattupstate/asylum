# -*- coding: utf-8 -*-
"""
    test_authorization_policies
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Authorization policy tests
"""

from flask_asylum import AuthorizationPolicy, SessionIdentityPolicy, current_identity


class DictionaryAuthorizationPolicy(AuthorizationPolicy):
    def __init__(self):
        self._groups = {
            'admin': ['read', 'write', 'delete'],
            'editor': ['read', 'write']
        }
        self._users = {
            'mary': {'groups': ['admin', 'editor']},
            'tina': {'groups': ['editor']}
        }

    def permits(self, identity, permission, context=None):
        user =  self._users.get(identity.user_id, None)
        if user is not None:
            user_groups = user.get('groups', [])
            permissions = set([p for g in user_groups for p in self._groups.get(g, [])])
            return permission in permissions
        return False

    def authorized_userid(self, identity):
        if identity.user_id in self._users:
            return identity.user_id


def test_custom_authorization_policy(app, client, asylum):
    asylum.identity_policy = SessionIdentityPolicy()
    asylum.authorization_policy = DictionaryAuthorizationPolicy()

    with client as c:
        c.get('/login/mary')
        assert asylum.authorization_policy.permits(current_identity, 'delete')

    with client as c:
        c.get('/login/tina')
        assert not asylum.authorization_policy.permits(current_identity, 'delete')


def test_acl_decorator(app, client, asylum):
    asylum.identity_policy = SessionIdentityPolicy()
    asylum.authorization_policy = DictionaryAuthorizationPolicy()

    @app.route('/allow')
    @asylum.acl([
        (asylum.Allow, '*', '*')
    ])
    def allow():
        return 'allow'

    with client as c:
        c.get('/allow')
