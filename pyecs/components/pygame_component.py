#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division
import pygame

from pyecs import *

class Pygame(Component):
    """docstring for Pygame"""
    def __init__(self, size = (640, 480), caption = "My Game", fps = 60, *args,**kwargs):
        super(Pygame, self).__init__(*args,**kwargs)
        # Set the width and height of the screen [width, height]
        self.size = size
        self.caption = caption
        self.pygame_mappings = dict({
            pygame.QUIT: "quit",
            pygame.ACTIVEEVENT: "activeevent",
            pygame.KEYDOWN: "keydown",
            pygame.KEYUP: "keyup",
            pygame.MOUSEMOTION: "mousemotion",
            pygame.MOUSEBUTTONUP: "mousebuttonup",
            pygame.MOUSEBUTTONDOWN: "mousebuttondown",
            pygame.JOYAXISMOTION: "joyaxismotion",
            pygame.JOYBALLMOTION: "joyballmotion",
            pygame.JOYHATMOTION: "joyhatmotion",
            pygame.JOYBUTTONUP: "joybuttonup",
            pygame.JOYBUTTONDOWN: "joybuttondown",
            pygame.VIDEORESIZE: "videoresize",
            pygame.VIDEOEXPOSE: "videoexpose",
            pygame.USEREVENT: "userevent"
            })

        # Used to manage how fast the screen updates
        self.fps = fps
        self.clock = pygame.time.Clock()

    @callback
    def setup(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.caption)

    @callback
    def quit(self, event):
        # Close the window and quit.
        # If you forget this line, the program will 'hang'
        # on exit if running from IDLE.
        pygame.quit()

    @callback
    def update(self, dt):
        self.entity.fire_callbacks("draw", self.screen)

        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # get mouse info
        cursor = pygame.mouse.get_pos()
        buttons = pygame.mouse.get_pressed() 
        # (left_button, middle_button, right_button) = buttons
        # get key info
        keys = pygame.key.get_pressed()        
        self.entity.fire_callbacks("input", cursor, buttons, keys)

        # Pump pygame events 
        for event in pygame.event.get(): # User did something
            if event.type in self.pygame_mappings:
                self.entity.fire_callbacks(self.pygame_mappings[event.type], event)
        
        # Limit FPS
        self.clock.tick(self.fps)

    @callback
    def component_added(self, component, entity):
        if self == component:
            component.setup()

    @callback
    def hotswap(self):
        self.setup()
