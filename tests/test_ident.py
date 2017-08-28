# -*- coding: utf-8 -*-
"""
    test_ident
    ~~~~~~~~~~

    Ident module tests
"""

import pytest

from asylum import core


class StaticIdentityProvider(core.IdentityProvider):

    def __init__(self, identity, credentials=None):
        self._identity = identity
        self._credentials = credentials

    def identify(self):
        if self._identity:
            return core.Authentication(self._identity, self._credentials)


def test_identity_provider_base():
    provider = core.IdentityProvider()
    with pytest.raises(NotImplementedError):
        provider.identify()
    with pytest.raises(NotImplementedError):
        provider.remember()
    with pytest.raises(NotImplementedError):
        provider.forget()


def test_static_identity_provider():
    provider = StaticIdentityProvider('mwright')
    authentication = provider.identify()
    assert isinstance(authentication, core.Authentication)
    assert authentication.identity == 'mwright'
    assert authentication.credentials is None
    assert not authentication.authenticated


def test_static_identity_provider_without_principal():
    provider = StaticIdentityProvider(None)
    authentication = provider.identify()
    assert authentication is None
