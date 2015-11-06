#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    

from time import time

from pyecs import *

import hotswap
hotswap.run()

def onHotswap():
    """Called when the source of this module has changed.

    When a function named 'onHotswap' is present in a module,
    this function is called after the module is reloaded.
    This should be used to trigger a redisplay of the screen or
    in general to discard cached results that are to be calculated
    again using the new method definitions.

    If onHotswap is not defined the module is reloaded anyway, but afterwards
    no further actions are performed. In this case the changed code has to be
    activated some other way like minimizing and restoring the window to be
    repainted.
    """
    onHotswap.notify = True

onHotswap.notify = False

class Application(object):
    """docstring for Application"""
    def __init__(self, auto_spin = True):
        super(Application, self).__init__()
        Application.instance = self
        
        self.done = False

        self.setup_main_entity()
        self.setup_scene()


        self.entity.fire_callbacks("setup")
        self.register_events()

        if auto_spin:
            self.spin()

    def on_hotswap(self):
        # self.setup_scene() # can be useful
        self.entity.fire_callbacks("hotswap")

    def setup_main_entity(self):
        self.entity = Entity()

    def setup_scene(self):
        pass

    def register_events(self):
        self.entity.register_callback("quit", self.on_quit)

    def on_quit(self, event):
        self.done = True

    def update(self, dt):
        self.entity.fire_callbacks("update", dt)

    def start(self):
        self.entity.fire_callbacks("start")

    def quit(self):
        self.entity.fire_callbacks("quit", None)

    def spin(self):
        # Loop until the user clicks the close button.
        self.done = False
         
        # start
        self.start()

        # prepare time measurement
        start_time = time()
        self.last_time = time()
        # -------- Main Program Loop -----------
        while not self.done:
            # compute dt
            dt = time()-self.last_time
            self.last_time = time()

            # trigger hotswap event
            if onHotswap.notify:
                onHotswap.notify = False
                self.on_hotswap()

            # update and draw
            self.update(dt)

        # quit
        self.quit()


def profile(operation, filename='profile'):
    import cProfile
    pr = cProfile.Profile()
    pr.enable()
    try:
        operation()
    finally:
        pr.disable()
        pr.dump_stats(filename)

def main():
    # profile(App)
    App()

if __name__ == '__main__':
    main()

