#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen

import types

from pyecs import *

class BackpropagateCallback(Component):
    """docstring for BackpropagateCallback"""
    def __init__(self, key, *args,**kwargs):
        super(BackpropagateCallback, self).__init__(*args,**kwargs)

        @callback
        def propagate(self, *args,**kwargs):
        	self.entity.parent.fire_callbacks_no_propagation(key, *args,**kwargs)

        self.__dict__[key] = types.MethodType(propagate, self)
        # self[key] = propagate
