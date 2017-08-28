# -*- coding: utf-8 -*-
"""
    test_integration
    ~~~~~~~~~~~~~~~~

    Integration tests
"""

from asylum import acl, core


class StaticIdentityProvider(core.IdentityProvider):

    def __init__(self, identity):
        self._identity = identity

    def identify(self):
        return core.Authentication(self._identity)


class PrincipaledIdentityAuthenticationProvider(core.AuthenticationProvider):
    """A very simple, username & plain-text-password authentication provider
    that uses an in-memory user lookup
    """

    _default_principals = [
        acl.Authenticated,
        acl.Everyone
    ]

    def __init__(self, users):
        self._users = users

    def authenticate(self, authentication):
        ident = authentication.identity
        if ident in self._users:
            principals = self._default_principals + self._users[ident]
            return core.Authentication(ident, None, True, principals)


class PrincipaledAclAuthorizationProvider(core.AuthorizationProvider):

    def can(self, authentication, permission, **kwargs):
        return acl.can(authentication.principals, permission, **kwargs)


class Thing(object):

    def __init__(self, id):
        self._id = id

    def __acl__(self):
        return [
            (acl.Allow, acl.Everyone, acl.Read),
            (acl.Allow, 'thing:%s:owner' % self._id, acl.Write)
        ]


def test_with_principaled_configuration():
    mwright = StaticIdentityProvider('mwright')
    kjones = StaticIdentityProvider('kjones')

    authn = PrincipaledIdentityAuthenticationProvider({
        'mwright': ['thing:1:owner'],
        'kjones': ['thing:2:owner']}
    )
    authz = PrincipaledAclAuthorizationProvider()

    thing1 = Thing(1)
    thing2 = Thing(2)

    ctx = core.AsylumContext(mwright, authn, authz)
    assert isinstance(ctx.authentication, core.Authentication)
    assert ctx.can(acl.Read, obj=thing1)
    assert ctx.can(acl.Write, obj=thing1)
    assert ctx.can(acl.Read, obj=thing2)
    assert ctx.cannot(acl.Write, obj=thing2)

    ctx = core.AsylumContext(kjones, authn, authz)
    assert isinstance(ctx.authentication, core.Authentication)
    assert ctx.can(acl.Read, obj=thing1)
    assert ctx.cannot(acl.Write, obj=thing1)
    assert ctx.can(acl.Read, obj=thing2)
    assert ctx.can(acl.Write, obj=thing2)
