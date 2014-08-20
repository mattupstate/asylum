# -*- coding: utf-8 -*-
"""
    conftest
    ~~~~~~~~

    Test fixtures, etc
"""

import pytest

from flask import Flask
from flask_asylum.core import Asylum


@pytest.fixture()
def app():
    app = Flask(__name__)
    app.debug = True
    app.testing = True
    app.config['SECRET_KEY'] = 'shhhh'
    return app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def asylum(app):
    return Asylum(app)
