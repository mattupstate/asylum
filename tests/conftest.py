# -*- coding: utf-8 -*-
"""
    conftest
    ~~~~~~~~

    Test fixtures, etc
"""

import pytest

from flask import Flask
from flask_asylum.core import Asylum, Identity


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
    asylum = Asylum(app)

    @app.route('/login')
    @app.route('/login/mary')
    def login_mary():
        asylum.remember('mary')
        return "logged in"

    @app.route('/login/tina')
    def login_tina():
        asylum.remember('tina')
        return "logged in"

    @app.route('/logout')
    def logout():
        asylum.forget()
        return "logged out"

    @app.route('/')
    def index():
        return 'index'

    return asylum
