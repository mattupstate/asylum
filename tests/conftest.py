# # -*- coding: utf-8 -*-
# """
#     conftest
#     ~~~~~~~~

#     Test fixtures, etc
# """

# import pytest

# from flask import Flask, request
# from asylum.core import Asylum, Authentication
# from asylum.authn import InMemoryAuthenticationProvider


# @pytest.fixture()
# def flask_app():
#     app = Flask(__name__)
#     app.debug = True
#     app.testing = True
#     app.config['SECRET_KEY'] = 'shhhh'
#     return app


# @pytest.fixture()
# def flask_client(flask_app):
#     return flask_app.test_client()


# @pytest.fixture()
# def asylum(flask_app):
#     asylum = Asylum(app)
#     asylum.authn_provider = InMemoryAuthenticationProvider({'mwright': 'password'})

#     @app.route('/login')
#     def login():
#         if 'user' in request.args:
#             asylum.set_identity(Authentication(request.args['user'], None, True))
#             return 'logged in'
#         return 'login error', 400

#     @app.route('/logout')
#     def logout():
#         asylum.set_identity(None)
#         return "logged out"

#     @app.route('/')
#     def index():
#         return 'index'

#     return asylum
