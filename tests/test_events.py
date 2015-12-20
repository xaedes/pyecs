#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from pyecs import *
from pyecs.components import *

from collections import defaultdict
from testing import *

class TestEvents():
    def test_initial_state(self):
        e = Events()
        assert hasattr(e,"callbacks")
        assert type(e.callbacks) == defaultdict
        assert hasattr(e,"callbacks_once")
        assert type(e.callbacks_once) == defaultdict

    def test_register_callback(self):
        e = Events()
        def foo():
            pass
        e.register_callback("foo",foo)

        assert "foo" in e.callbacks
        assert foo in e.callbacks["foo"]

    def test_register_callback_once(self):
        e = Events()
        def foo():
            pass
        e.register_callback_once("foo",foo)

        assert "foo" in e.callbacks_once
        assert foo in e.callbacks_once["foo"]

    def test_remove_callback(self):
        e = Events()
        def foo():
            foo.called = True
        foo.called = False
        e.register_callback("foo",foo)

        assert "foo" in e.callbacks
        assert foo in e.callbacks["foo"]
        e.fire_callbacks("foo")
        assert foo.called

        e.remove_callback("foo", foo)

        # because we only remove from the list e.callbacks, an empty list will remain
        assert "foo" in e.callbacks 
        assert foo not in e.callbacks["foo"]
        assert e.callbacks["foo"] == []
        
        # assert the callback is actually removed
        foo.called = False
        e.fire_callbacks("foo")

        assert not foo.called

    def test_remove_callback_once(self):
        e = Events()
        def foo():
            foo.called = True
        e.register_callback_once("foo",foo)

        assert "foo" in e.callbacks_once
        assert foo in e.callbacks_once["foo"]

        e.remove_callback("foo", foo)

        # because we only remove from the list e.callbacks_once, an empty list will remain
        assert "foo" in e.callbacks_once 
        assert foo not in e.callbacks_once["foo"]
        assert e.callbacks_once["foo"] == []
        
        # assert the callback is actually removed
        foo.called = False
        e.fire_callbacks("foo")

        assert not foo.called

    def test_fire_callbacks(self):
        e = Events()
        def foo_0arg():
            foo_0arg.called = True
        foo_0arg.called = False
        e.register_callback("foo0",foo_0arg)

        e.fire_callbacks("foo0")
        assert foo_0arg.called
        
        def foo_1arg(foo):
            assert foo == 1
            foo_1arg.called = True
        foo_1arg.called = False
        e.register_callback("foo1",foo_1arg)

        e.fire_callbacks("foo1",1)
        assert foo_1arg.called

        def foo_2arg(foo,bar):
            assert foo == 1
            assert bar == 2
            foo_2arg.called = True
        foo_2arg.called = False
        e.register_callback("foo2",foo_2arg)

        e.fire_callbacks("foo2",1,bar=2)
        assert foo_2arg.called

    def test_fire_callbacks_once(self):
        e = Events()
        def foo():
            foo.called = True

        foo.called = False
        e.register_callback_once("foo",foo)
        assert foo in e.callbacks_once["foo"]
        
        e.fire_callbacks("foo")
        assert foo.called
        assert e.callbacks_once["foo"] == []
        
        # assert it is only called once
        foo.called = False
        e.fire_callbacks("foo")
        assert not foo.called
        