#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    

from collections import defaultdict

### useful for debugging purposes
### uncomment as needed
#
# from pprint import pprint
# import traceback
# import inspect

class Events(object):
    """docstring for Events"""
    def __init__(self):
        super(Events, self).__init__()
        self.callbacks = defaultdict(list)
        self.callbacks_once = defaultdict(list)

    def register_callback(self, key, callback):
        if callback not in self.callbacks[key]:
            self.callbacks[key].append(callback)

    def register_callback_once(self, key, callback):
        if callback not in self.callbacks_once[key]:
            self.callbacks_once[key].append(callback)

    def remove_callback(self, key, callback):
        if callback in self.callbacks[key]:
            self.callbacks[key].remove(callback)
        if callback in self.callbacks_once[key]:
            self.callbacks_once[key].remove(callback)

    def fire_callbacks(self, key, *args, **kwargs):
        if key in self.callbacks:
            for callback in self.callbacks[key]:
                callback(*args,**kwargs)
        if key in self.callbacks_once:
            for callback in self.callbacks_once[key]:
                callback(*args,**kwargs)
            self.callbacks_once[key] = []

    def fire_callbacks_pipeline(self, key, start_accum=None, *args, **kwargs):
        accum = start_accum
        if key in self.callbacks:
            for callback in self.callbacks[key]:
                accum = callback(accum,*args,**kwargs)

        if key in self.callbacks_once:
            for callback in self.callbacks_once[key]:
                accum = callback(accum,*args,**kwargs)
            self.callbacks_once[key] = []
        return accum
    # common events:
    # start        : called after setup/initialization complete, right before update loop starts
    # update(dt)   : called in every iteration of the update loop
    # quit(event)  : called when application quits
    # awake        : called after an entity is completed; breaths life to it, telling it
    #                everything it needs is available now; called right before return statement 
    #                in creation function of entity