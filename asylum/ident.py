# # -*- coding: utf-8 -*-
# """
#     asylum.ident
#     ~~~~~~~~~~~~

#     Asylum's stock identity providers
# """

# from . import _compat, core

# # # import hmac

# # # from datetime import datetime, timedelta
# # # from hashlib import sha1

# # from . import _compat
# # from .core import Authentication

# # # IDENTITY_SESSION_KEY = 'identity'
# # # REMEMBER_COOKIE_NAME = '_remember_me'
# # # REMEMBER_COOKIE_DOMAIN = None
# # # REMEMBER_COOKIE_DURATION = timedelta(days=365)


# # class IdentityProvider(object):
# #     """And object representing an identity policy.
# #     """

# #     def identify(self):
# #         """Return the claimed identity of the user associated with the current request or ``None``
# #         if no identity can be found.
# #         """
# #         raise NotImplementedError


# class HMACIdentityProvider(core.IdentityProvider):

#     def __init__(self, secret_key, message_provider, delimiter=u'|'):
#         if isinstance(secret_key, _compat.text_type):  # pragma: no cover
#             secret_key = secret_key.encode('latin1')
#         self._secret_key = secret_key
#         self._message_provider = message_provider
#         self._delimiter = delimiter

#     def get_digest(self, value):
#         return hmac.new(self._secret_key, value.encode('utf-8'), sha1).hexdigest()

#     def sign(self, value):
#         return u'{0}{1}{2}'.format(value, self._delimiter, self._get_digest(value))

#     def unsign(self, message):
#         try:
#             value, digest = message.rsplit(self._delimiter, 1)
#             if hasattr(digest, 'decode'):
#                 digest = digest.decode('ascii')  # pragma: no cover
#         except ValueError:
#             return

#         # hmac.compare_digest offers a way to compare in constant time
#         if hmac.compare_digest(self._get_digest(value), digest):
#             return value

#     def identify(self):
#         return self._unsign(self._message_provider())


# # class PrioritizingIdentityProvider(IdentityProvider):
# #     """Iterates through a list of providers, returnining the first valid identity.
# #     """

# #     def __init__(self, providers=None):
# #         self._providers = providers or []

# #     def identify(self):
# #         for policy in self._providers:
# #             identity = policy.identify()
# #             if identity:
# #                 return identity
