# -*- coding: utf-8 -*-
"""
    test_authz
    ~~~~~~~~~~

    Authz module tests
"""

import pytest

from asylum import core


class IdentityAuthorizationProvider(core.AuthorizationProvider):
    """A very simple authorization provider that implicitly trusts the
    principal as provided.
    """

    def __init__(self):
        self._identities = {
            'mwright': {'perm1', 'perm2'},
            'kjones': {'perm1'}
        }

    def _get_permissions(self, principal):
        return self._identities.get(principal, [])

    def can(self, authentication, permission, **kwargs):
        return permission in self._get_permissions(authentication.identity)


def test_base_authorization_provider():
    provider = core.AuthorizationProvider()
    with pytest.raises(NotImplementedError):
        provider.can(None, None);


def test_identity_authorization_provider():
    provider = IdentityAuthorizationProvider()

    authentication = core.Authentication('mwright')
    assert provider.can(authentication, 'perm1')
    assert provider.can(authentication, 'perm2')
    assert provider.cannot(authentication, 'perm3')

    authentication = core.Authentication('kjones')
    assert provider.can(authentication, 'perm1')
    assert provider.cannot(authentication, 'perm2')
    assert provider.cannot(authentication, 'perm3')
