#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen
from numbers import Number

from pyecs import *
from pyecs.components import Pose

class Size(Component):
    """docstring for Size"""
    def __init__(self, size, *args,**kwargs):
        super(Size, self).__init__(*args,**kwargs)
        self.size = size

    @with_components(required=[Pose])
    def bounding_box(self, pose):
    	if isinstance(self.size, Number):
    		# one-dimensional size
    		return (pose.x - self.size/2, pose.y - self.size/2, self.size, self.size)
    	elif type(self.size) == tuple:
    		# two-dimensional size
    		return (pose.x - self.size[0]/2, pose.y - self.size[1]/2, self.size[0], self.size[1])