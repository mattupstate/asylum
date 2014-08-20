# -*- coding: utf-8 -*-
"""
    flask_asylum.authorization
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Stock authorization policies
"""

from datetime import timedelta

from itsdangerous import TimedJSONWebSignatureSerializer


class AuthorizationPolicy(object):
      """An object representing an authorization policy.
      """

      def permits(self, identity, permission):
          """Return True if the identity is allowed the permission in the current context,
          else return False
          """
          raise NotImplementedError

      def authorized_userid(self, identity):
          """Return the unique identifier of the user as described by the identity or 'None' if no
          user exists related to the identity
          """
          raise NotImplementedError
