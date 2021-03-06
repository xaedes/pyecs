#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division

import pygame
import pyecs
from pyecs import Application, Entity, profile
from pyecs.components import *
from components import *

class Pong(Application):
    """docstring for Experiment"""
    def __init__(self):
        super(Pong, self).__init__()
        pygame.mouse.set_visible(False)

    def setup_main_entity(self):
        super(Pong, self).setup_main_entity()
        self.entity.add_component(Pygame())
        self.entity.add_component(ColorFill(color=(0,0,0)))
        self.entity.add_component(PropagateCallback(["update","draw","mousemotion"]))

    def setup_scene(self):
        super(Pong, self).setup_scene()
        self.entity.add_entity(self.create_ball())
        self.entity.add_entity(self.create_ai_paddle())
        self.entity.add_entity(self.create_human_paddle())

    def create_ball(self):
        entity = Entity()
        entity.add_component(Pose(100,100,0))
        entity.add_component(Size(size=15))
        entity.add_component(Ball())
        entity.add_component(Colliding(with_component_types=[Paddle]))
        entity.add_component(BounceOnCollision())
        entity.add_component(DrawSizeAsCircle(color=(255,255,255)))
        entity.add_component(Velocity(150,50))
        entity.add_component(BounceInside(*self.entity.get_component(Pygame).size))
        return entity

    def create_ai_paddle(self):
        entity = self.create_paddle('left')
        entity.add_component(FollowBall())
        return entity
        
    def create_human_paddle(self):
        entity = self.create_paddle('right')
        entity.add_component(FollowMouse())
        return entity

    def create_paddle(self,position,margin=10):
        entity = Entity()

        if position == 'left':
            x = margin
        elif position == 'right':
            x = self.entity.get_component(Pygame).size[0] - margin

        y = self.entity.get_component(Pygame).size[1] / 2

        entity.add_component(Paddle())
        entity.add_component(Pose(x,y,0))
        entity.add_component(Size(size=(10,100)))
        entity.add_component(DrawSizeAsRectangle(color=(255,255,255)))

        return entity


def main():
    # profile(Pong)
    Pong()

if __name__ == '__main__':
    main()
