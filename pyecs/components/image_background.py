#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen
import pygame

from pyecs import *


class ImageBackground(Component):
    """docstring for ImageBackground"""
    def __init__(self, filename, *args,**kwargs):
        super(ImageBackground, self).__init__(*args,**kwargs)
        # load image
        self.filename = filename
        self.img = pygame.image.load(self.filename)
        self.rect = self.img.get_rect()

    @callback
    def draw(self, screen):
        screen.blit(self.img, self.rect)

