#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen

from pyecs import *
from pyecs.components import Pose

class Velocity(Component):
    """docstring for Velocity"""
    def __init__(self, x, y, *args,**kwargs):
        super(Velocity, self).__init__(*args,**kwargs)
        self.x = x
        self.y = y

    @callback
    @with_components(required=[Pose])
    def update(self, dt, pose):
        pose.x += self.x * dt
        pose.y += self.y * dt