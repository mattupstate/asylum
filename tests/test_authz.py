# -*- coding: utf-8 -*-
"""
    test_authorization_policies
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Authorization policy tests
"""

from flask_asylum.authz import AuthorizationProvider
from flask_asylum.ident import SessionIdentityProvider


class GroupBasedAuthorizationProvider(AuthorizationProvider):
    def __init__(self):
        self._groups = {
            'admin': {'read', 'write', 'delete'},
            'editor': {'read', 'write'}
        }
        self._users = {
            'mary': {'admin', 'editor'},
            'tina': {'editor'}
        }

    def can(self, identity, permission, **kwargs):
        groups = self._users.get(identity.uid)
        permissions = set([p for g in groups for p in self._groups.get(g, [])])
        return permission in permissions


def test_custom_authz_provider(app, client, asylum):
    asylum.identity_provider = SessionIdentityProvider()
    asylum.authz_provider = GroupBasedAuthorizationProvider()

    with client as c:
        c.get('/login?user=mary')
        assert asylum.can('delete')

    with client as c:
        c.get('/login?user=tina')
        assert asylum.cannot('delete')
