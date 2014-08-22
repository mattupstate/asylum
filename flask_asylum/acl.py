# -*- coding: utf-8 -*-
"""
    flask_asylum.acl
    ~~~~~~~~~~~~~~~~

    ACL module
"""

from flask import g, current_app, request

Everyone = 'Everyone'
Authenticated = 'Authenticated'
Allow = 'Allow'
Deny = 'Deny'
Read = 'Read'
Write = 'Write'
Delete = 'Delete'
Any = [Read, Write, Delete]

class ACL(object):

    default_acl = (Deny, Everyone, Any)

    def protected_by(self, *rules):
        def decorator(obj):
            obj.__acl__ = rules
            return obj
        return decorator

    def permits(self, principals, permission):
        if self.current_acl is None:
            return False

        for ace in self.current_acl:
            ace_action, ace_principal, ace_permissions = ace
            if ace_principal in principals and permission in ace_permissions:
                return ace_action == Allow

    @property
    def current_acl(self):
        acl = getattr(g, '_current_acl', None)
        if acl is None:
            acl = g._current_acl = self._get_current_acl()
        return acl

    def _get_current_acl(self):
        root_acl = getattr(current_app, '__acl__', self.default_acl)
        blueprint_acl = None
        if request.blueprint:
            blueprint_acl = getattr(current_app.blueprints[request.blueprint], '__acl__', None)
        view_acl = getattr(current_app.view_functions[request.endpoint], '__acl__', None)
        return view_acl or blueprint_acl or root_acl


