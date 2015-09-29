#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen

from pyecs import *
from pyecs.components import *

class Keyboard(Component):
    """docstring for Keyboard"""
    def __init__(self, *args,**kwargs):
        super(Keyboard, self).__init__(*args,**kwargs)
        self.pressed = set()

    @callback
    def keydown(self, event):
        self.pressed.add(event.key)

    @callback
    def keyup(self, event):
        if event.key in self.pressed:
            self.pressed.remove(event.key)
