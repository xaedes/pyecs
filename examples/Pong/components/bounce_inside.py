#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen

from pyecs import *
from pyecs.components import Pose,Size
from components import Velocity
class BounceInside(Component):
    """docstring for BounceInside"""
    def __init__(self, width, height, x=0, y=0, *args,**kwargs):
        super(BounceInside, self).__init__(*args,**kwargs)
        self.width, self.height = width, height
        self.x, self.y = x, y

    @callback
    @with_components(required=[Pose,Size,Velocity])
    def update(self, dt, pose, size, velocity):
        bbox = size.bounding_box()
        bbx, bby, bbw, bbh = bbox
        if bbx < self.x: 
            # bring position back inside
            pose.x += (self.x - bbx)
            # and bounce
            velocity.x *= -1
        elif bbx + bbw > self.x + self.width: 
            # bring position back inside
            pose.x += ((self.x + self.width) - (bbx + bbw))
            # and bounce
            velocity.x *= -1
        if bby < self.y: 
            # bring position back inside
            pose.y += (self.y - bby)
            # and bounce
            velocity.y *= -1
        elif bby + bbh > self.y + self.height: 
            # bring position back inside
            pose.y += ((self.y + self.height) - (bby + bbh))
            # and bounce
            velocity.y *= -1

