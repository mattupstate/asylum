# # -*- coding: utf-8 -*-
"""
    test_acl
    ~~~~~~~~

    ACL module tests
"""

import pytest

from asylum import acl


class Node(object):

    def __init__(self, name, parent=None, acl=None):
        self.name = name
        if parent:
            self.__parent__ = parent
        if acl:
            self.__acl__ = acl


class Thing(object):

    def __init__(self, id):
        self._id = id

    def __acl__(self):
        return [
            (Allow, acl.Admin, acl.All),
            (Allow, 'thing:%s' % self.id, All)
        ]

def test_has_permisssion_with_string_value():
    assert acl.has_permission("write", "write")


def test_has_permisssion_with_container_value():
    assert acl.has_permission("write", ["write"])


def test_has_permisssion_with_callable_value():
    assert acl.has_permission("write", lambda p: p == "write")


def test_has_permisssion_with_unsupported_value():
    with pytest.raises(TypeError) as e:
        assert acl.has_permission("write", 1)
    assert 'permissions must be a string, container, or callable' in str(e)


def test_walk_with_tree():
    leaf = Node("3", Node("2", Node("1")))
    results = []
    for obj in acl.walk(leaf):
        assert isinstance(obj, Node)
        results.append(obj.name)
    assert len(results) == 3
    assert results == ["3", "2", "1"]


def test_get_acl():
    node = Node("1", None, "A")
    assert acl.get_acl(node) == "A"


def test_get_acl_with_callable():
    node = Node("1", None, lambda: "A")
    assert acl.get_acl(node) == "A"


def test_get_acl_with_tree():
    leaf = Node("2", Node("1", None, "A"), "B")
    assert acl.get_acl(leaf) == "B"


def test_get_acl_with_parent():
    leaf = Node("2", Node("1", None, "A"), None)
    assert acl.get_acl(leaf) == "A"


def test_get_acl_without_any_acls():
    leaf = Node("2", Node("1", None, None), None)
    assert acl.get_acl(leaf) == []


def test_get_acl_with_unknown_attribute_error():
    class Thing(object):
        def __acl__(self):
            raise AttributeError("something other than __acl__")

    with pytest.raises(AttributeError):
        acl.get_acl(Thing())


def test_static_acl_attribute_evaluation():
    obj = Node("A", None, [
        (acl.Allow, acl.Everyone, acl.Read)
    ])
    assert acl.can([acl.Everyone], acl.Read, obj)
