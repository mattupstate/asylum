# -*- coding: utf-8 -*-
"""
    flask_asylum
    ~~~~~~~~~~~~

    Flask-Asylum top level package
"""

from .core import Asylum, current_identity
from .identity import SessionIdentityPolicy, RememberMeCookieIdentityPolicy, \
    BasicAuthIdentityPolicy, MultiIdentityPolicy
