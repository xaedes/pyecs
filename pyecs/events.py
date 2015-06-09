#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    

from collections import defaultdict

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
