#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from pyecs import *
from pyecs.components import *

from collections import defaultdict
from testing import *

class TestComponent():
    def test__reset_global(self):
        assert hasattr(Component,"__added_components__")
        assert type(Component.__added_components__) == defaultdict

        Component.__added_components__ = "foo"
        
        assert type(Component.__added_components__) != defaultdict

        Component._reset_global()

        assert type(Component.__added_components__) == defaultdict

    def test_initial_state(self):
        c = Component()
        assert hasattr(c, "entity")
        assert c.entity == None
        assert hasattr(c, "__hotswap_callback__")

    def test_initial_state_entity_given(self):
        e = Entity()
        c = Component(e)
        assert hasattr(c, "entity")
        assert c.entity == e

    def test_register_callbacks_is_called_when_added(self):


        def register_callbacks():
            register_callbacks.called = True
                
        e = Entity()
        c = Component()
        c.register_callbacks = register_callbacks

        register_callbacks.called = False
        e.add_component(c)
        assert register_callbacks.called


    def test_register_callbacks_add_to_callbacks(self):
        class Comp(Component):
            def __init__(self):
                super(Comp, self).__init__()

            @callback
            def foo(self):
                self.foo_called = True
                
            @component_callback
            def bar(self):
                self.bar_called = True

        e = Entity()
        c = Comp()
        e.add_component(c)

        assert "bar" in c.callbacks
        assert c.bar in c.callbacks["bar"]

        assert "foo" in e.callbacks
        assert c.foo in e.callbacks["foo"]

        c.foo_called = False
        c.bar_called = False

        e.fire_callbacks("foo")
        
        assert c.foo_called
        assert not c.bar_called
        
        c.foo_called = False
        c.bar_called = False

        c.fire_callbacks("bar")
        
        assert not c.foo_called
        assert c.bar_called

    def test_register_callbacks_hotswap_false(self):
        class Comp(Component):
            def __init__(self):
                super(Comp, self).__init__()
                self.__hotswap_callback__ = False

            @callback
            def foo(self):
                self.foo_called = True
                

        e = Entity()
        c = Comp()
        e.add_component(c)

        c.foo_called = False
        e.fire_callbacks("foo")
        assert c.foo_called

        def foo2():
            foo2.called = True

        foo2.called = False
        c.foo_called = False

        c.foo = foo2

        e.fire_callbacks("foo")
        assert c.foo_called
        assert not foo2.called

    def test_register_callbacks_hotswap_true(self):
        class Comp(Component):
            def __init__(self):
                super(Comp, self).__init__()
                self.__hotswap_callback__ = True

            @callback
            def foo(self):
                self.foo_called = True
                

        e = Entity()
        c = Comp()
        e.add_component(c)

        c.foo_called = False
        e.fire_callbacks("foo")
        assert c.foo_called

        def foo2():
            foo2.called = True

        foo2.called = False
        c.foo_called = False

        c.foo = foo2

        e.fire_callbacks("foo")
        assert not c.foo_called
        assert foo2.called

    def test_register_callbacks_hotswap_false_deleted_callback(self):
        class Comp(Component):
            def __init__(self):
                super(Comp, self).__init__()
                self.__hotswap_callback__ = False
                
        @callback
        def foo():
            foo.called = True

        c = Comp()
        setattr(c, "foo", foo)
        assert hasattr(c,"foo")
        e = Entity()
        e.add_component(c)
        
        foo.called = False
        e.fire_callbacks("foo")
        assert foo.called 

        delattr(c,"foo")
        assert not hasattr(c,"foo")

        foo.called = False
        e.fire_callbacks("foo")
        assert foo.called 

    def test_register_callbacks_hotswap_true_deleted_callback(self):
        class Comp(Component):
            def __init__(self):
                super(Comp, self).__init__()
                self.__hotswap_callback__ = True
                
        @callback
        def foo():
            foo.called = True

        c = Comp()
        setattr(c, "foo", foo)
        assert hasattr(c,"foo")
        e = Entity()
        e.add_component(c)
        
        foo.called = False
        e.fire_callbacks("foo")
        assert foo.called 

        delattr(c,"foo")
        assert not hasattr(c,"foo")

        foo.called = False
        e.fire_callbacks("foo")
        assert not foo.called 

    def test_register_callbacks_hotswap_true_with_exception(self, capfd):
        class Comp(Component):
            def __init__(self):
                super(Comp, self).__init__()
                self.__hotswap_callback__ = True

            @callback
            def foo(self):
                self.foo_called = True
                
            def __str__(self):
                return "foobar"

        e = Entity()
        c = Comp()
        e.add_component(c)

        c.foo_called = False
        e.fire_callbacks("foo")
        assert c.foo_called

        def foo2():
            foo2.called = True
            raise Exception() # this will be catched

        foo2.called = False
        c.foo_called = False

        c.foo = foo2

        e.fire_callbacks("foo")
        assert not c.foo_called
        assert foo2.called

        out, err = capfd.readouterr()
        assert "foobar" in out

    def test_has_component(self):
        class Comp1(Component):
            def __init__(self,*args,**kwargs):
                super(Comp1, self).__init__(*args,**kwargs)

        class Comp2(Component):
            def __init__(self,*args,**kwargs):
                super(Comp2, self).__init__(*args,**kwargs)

        class Comp3(Component):
            def __init__(self,*args,**kwargs):
                super(Comp3, self).__init__(*args,**kwargs)

        c1 = Comp1()
        assert c1.has_component(Comp1) == None # because c1 has no entity

        c2 = Comp2()
        assert c2.has_component(Comp2) == None # because c2 has no entity

        e = Entity()
        c3 = Comp3(e)
        assert c3.entity == e
        assert c3.has_component(Comp3) == False # because c3 already has entity, but c3 is not yet added

        e.add_component(c1)
        assert c1.has_component(Comp1) == True
        assert c1.has_component(Comp2) == False
        assert c1.has_component(Comp3) == False
        assert c2.has_component(Comp1) == None
        assert c2.has_component(Comp2) == None
        assert c2.has_component(Comp3) == None
        assert c3.has_component(Comp1) == True
        assert c3.has_component(Comp2) == False
        assert c3.has_component(Comp3) == False

        e.add_component(c2)
        assert c1.has_component(Comp1) == True
        assert c1.has_component(Comp2) == True
        assert c1.has_component(Comp3) == False
        assert c2.has_component(Comp1) == True
        assert c2.has_component(Comp2) == True
        assert c2.has_component(Comp3) == False
        assert c3.has_component(Comp1) == True
        assert c3.has_component(Comp2) == True
        assert c3.has_component(Comp3) == False

        e.add_component(c3)
        assert c1.has_component(Comp1) == True
        assert c1.has_component(Comp2) == True
        assert c1.has_component(Comp3) == True
        assert c2.has_component(Comp1) == True
        assert c2.has_component(Comp2) == True
        assert c2.has_component(Comp3) == True
        assert c3.has_component(Comp1) == True
        assert c3.has_component(Comp2) == True
        assert c3.has_component(Comp3) == True

    def test_get_component(self):
        class Comp1(Component):
            def __init__(self,*args,**kwargs):
                super(Comp1, self).__init__(*args,**kwargs)

        class Comp2(Component):
            def __init__(self,*args,**kwargs):
                super(Comp2, self).__init__(*args,**kwargs)

        class Comp3(Component):
            def __init__(self,*args,**kwargs):
                super(Comp3, self).__init__(*args,**kwargs)

        c1 = Comp1()
        assert c1.get_component(Comp1) == None # because c1 has no entity

        c2 = Comp2()
        assert c2.get_component(Comp2) == None # because c2 has no entity

        e = Entity()
        c3 = Comp3(e)
        assert c3.entity == e
        assert c3.get_component(Comp3) == None # because c3 already has entity, but c3 is not yet added

        e.add_component(c1)
        assert c1.get_component(Comp1) == c1
        assert c1.get_component(Comp2) == None
        assert c1.get_component(Comp3) == None
        assert c2.get_component(Comp1) == None
        assert c2.get_component(Comp2) == None
        assert c2.get_component(Comp3) == None
        assert c3.get_component(Comp1) == c1
        assert c3.get_component(Comp2) == None
        assert c3.get_component(Comp3) == None

        e.add_component(c2)
        assert c1.get_component(Comp1) == c1
        assert c1.get_component(Comp2) == c2
        assert c1.get_component(Comp3) == None
        assert c2.get_component(Comp1) == c1
        assert c2.get_component(Comp2) == c2
        assert c2.get_component(Comp3) == None
        assert c3.get_component(Comp1) == c1
        assert c3.get_component(Comp2) == c2
        assert c3.get_component(Comp3) == None

        e.add_component(c3)
        assert c1.get_component(Comp1) == c1
        assert c1.get_component(Comp2) == c2
        assert c1.get_component(Comp3) == c3
        assert c2.get_component(Comp1) == c1
        assert c2.get_component(Comp2) == c2
        assert c2.get_component(Comp3) == c3
        assert c3.get_component(Comp1) == c1
        assert c3.get_component(Comp2) == c2
        assert c3.get_component(Comp3) == c3


    def test___uid__(self):
        e = Entity()
        c = Component()
        assert c.__uid__ == None
        e.add_component(c)
        assert e.__uid__ == c.__uid__

    def test___str__(self):
        c = Component()
        assert str(c) == "Component"