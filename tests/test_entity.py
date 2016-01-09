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

    def test_has_tag(self):
        Entity._reset_global()
        e = Entity()
        assert e.has_tag("foo") == False
        e.add_tag("foo")
        assert e.has_tag("foo") == True

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
        Component._reset_global()
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

        def component_attached():
            component_attached.called = True

        e.register_callback("component_added", component_added)
        c.register_callback("component_attached", component_attached)
        component_added.called = False
        component_attached.called = False
        e.add_component(c)
        assert component_added.called
        assert component_attached.called


    def test_remove_component(self):
        Entity._reset_global()
        Component._reset_global()
        e = Entity()
        c = Component()

        e.add_component(c)
        assert c in e.components[type(c)]
        assert c in Component.__added_components__[type(c)]

        e.remove_component(c)
        assert c not in e.components[type(c)]
        assert c not in Component.__added_components__[type(c)]

    
    def test_remove_component_callbacks(self):
        Entity._reset_global()
        e = Entity()
        c = Component()

        def component_removed(component,entity):
            assert e == entity
            assert c == component
            component_removed.called = True

        def component_detached(entity):
            assert e == entity
            component_detached.called = True

        e.register_callback("component_removed", component_removed)
        c.register_callback("component_detached", component_detached)
        e.add_component(c)

        component_removed.called = False
        component_detached.called = False
        e.remove_component(c)
        assert component_removed.called
        assert component_detached.called

    def test_find_parent_entity_with_component(self):
        e0 = Entity()
        e1 = Entity()
        e2 = Entity()
        e3 = Entity()
        e4 = Entity()
        c = Component()
        e0.add_entity(e1)
        e1.add_entity(e2)
        e2.add_entity(e3)
        e3.add_entity(e4)
        e2.add_component(c)

        assert e0.find_parent_entity_with_component(type(c)) == None
        assert e1.find_parent_entity_with_component(type(c)) == None
        assert e2.find_parent_entity_with_component(type(c)) == None
        assert e3.find_parent_entity_with_component(type(c)) == e2
        assert e4.find_parent_entity_with_component(type(c)) == e2

    def test_add_entity(self):
        e_parent = Entity()
        e_child = Entity()
        def entity_added(parent,entity):
            assert parent == e_parent
            assert entity == e_child
            entity_added.called = True

        assert e_child not in e_parent.children
        assert e_child.parent != e_parent
        entity_added.called = False
        e_child.register_callback("entity_added",entity_added)
        e_parent.add_entity(e_child)
        assert e_child in e_parent.children
        assert e_child.parent == e_parent
        assert entity_added.called

    def test_remove_entity_result(self):
        e_parent = Entity()
        e_child = Entity()
        
        assert e_parent.remove_entity(e_child) == False
        e_parent.add_entity(e_child)
        assert e_parent.remove_entity(e_child) == True
        assert e_parent.remove_entity(e_child) == False
    
    def test_remove_entity(self):
        e_parent = Entity()
        e_child = Entity()
        
        def entity_removed(parent,entity):
            assert parent == e_parent
            assert entity == e_child
            entity_removed.called = True

        e_child.register_callback("entity_removed",entity_removed)
        e_parent.add_entity(e_child)

        assert e_child.parent is not None
        assert e_child in e_parent.children

        entity_removed.called = False
        e_parent.remove_entity(e_child)

        assert entity_removed.called
        assert e_child.parent is None
        assert e_child not in e_parent.children

    def test_remove_from_parent(self):
        e_parent = Entity()
        e_child = Entity()
        
        def entity_removed(parent,entity):
            assert parent == e_parent
            assert entity == e_child
            entity_removed.called = True

        e_child.register_callback("entity_removed",entity_removed)
        e_parent.add_entity(e_child)

        assert e_child.parent is not None
        assert e_child in e_parent.children

        entity_removed.called = False
        e_child.remove_from_parent()

        assert entity_removed.called
        assert e_child.parent is None
        assert e_child not in e_parent.children

    def test_remove_entity_result_from_parent(self):
        e_parent = Entity()
        e_child = Entity()
        
        assert e_child.remove_from_parent() == False
        e_parent.add_entity(e_child)
        assert e_child.remove_from_parent() == True
        assert e_child.remove_from_parent() == False
    

    def test_has_component(self):
        e = Entity()
        c = Component()

        assert not e.has_component(type(c))
        e.add_component(c)
        assert e.has_component(type(c))
        e.remove_component(c)
        assert not e.has_component(type(c))

    def test_get_component(self):
        e = Entity()
        c0 = Component()
        c1 = Component()

        assert e.get_component(type(c0)) == None
        assert e.get_component(Component) == None
        
        e.add_component(c0)
        assert e.get_component(Component) == c0

        e.add_component(c1)
        assert e.get_component(Component) == c0

        e.remove_component(c0)
        assert e.get_component(Component) == c1
        
        e.add_component(c0)
        assert e.get_component(Component) == c1
        
        e.remove_component(c0)
        e.remove_component(c1)
        assert e.get_component(Component) == None
        
        e.add_component(c0)
        e.add_component(c1)
        assert e.get_component(Component) == c0
        
        e.remove_component(c1)
        assert e.get_component(Component) == c0

    def test_find_root(self):
        e0 = Entity()
        e1 = Entity()
        e2 = Entity()
        e3 = Entity()
        e4 = Entity()
        e0.add_entity(e1)
        e1.add_entity(e2)
        e2.add_entity(e3)
        e2.add_entity(e4)

        assert e0.find_root() == e0
        assert e1.find_root() == e0
        assert e2.find_root() == e0
        assert e3.find_root() == e0
        assert e4.find_root() == e0

    def test_entity_path(self):
        e0 = Entity()
        e1 = Entity()
        e2 = Entity()
        e3 = Entity()
        e4 = Entity()
        e0.add_entity(e1)
        e1.add_entity(e2)
        e2.add_entity(e3)
        e2.add_entity(e4)

        assert list(e0.entity_path()) == [e0]
        assert list(e1.entity_path()) == [e0,e1]
        assert list(e2.entity_path()) == [e0,e1,e2]
        assert list(e3.entity_path()) == [e0,e1,e2,e3]
        assert list(e4.entity_path()) == [e0,e1,e2,e4]

    def test_uid(self):
        Entity._reset_global()
        e0 = Entity()
        e1 = Entity()
        e2 = Entity()

        assert e0.uid == 0
        assert e1.uid == 1
        assert e2.uid == 2
        
    def test_uid_path(self):
        Entity._reset_global()
        e0 = Entity()
        e1 = Entity()
        e2 = Entity()
        e3 = Entity()
        e4 = Entity()
        e0.add_entity(e1)
        e1.add_entity(e2)
        e2.add_entity(e3)
        e2.add_entity(e4)

        assert e0.uid_path() == "0"
        assert e1.uid_path() == "0.1"
        assert e2.uid_path() == "0.1.2"
        assert e3.uid_path() == "0.1.2.3"
        assert e4.uid_path() == "0.1.2.4"

    @forEach("i",generateNaturalIntegers,2**5)
    def test_find_all_entities_with_component(self,i):
        Entity._reset_global()
        e0 = Entity()
        e1 = Entity()
        e2 = Entity()
        e3 = Entity()
        e4 = Entity()
        c = Component()
        e0.add_entity(e1)
        e1.add_entity(e2)
        e2.add_entity(e3)
        e2.add_entity(e4)

        es = []

        # assert find_all_entities_with_component(..) - es  == []
        for e in [e0,e1,e2,e3,e4]:
            assert [item for item in e.find_all_entities_with_component(Component) if item not in es] == []

        
        for k,e in enumerate([e0,e1,e2,e3,e4]):
            # if k'th bit is set in i
            if (1 << k) & i == (1 << k):
                e.add_component((c))
                es.append(e)

        # assert find_all_entities_with_component(..) - es  == []
        for e in [e0,e1,e2,e3,e4]:
            assert [item for item in e.find_all_entities_with_component(Component) if item not in es] == []

    def test_find_entities_with_component(self):
        Entity._reset_global()
        e0 = Entity()
        e1 = Entity()
        e2 = Entity()
        e3 = Entity()
        e4 = Entity()
        c = Component()
        e0.add_entity(e1)
        e1.add_entity(e2)
        e2.add_entity(e3)
        e2.add_entity(e4)

        e1.add_component(c)
        e2.add_component(c)

        es = [e1,e2]

        assert [item for item in e0.find_entities_with_component(Component) if item not in [e1,e2]] == []
        assert e1 in e0.find_entities_with_component(Component)
        assert e2 in e0.find_entities_with_component(Component)
        assert [item for item in e1.find_entities_with_component(Component) if item not in [e1,e2]] == []
        assert e1 in e1.find_entities_with_component(Component)
        assert e2 in e1.find_entities_with_component(Component)
        assert [item for item in e2.find_entities_with_component(Component) if item not in [e2]] == []
        assert e2 in e2.find_entities_with_component(Component)
        assert e3.find_entities_with_component(Component) == []
        assert e4.find_entities_with_component(Component) == []

    def test_find_entity_with_component(self):
        Entity._reset_global()
        e0 = Entity()
        e1 = Entity()
        e2 = Entity()
        e3 = Entity()
        e4 = Entity()
        c = Component()
        e0.add_entity(e1)
        e1.add_entity(e2)
        e2.add_entity(e3)
        e2.add_entity(e4)

        e1.add_component(c)
        e2.add_component(c)

        assert e0.find_entity_with_component(Component) == e1
        assert e1.find_entity_with_component(Component) == e1
        assert e2.find_entity_with_component(Component) == e2
        assert e3.find_entity_with_component(Component) == None
        assert e4.find_entity_with_component(Component) == None

    def test_first_or_none(self):
        assert Entity.first_or_none([]) == None
        assert Entity.first_or_none([1]) == 1
        assert Entity.first_or_none([1,2]) == 1
        assert Entity.first_or_none([4,3,2,1]) == 4
        assert Entity.first_or_none([None,3,2,1]) == None # note this!
    
    def test_find_entities_with_tag(self):
        Entity._reset_global()
        e0 = Entity()
        e1 = Entity()
        e2 = Entity()
        
        e0.add_tag("foo")
        assert type(Entity.find_entities_with_tag("foo")) == set
        assert Entity.find_entities_with_tag("foo") == set([e0])

        e1.add_tag("foo")
        assert Entity.find_entities_with_tag("foo") == set([e0,e1])

    @forEach("i",lambda:iter(range(10)))
    @discardParameter("i")
    def test_find_entity_with_tag(self):
        Entity._reset_global()
        e0 = Entity()
        e1 = Entity()
        e2 = Entity()
        
        assert Entity.find_entity_with_tag("foo") == None
        
        e0.add_tag("foo")
        assert Entity.find_entity_with_tag("foo") == e0

        e1.add_tag("foo")
        assert Entity.find_entity_with_tag("foo") in [e0,e1]

        e0.remove_tag("foo")
        assert Entity.find_entity_with_tag("foo") == e1
        
        e1.remove_tag("foo")
        assert Entity.find_entity_with_tag("foo") == None

    def test_find_entities_with_tags(self):
        Entity._reset_global()
        e0 = Entity()
        e1 = Entity()
        e2 = Entity()
        
        e0.add_tag("foo")
        assert type(Entity.find_entities_with_tags(["foo"])) == set
        assert Entity.find_entities_with_tags(["foo"]) == set([e0])

        e1.add_tag("foo")
        assert Entity.find_entities_with_tags(["foo"]) == set([e0,e1])

        assert Entity.find_entities_with_tags(["foo","bar"]) == set([])

        e0.add_tag("bar")
        assert Entity.find_entities_with_tags(["foo","bar"]) == set([e0])

        e1.add_tag("bar")
        assert Entity.find_entities_with_tags(["foo","bar"]) == set([e0,e1])
    
    @forEach("i",lambda:iter(range(10)))
    @discardParameter("i")
    def test_find_entity_with_tags(self):
        Entity._reset_global()
        e0 = Entity()
        e1 = Entity()
        e2 = Entity()
        
        e0.add_tag("foo")
        assert Entity.find_entity_with_tags(["foo"]) == e0

        e1.add_tag("foo")
        assert Entity.find_entity_with_tags(["foo"]) in set([e0,e1])

        assert Entity.find_entity_with_tags(["foo","bar"]) == None

        e0.add_tag("bar")
        assert Entity.find_entity_with_tags(["foo","bar"]) == e0

        e1.add_tag("bar")
        assert Entity.find_entity_with_tags(["foo","bar"]) in set([e0,e1])

    def test_find_entities(self):
        Entity._reset_global()
        e0 = Entity()
        e1 = Entity()
        e2 = Entity()
        e3 = Entity()
        e4 = Entity()
        e0.add_entity(e1)
        e1.add_entity(e2)
        e2.add_entity(e3)
        e2.add_entity(e4)

        assert e0.find_entities(lambda e:True) == [e0,e1,e2,e3,e4]
        assert e1.find_entities(lambda e:True) == [e1,e2,e3,e4]
        assert e2.find_entities(lambda e:True) == [e2,e3,e4]
        assert e3.find_entities(lambda e:True) == [e3]
        assert e4.find_entities(lambda e:True) == [e4]
        
        assert e0.find_entities(lambda e:False) == []
        assert e1.find_entities(lambda e:False) == []
        assert e2.find_entities(lambda e:False) == []
        assert e3.find_entities(lambda e:False) == []
        assert e4.find_entities(lambda e:False) == []

        e0.flag = False
        e1.flag = True
        e2.flag = True
        e3.flag = False
        e4.flag = False

        assert e0.find_entities(lambda e:e.flag) == [e1,e2]
        assert e1.find_entities(lambda e:e.flag) == [e1,e2]
        assert e2.find_entities(lambda e:e.flag) == [e2]
        assert e3.find_entities(lambda e:e.flag) == []
        assert e4.find_entities(lambda e:e.flag) == []
    
    def test_traverse_entities(self):
        Entity._reset_global()
        e0 = Entity()
        e1 = Entity()
        e2 = Entity()
        e3 = Entity()
        e4 = Entity()
        e0.add_entity(e1)
        e1.add_entity(e2)
        e2.add_entity(e3)
        e2.add_entity(e4)

        def traverse_entities(e):
            traverse_entities.es.append(e)


        traverse_entities.es = []
        e0.traverse_entities(traverse_entities)
        assert traverse_entities.es == [e0,e1,e2,e3,e4]

        traverse_entities.es = []
        e1.traverse_entities(traverse_entities)
        assert traverse_entities.es == [e1,e2,e3,e4]

        traverse_entities.es = []
        e2.traverse_entities(traverse_entities)
        assert traverse_entities.es == [e2,e3,e4]

        traverse_entities.es = []
        e3.traverse_entities(traverse_entities)
        assert traverse_entities.es == [e3]

        traverse_entities.es = []
        e4.traverse_entities(traverse_entities)
        assert traverse_entities.es == [e4]

    def test_traverse_entities_accum(self):
        Entity._reset_global()
        e0 = Entity()
        e1 = Entity()
        e2 = Entity()
        e3 = Entity()
        e4 = Entity()
        e0.add_entity(e1)
        e1.add_entity(e2)
        e2.add_entity(e3)
        e2.add_entity(e4)

        def traverse_entities_accum(e,accum):
            accum.append(e)
            return accum


        assert e0.traverse_entities_accum(traverse_entities_accum,[]) == [e0,e1,e2,e3,e4]
        assert e1.traverse_entities_accum(traverse_entities_accum,[]) == [e1,e2,e3,e4]
        assert e2.traverse_entities_accum(traverse_entities_accum,[]) == [e2,e3,e4]
        assert e3.traverse_entities_accum(traverse_entities_accum,[]) == [e3]
        assert e4.traverse_entities_accum(traverse_entities_accum,[]) == [e4]

    def test_all_components(self):
        Entity._reset_global()
        e = Entity()

        class Component1(Component):
            def __init__(self, *args, **kwargs):
                super(Component1, self).__init__(*args, **kwargs)
        class Component2(Component):
            def __init__(self, *args, **kwargs):
                super(Component2, self).__init__(*args, **kwargs)

        assert set(e.all_components()) == set([])
        c1 = e.add_component(Component1())
        assert set(e.all_components()) == set([c1])
        c2 = e.add_component(Component2())
        assert set(e.all_components()) == set([c1,c2])
        c3 = e.add_component(Component2())
        assert set(e.all_components()) == set([c1,c2,c3])
        e.remove_component(c1)
        assert set(e.all_components()) == set([c2,c3])
        e.remove_component(c2)
        assert set(e.all_components()) == set([c3])
        e.remove_component(c3)
        assert set(e.all_components()) == set([])

    def test_print_components(self,capfd):
        Entity._reset_global()
        e = Entity()

        class Component1(Component):
            def __init__(self, *args, **kwargs):
                super(Component1, self).__init__(*args, **kwargs)
            def __str__(self):
                return str(("Component1", id(self)))
        class Component2(Component):
            def __init__(self, *args, **kwargs):
                super(Component2, self).__init__(*args, **kwargs)
            def __str__(self):
                return str(("Component2", id(self)))


        c1 = e.add_component(Component1())
        c2 = e.add_component(Component2())
        c3 = e.add_component(Component2())

        res = e.print_components(True)
        assert "Component1" in res
        assert str(id(c1)) in res
        assert "Component2" in res
        assert str(id(c2)) in res
        assert "Component2" in res
        assert str(id(c3)) in res

        e.print_components()
        out, err = capfd.readouterr()

        assert out == res + "\n"

    def test___str__(self):
        Entity._reset_global()
        e0 = Entity()
        e1 = Entity()
        e2 = Entity()
        e0.add_entity(e1)
        e1.add_entity(e2)
        class Component1(Component):
            def __init__(self, *args, **kwargs):
                super(Component1, self).__init__(*args, **kwargs)
            def __str__(self):
                return str("Component1")
        
        e2.add_component(Component1())
        e2.add_component(Component1())

        assert str(e0) == "Entity 0"
        assert str(e1) == "Entity 0.1"
        assert str(e2) == "Entity 0.1.2 Component1, Component1"

    def test_print_structure(self,capfd):
        Entity._reset_global()
        e0 = Entity()
        e1 = Entity()
        e2 = Entity()
        e0.add_entity(e1)
        e1.add_entity(e2)
        class Component1(Component):
            def __init__(self, *args, **kwargs):
                super(Component1, self).__init__(*args, **kwargs)
            def __str__(self):
                return str("Component1")
        
        e2.add_component(Component1())
        e2.add_component(Component1())

        res = e0.print_structure(True)
        assert res == "0        \n" + \
                      "0.1      \n" + \
                      "0.1.2    Component1, Component1"

        e0.print_structure()
        out, err = capfd.readouterr()

        assert out == res + "\n"
       
    def test_remove_component_removes_callbacks(self):
        e=Entity()
        class Component1(Component):
            def __init__(self, *args, **kwargs):
                super(Component1, self).__init__(*args, **kwargs)
                self.foobar_called = False

            @callback
            def foobar(self):
                self.foobar_called = True
        c = Component1()
        
        e.add_component(c)
        e.fire_callbacks("foobar")
        assert c.foobar_called == True
        
        e.remove_component(c)
        c.foobar_called = False
        e.fire_callbacks("foobar")
        assert c.foobar_called == False

    def test_readded_component_callbacks(self):
        e=Entity()
        class Component1(Component):
            def __init__(self, *args, **kwargs):
                super(Component1, self).__init__(*args, **kwargs)
                self.foobar_called = False

            @callback
            def foobar(self):
                self.foobar_called = True

        c = Component1()
        
        e.add_component(c)
        c.foobar_called = False
        e.fire_callbacks("foobar")
        assert c.foobar_called == True
        
        e.remove_component(c)
        c.foobar_called = False
        e.fire_callbacks("foobar")
        assert c.foobar_called == False

        e.add_component(c)
        c.foobar_called = False
        e.fire_callbacks("foobar")
        assert c.foobar_called == True

    def test_remove_component_doesnt_remove_component_callbacks(self):
        e=Entity()
        class Component1(Component):
            def __init__(self, *args, **kwargs):
                super(Component1, self).__init__(*args, **kwargs)
                self.foobar_called = False

            @component_callback
            def foobar(self):
                self.foobar_called = True
        c = Component1()
        
        e.add_component(c)
        c.foobar_called = False
        c.fire_callbacks("foobar")
        assert c.foobar_called == True
        
        e.remove_component(c)
        c.foobar_called = False
        c.fire_callbacks("foobar")
        assert c.foobar_called == True
