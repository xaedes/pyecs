#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen

import pygame
from pyecs import *
from pyecs.components import Pose,Size
from components import Velocity

class Colliding(Component):
    """docstring for Colliding"""
    def __init__(self, with_component_types=[], *args,**kwargs):
        super(Colliding, self).__init__(*args,**kwargs)
        self.with_component_types = with_component_types

    @callback
    @with_components(required=[Pose,Size])
    def update(self, dt, pose, size):
        bbox = size.bounding_box()
        rect = pygame.Rect(*bbox)
        entities = []
        for component_type in self.with_component_types:
            entities.extend(
                [e for e in self.entity.find_all_entities_with_component(component_type)
                    if (e.uid != self.entity.uid) 
                ])

        for entity in entities:
            bbox2 = entity.get_component(Size).bounding_box()
            if rect.colliderect(pygame.Rect(*bbox2)):
                self.entity.fire_callbacks("collide", entity, self.entity)
