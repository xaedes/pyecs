#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from pyecs import *
from pyecs.components import *

from collections import defaultdict
from testing import *

class TestEntity():
    def test__reset_global(self):
        Entity.__uid__ = "foo"
        Entity.__tags__ = "bar"
        assert hasattr(Entity, "__uid__")
        assert hasattr(Entity, "__tags__")
        assert type(Entity.__uid__) != int
        assert type(Entity.__tags__) != defaultdict
        
        Entity._reset_global()

        assert hasattr(Entity, "__uid__")
        assert hasattr(Entity, "__tags__")
        assert type(Entity.__uid__) == int
        assert type(Entity.__tags__) == defaultdict
        assert Entity.__uid__ == 0
        assert Entity.__tags__ == defaultdict(set)

    def test_entity_static_members(self):
        Entity._reset_global()
        e = Entity()
        assert hasattr(Entity, "__uid__")
        assert type(Entity.__uid__) == int
        assert hasattr(Entity, "__tags__")
        assert type(Entity.__tags__) == defaultdict

    def test_initial_state(self):
        Entity._reset_global()
        e = Entity()
        assert hasattr(e, "uid")
        assert hasattr(e, "parent")
        assert hasattr(e, "children")
        assert hasattr(e, "tags")
        assert hasattr(e, "components")
        assert type(e.uid) == int
        assert type(e.components) == defaultdict
        assert type(e.children) == list
        assert type(e.tags) == set
        assert e.parent == None
        assert len(list(e.components.iterkeys())) == 0
        assert len(e.children) == 0
        assert len(e.tags) == 0

    def test_add_tag(self):
        Entity._reset_global()
        e = Entity()
        assert "foo" not in e.tags
        assert "foo" not in Entity.__tags__
        assert e not in Entity.__tags__["foo"]
        e.add_tag("foo")
        assert "foo" in e.tags
        assert "foo" in Entity.__tags__
        assert e in Entity.__tags__["foo"]

    def test_remove_tag(self):
        Entity._reset_global()
        e = Entity()
        assert "foo" not in e.tags
        assert "foo" not in Entity.__tags__
        assert e not in Entity.__tags__["foo"]
        e.add_tag("foo")
        assert "foo" in e.tags
        assert "foo" in Entity.__tags__
        assert e in Entity.__tags__["foo"]
        e.remove_tag("foo")
        assert "foo" not in e.tags
        assert "foo" in Entity.__tags__ # because __tags__ is a defaultdict(set) we only removed from the set
        assert e not in Entity.__tags__["foo"]

    def test_add_component_when_added_does_nothing_and_returns_None(self):
        Entity._reset_global()
        e = Entity()
        c = Component()
        e.add_component(c)
        i = len(e.components[type(c)])
        assert e.add_component(c) == None
        assert len(e.components[type(c)]) == i

    def test_add_component_returns_component(self):
        Entity._reset_global()
        e = Entity()
        c = Component()
        assert e.add_component(c) == c

    def test_add_component(self):
        Entity._reset_global()
        e = Entity()
        c = Component()

        assert c not in e.components[type(c)]
        assert c not in Component.__added_components__[type(c)]
        e.add_component(c)
        assert c in e.components[type(c)]
        assert c in Component.__added_components__[type(c)]

    def test_add_component_callbacks(self):
        Entity._reset_global()
        e = Entity()
        c = Component()
        def component_added(component,entity):
            assert e == entity
            assert c == component
            component_added.called = True
        component_added.called = False
        def component_attached():
            component_attached.called = True
        component_attached.called = False
        e.register_callback("component_added", component_added)
        c.register_callback("component_attached", component_attached)
        e.add_component(c)
        assert component_added.called
        assert component_attached.called


