#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division

import pyecs
from pyecs import Application, Entity
from pyecs.components import *

class BasicPygame(Application):
    """docstring for Experiment"""
    def __init__(self):
        super(BasicPygame, self).__init__()
    
    def setup_main_entity(self):
        super(BasicPygame, self).setup_main_entity()
        self.entity.add_component(Pygame())
        self.entity.add_component(ColorFill(color=(0,0,0)))
        self.entity.add_component(PropagateCallback(["update","draw","mousemotion","mousebuttondown","mousebuttonup"]))

    def setup_scene(self):
        super(BasicPygame, self).setup_scene()
        self.entity.add_entity(self.create_draggable_circle())

    def create_draggable_circle(self):
        entity = Entity()
        entity.add_component(Pose(100,100,0))
        entity.add_component(Size(size=15))
        entity.add_component(DrawSizeAsCircle(color=(255,0,0)))
        entity.add_component(Draggable())
        return entity

def main():
    # profile(BasicPygame())
    BasicPygame()

if __name__ == '__main__':
    main()
