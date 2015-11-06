#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen

import types

from pyecs import *

class PropagateCallback(Component):
    """docstring for PropagateCallback"""
    def __init__(self, key, *args,**kwargs):
        super(PropagateCallback, self).__init__(*args,**kwargs)
        if type(key) == list:
            self.keys = key
            for k in key:
                self.prop(k)
        else:
            self.keys = [key]
            self.prop(key)

    def prop(self, key):
        @callback
        def propagate(self, *args,**kwargs):
            for child in self.entity.children:
                child.fire_callbacks(key, *args,**kwargs)

        self.__dict__[key] = types.MethodType(propagate, self)


    def __str__(self):
        return "%s(%s)" % (super(type(self),self).__str__(), ",".join(self.keys))
