#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen

from pyecs import *

class HotswapController(Component):
    """docstring for HotswapController"""
    def __init__(self, *args,**kwargs):
        super(HotswapController, self).__init__(*args,**kwargs)

    @callback
    def update(self, dt):
        pass
        # you can set properties of the entity here, hotswapping will apply them