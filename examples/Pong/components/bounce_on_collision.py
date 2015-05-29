#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen

from pyecs import *
from pyecs.components import Pose,Size
from components import Velocity

class BounceOnCollision(Component):
    """docstring for BounceOnCollision"""
    def __init__(self, *args,**kwargs):
        super(BounceOnCollision, self).__init__(*args,**kwargs)
        self.last_pos = None

    @callback
    @with_components(required=[Pose])
    def update(self, dt, pose):
        self.last_pos = pose.x, pose.y

    @callback
    @with_components(required=[Pose,Velocity])
    def collide(self, other_entity, me, pose, velocity):
        if me != self.entity:
            return

        velocity.x *= -1
        if self.last_pos is not None:
            pose.x, pose.y = self.last_pos
