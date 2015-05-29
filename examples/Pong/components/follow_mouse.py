#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen

from pyecs import *
from pyecs.components import Pose

class FollowMouse(Component):
    """docstring for FollowMouse"""
    def __init__(self, *args,**kwargs):
        super(FollowMouse, self).__init__(*args,**kwargs)

    @callback
    @with_components(required=[Pose])
    def mousemotion(self, event, pose):
        pose.y = event.pos[1]
