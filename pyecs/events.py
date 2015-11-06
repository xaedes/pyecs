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

    def init_callback_key(self, key):
        self.callbacks[key] = []

    def register_callback(self, key, callback):
        if callback not in self.callbacks[key]:
            self.callbacks[key].append(callback)

    def remove_callback(self, key, callback):
        if callback in self.callbacks[key]:
            self.callbacks[key].remove(callback)

    def fire_callbacks(self, key, *args, **kwargs):
        if key in self.callbacks:
            for callback in self.callbacks[key]:
                callback(*args,**kwargs)

    # common events:
    # start        : called after setup/initialization complete, right before update loop starts
    # update(dt)   : called in every iteration of the update loop
    # quit(event)  : called when application quits
    # awake        : called after an entity is completed; breaths life to it, telling it
    #                everything it needs is available now; called right before return statement 
    #                in creation function of entity