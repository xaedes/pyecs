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
        
        # specify how much time shall elapse between to Pose updates
        self.move_every = move_every


    @callback    
    @with_components(required=[Pose,Size])
    def mousebuttondown(self, event, pose, size):
        # select 
        if event.button == 1: # left 
            if pose.distance_to_xy(*event.pos) < size.size:
                self.selected = True
                    
    @callback    
    @with_components(required=[Pose,Size])
    def mousemotion(self, event, pose, size):
        # move if selected
        if self.selected:
            if time() - self.last_move > self.move_every:
                self.last_move = time()
                pose.x, pose.y = event.pos
    
    @callback
    @with_components(required=[Pose,Size])
    def mousebuttonup(self, event, pose, size):
        # deselect
        self.selected = False


