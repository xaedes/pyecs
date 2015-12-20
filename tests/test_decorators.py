#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from pyecs import *
from pyecs.components import *

from collections import defaultdict
from testing import *

class TestDecorators():
    def test_callback(self):
        class Foo(Component):
            @callback
            def bar(self):
                self.bar_called = True
        foo = Foo()
        e = Entity()
        e.add_component(foo)
        foo.bar_called = False
        e.fire_callbacks("bar")
        assert foo.bar_called == True

    def test_callback_key(self):
        class Foo(Component):
            @callback("foobar")
            def bar(self):
                self.bar_called = True
        foo = Foo()
        e = Entity()
        e.add_component(foo)
        foo.bar_called = False
        e.fire_callbacks("foobar")
        assert foo.bar_called == True

    def test_component_callback(self):
        class Foo(Component):
            @component_callback
            def bar(self):
                self.bar_called = True
        foo = Foo()
        foo.register_callbacks()
        foo.bar_called = False
        foo.fire_callbacks("bar")
        assert foo.bar_called == True
    def test_component_callback_key(self):
        class Foo(Component):
            @component_callback("foobar")
            def bar(self):
                self.bar_called = True
        foo = Foo()
        foo.register_callbacks()
        foo.bar_called = False
        foo.fire_callbacks("foobar")
        assert foo.bar_called == True

    def test_with_component(self):
        c = Component()
        class Foo(Component):
            @with_component(Component)
            def bar1(self,component):
                self.bar1_called = True
                return component
            @with_component(Component,required=True)
            def bar2(self,component):
                assert type(component) == Component
                assert component == c
                self.bar2_called = True
                return component
        foo = Foo()
        e = Entity()
        e.add_component(foo)
        foo.bar1_called = False
        foo.bar2_called = False
        assert foo.bar1() == None
        assert foo.bar2() == None
        assert foo.bar1_called
        assert not foo.bar2_called
        e.add_component(c)
        foo.bar1_called = False
        foo.bar2_called = False
        assert foo.bar1() == c
        assert foo.bar2() == c
        assert foo.bar1_called
        assert foo.bar2_called

    def test_with_components(self):
        c = Component()
        class Component2(Component):
            pass
        c2 = Component2()

        class Foo(Component):
            @with_components(optional=[Component,Component2])
            def bar0(self,component,component2):
                self.bar0_called = True
                return component,component2
            @with_components(optional=[Component],required=[Component2])
            def bar1(self,component,component2):
                assert type(component2) == Component2
                assert component2 == c2
                self.bar1_called = True
                return component,component2
            @with_components(required=[Component,Component2])
            def bar2(self,component,component2):
                assert type(component) == Component
                assert component == c
                assert type(component2) == Component2
                assert component2 == c2
                self.bar2_called = True
                return component,component2
            @with_components(optional=[Component2],required=[Component])
            def bar3(self,component,component2):
                assert type(component) == Component
                assert component == c
                self.bar3_called = True
                return component,component2
        foo = Foo()
        e = Entity()
        e.add_component(foo)
        foo.bar0_called = False
        foo.bar1_called = False
        foo.bar2_called = False
        foo.bar3_called = False
        assert foo.bar0() == (None, None)
        assert foo.bar1() == None
        assert foo.bar2() == None
        assert foo.bar3() == None
        assert foo.bar0_called
        assert not foo.bar1_called
        assert not foo.bar2_called
        assert not foo.bar3_called
        e.add_component(c)
        foo.bar0_called = False
        foo.bar1_called = False
        foo.bar2_called = False
        foo.bar3_called = False
        assert foo.bar0() == (c, None)
        assert foo.bar1() == None
        assert foo.bar2() == None
        assert foo.bar3() == (c, None)
        assert foo.bar0_called
        assert not foo.bar1_called
        assert not foo.bar2_called
        assert foo.bar3_called
        e.add_component(c2)
        foo.bar0_called = False
        foo.bar1_called = False
        foo.bar2_called = False
        foo.bar3_called = False
        assert foo.bar0() == (c, c2)
        assert foo.bar1() == (c, c2)
        assert foo.bar2() == (c, c2)
        assert foo.bar3() == (c, c2)
        assert foo.bar0_called
        assert foo.bar1_called
        assert foo.bar2_called
        assert foo.bar3_called
        e.remove_component(c)
        foo.bar0_called = False
        foo.bar1_called = False
        foo.bar2_called = False
        foo.bar3_called = False
        assert foo.bar0() == (None, c2)
        assert foo.bar1() == (None, c2)
        assert foo.bar2() == None
        assert foo.bar3() == None
        assert foo.bar0_called
        assert foo.bar1_called
        assert not foo.bar2_called
        assert not foo.bar3_called
