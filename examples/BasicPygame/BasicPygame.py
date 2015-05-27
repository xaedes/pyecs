#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division

import pyecs
from pyecs import Application
# from pyecs.Components import Pygame

class BasicPygame(Application):
    """docstring for Experiment"""
    def __init__(self):
        super(BasicPygame, self).__init__()
    
    def setup_main_entity(self):
        super(BasicPygame, self).setup_main_entity()
        self.entity.add_component(pyecs.Components.Pygame())

    def setup_scene(self):
        super(BasicPygame, self).setup_scene()

def main():
    # profile(BasicPygame())
    BasicPygame()

if __name__ == '__main__':
    main()
