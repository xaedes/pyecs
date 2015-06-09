#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen

from pyecs import *
from pyecs.components import Pose, Size

from time import time

class Draggable(Component):
    """docstring for Draggable"""
    def __init__(self, move_every = 1/60, *args,**kwargs):
        super(Draggable, self).__init__(*args,**kwargs)
        self.selected = False
        self.last_move = time()
        
        # specify how much time shall elapse between two Pose updates
        self.move_every = move_every

        # print "Draggable()"


    @callback    
    @with_components(required=[Pose,Size])
    def mousebuttondown(self, event, pose, size):
        # select 
        if event.button == 1: # left 
            # print "mousebuttondown", event
            if pose.distance_to_xy(*event.pos) < size.bounding_radius():
                # print "self.selected = True", pose.distance_to_xy(*event.pos), size.bounding_radius(), size.size, pose, event.pos
                self.selected = True
                self.entity.fire_callbacks("drag", self)
                    
    @callback    
    @with_components(required=[Pose,Size])
    def mousemotion(self, event, pose, size):
        # move if selected
        if self.selected:
            # print "mousemotion", event
            if time() - self.last_move > self.move_every:
                self.last_move = time()
                pose.x, pose.y = event.pos
                self.entity.fire_callbacks("dragging", self)
    
    @callback
    @with_components(required=[Pose,Size])
    def mousebuttonup(self, event, pose, size):
        # deselect
        if self.selected:
            # print "mousebuttonup", event
            self.selected = False
            self.entity.fire_callbacks("drop", self)


