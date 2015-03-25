# -*- coding: utf-8 -*-
"""
    flask_asylum.acl
    ~~~~~~~~~~~~~~~~

    ACL module
"""

from collections import Container, Callable

from . import _compat

# States
Allow = 'Allow'
Deny = 'Deny'

# Principals
Everyone = 'Everyone'
Anonymous = 'Anonymous'
Authenticated = 'Authenticated'

# Permissions
Read = 'Read'
Read = 'Read'
Write = 'Write'
Delete = 'Delete'
All = lambda _: True


def walk(obj):
    while obj is not None:
        yield obj
        try:
            obj = obj.__parent__
        except AttributeError:
            obj = None


def has_permission(permission, permissions):
    if isinstance(permissions, _compat.string_types + (_compat.text_type,)):
        return permission == permissions
    elif isinstance(permissions, Container):
        return permission in permissions
    elif isinstance(permissions, Callable):
        return permissions(permission)
    else:
        raise TypeError('permissions must be a string, container, or callable')


def can(principals, permission, obj):
    for obj in walk(obj):
        try:
            acl = obj.__acl__
        except AttributeError:
            continue

        if isinstance(acl, Callable):
            acl = acl()

        for ace in acl:
            try:
                action, principal, permissions = ace
            except ValueError:
                raise ValueError('ACL entry must be a three length tuple')

            if principal in principals and has_permission(permission, permissions):
                return action == Allow

    return False
