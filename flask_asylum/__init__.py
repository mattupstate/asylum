# -*- coding: utf-8 -*-
"""
    flask_asylum
    ~~~~~~~~~~~~

    Flask-Asylum top level package
"""

from .authorization import AuthorizationPolicy, MultiAuthorizationPolicy
from .core import Asylum, Identity, current_identity
from .identity import SessionIdentityPolicy, RememberMeCookieIdentityPolicy, \
    BasicAuthIdentityPolicy, MultiIdentityPolicy
