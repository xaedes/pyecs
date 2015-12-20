#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from pyecs import *
from pyecs.components import *

import pyecs
import pyecs.application

from collections import defaultdict
from testing import *

from funcy import partial
import mock
class TestBackpropagateCallback():
    def test1(self):
        e = Entity()
        e2 = e.add_entity(Entity())
        foobar = mock.MagicMock()
        e.register_callback("foobar",foobar)
        c = e2.add_component(BackpropagateCallback("foobar"))
        e2.fire_callbacks("foobar")
        assert foobar.called

    def test2(self):
        e = Entity()
        e2 = e.add_entity(Entity())
        foobar1 = mock.MagicMock()
        foobar2 = mock.MagicMock()
        e.register_callback("foobar1",foobar1)
        e.register_callback("foobar2",foobar2)
        c = e2.add_component(BackpropagateCallback(["foobar1","foobar2"]))
        e2.fire_callbacks("foobar1")
        e2.fire_callbacks("foobar2")
        assert foobar1.called
        assert foobar2.called

    def test3(self):
        e = Entity()
        e2 = e.add_entity(Entity())
        foobar1 = mock.MagicMock()
        foobar2 = mock.MagicMock()
        e.register_callback("foobar1",foobar1)
        e.register_callback("foobar2",foobar2)
        c = e2.add_component(BackpropagateCallback(["foobar1"]))
        e2.fire_callbacks("foobar1")
        e2.fire_callbacks("foobar2")
        assert foobar1.called
        assert foobar2.not_called

    def test_str(self):
        assert str(BackpropagateCallback([])) == "BackpropagateCallback()"
        assert str(BackpropagateCallback("foobar1")) == "BackpropagateCallback(foobar1)"
        assert str(BackpropagateCallback(["foobar1"])) == "BackpropagateCallback(foobar1)"
        assert str(BackpropagateCallback(["foobar1","foobar2"])) == "BackpropagateCallback(foobar1,foobar2)"