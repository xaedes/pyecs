#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen

from pyecs import *
from pyecs.components import Pose
from components import Ball

class FollowBall(Component):
    """docstring for FollowBall"""
    def __init__(self, *args,**kwargs):
        super(FollowBall, self).__init__(*args,**kwargs)
        self.ball = None

    @callback
    def entity_added(self, parent, entity):
        if self.entity == entity:
            self.ball = self.entity.find_root().find_entity_with_component(Ball)

    @callback
    @with_components(required=[Pose])
    def update(self, dt, pose):
        if self.ball is not None:
            pose.y = self.ball.get_component(Pose).y

