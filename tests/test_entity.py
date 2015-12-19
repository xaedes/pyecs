#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from pyecs import Entity
from collections import defaultdict
from testing import *

class TestEntity():
    def test_initial_state(self):
        e = Entity()
        assert hasattr(e, "uid")
        assert type(e.uid) == int
        assert hasattr(e, "components")
        assert type(e.components) == defaultdict
        assert hasattr(e, "parent")
        assert e.parent == None
        assert hasattr(e, "children")
        assert type(e.children) == list
        assert hasattr(e, "tags")
        assert type(e.tags) == set
