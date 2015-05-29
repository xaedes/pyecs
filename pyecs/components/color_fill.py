#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen

import pygame

from pyecs import *

class ColorFill(Component):
    """docstring for ColorFill"""
    def __init__(self, color = (0,0,0), *args,**kwargs):
        super(ColorFill, self).__init__(*args,**kwargs)
        self.color = color

    @callback
    def draw(self, screen):
        screen.fill(self.color)
