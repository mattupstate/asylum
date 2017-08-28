# -*- coding: utf-8 -*-
"""
    asylum.acl
    ~~~~~~~~~~

    ACL module
"""

from collections import Container, Callable

from . import _compat

# States
Allow = 'Allow'
Deny = 'Deny'

# Principals
Everyone = 'Everyone'
Authenticated = 'Authenticated'

# Permissions
Read = 'Read'
Write = 'Write'
Delete = 'Delete'
Any = lambda _: True


def walk(obj):
    while obj is not None:
        yield obj
        try:
            obj = obj.__parent__
        except AttributeError:
            obj = None


def _get_acl_attr(obj):
    try:
        acl = obj.__acl__
        if isinstance(acl, Callable):
            acl = acl()
        return acl
    except AttributeError as e:
        if "object has no attribute '__acl__'" in str(e):
            return None
        raise


def get_acl(obj):
    for obj in walk(obj):
        acl = _get_acl_attr(obj)
        if acl is None:
            continue
        return acl
    return []


def has_permission(permission, permissions):
    if isinstance(permissions, _compat.string_types + (_compat.text_type,)):
        return permission == permissions
    elif isinstance(permissions, Container):
        return permission in permissions
    elif isinstance(permissions, Callable):
        return permissions(permission)
    raise TypeError('permissions must be a string, container, or callable')


def can(principals, permission, obj):
    for obj in walk(obj):
        acl = get_acl(obj)
        print(acl)
        for action, principal, permissions in acl:
            if principal in principals and has_permission(permission, permissions):
                return action == Allow
    return False
