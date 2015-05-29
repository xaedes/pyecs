#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen
import pygame
from pyecs import *
from pyecs.components import Pose, Size

class DrawSizeAsCircle(Component):
    """docstring for DrawSizeAsCircle"""
    def __init__(self, color=(255,255,255), *args,**kwargs):
        super(DrawSizeAsCircle, self).__init__(*args,**kwargs)
        self.color = color

    @callback
    @with_components(required=[Pose,Size])
    def draw(self, screen, pose, size):
        pygame.draw.circle(screen, self.color, (int(pose.x+0.5), int(pose.y+0.5)), int(size.size/2+0.5), 1)
