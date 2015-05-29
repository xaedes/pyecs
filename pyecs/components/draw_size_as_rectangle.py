#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen
import pygame
from pyecs import *
from pyecs.components import Pose, Size

class DrawSizeAsRectangle(Component):
    """docstring for DrawSizeAsRectangle"""
    def __init__(self, color=(255,255,255), *args,**kwargs):
        super(DrawSizeAsRectangle, self).__init__(*args,**kwargs)
        self.color = color

    @callback
    @with_components(required=[Pose,Size])
    def draw(self, screen, pose, size):
        bbox = size.bounding_box()
        pygame.draw.rect(screen, self.color, bbox, 1)
