# -*- coding: utf-8 -*-
"""
    test_core
    ~~~~~~~~~

    Core module tests
"""

import pytest

from asylum.core import Authentication


def test_authentication_constructor_with_required_args():
    auth = Authentication('mwright')
    assert auth.identity == 'mwright'
    assert auth.credentials is None
    assert not auth.authenticated


def test_authentication_constructor_with_optional_args():
    auth = Authentication('mwright', 'password', True)
    assert auth.identity == 'mwright'
    assert auth.credentials == 'password'
    assert auth.authenticated


def test_authentication_property_setters_fail():
    msg = "can't set attribute"
    auth = Authentication('mwright')

    with pytest.raises(AttributeError) as excinfo:
        auth.identity = 'x'
    assert msg in str(excinfo.value)

    with pytest.raises(AttributeError) as excinfo:
        auth.credentials = 'x'
    assert msg in str(excinfo.value)

    with pytest.raises(AttributeError) as excinfo:
        auth.authenticated = 'x'
    assert msg in str(excinfo.value)

    with pytest.raises(AttributeError) as excinfo:
        auth.principals = 'x'
    assert msg in str(excinfo.value)


def test_authentication_string_representation(capsys):
    auth = Authentication('mwright', 'secret', True, ['hi'])
    print(auth)
    out, err = capsys.readouterr()
    assert out == "Authentication(mwright, authenticated=True, principals=['hi'])\n"
