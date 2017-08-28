# -*- coding: utf-8 -*-
"""
    test_authn
    ~~~~~~~~~~

    authn module tests
"""

import pytest

from asylum import core


class InMemoryAuthenticationProvider(core.AuthenticationProvider):
    """A very simple, username & plain-text-password authentication provider
    that uses an in-memory user lookup
    """

    def __init__(self, users):
        self._users = users

    def authenticate(self, authentication):
        username = authentication.identity
        password = authentication.credentials
        if self._users.get(username, None) == password:
            return core.Authentication(username, None, True)


in_memory_authn_provider = InMemoryAuthenticationProvider({
    'mwright': 'password'
})


def test_authentication_provider_base():
    with pytest.raises(NotImplementedError):
        core.AuthenticationProvider().authenticate(None)


def test_in_memory_authentication_provider():
    authentication = in_memory_authn_provider.authenticate(
        core.Authentication('mwright', 'password'))
    assert isinstance(authentication, core.Authentication)
    assert authentication.identity == 'mwright'
    assert authentication.credentials is None
    assert authentication.authenticated


def test_in_memory_authentication_provider_with_invalid_username():
    authentication = in_memory_authn_provider.authenticate(
        core.Authentication('bogus', 'password'))
    assert authentication is None


def test_in_memory_authentication_provider_with_invalid_password():
    authentication = in_memory_authn_provider.authenticate(
        core.Authentication('mwright', 'bogus'))
    assert authentication is None
