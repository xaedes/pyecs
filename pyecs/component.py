#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division  

from events import Events

from collections import defaultdict
from .decorators import callback

class Component(Events):
    __added_components__ = defaultdict(list)
    @classmethod
    def _reset_global(CLS):
        Component.__added_components__ = defaultdict(list)
    """docstring for Component"""
    def __init__(self, entity = None):
        super(Component, self).__init__()
        self.entity = entity
        # self.__hotswap_callback__ = True
        self.__hotswap_callback__ = False

    def register_callbacks(self):
        callbacks = [method for method in dir(self) if callable(getattr(self, method))]
        this = self
        for callback in callbacks:
            method = getattr(self,callback)
            if hasattr(method,"__callback__"):
                key = method.__callback_key__

                if key is None:
                    key = callback
                
                if method.__component_callback__:
                    register_on = self
                else:
                    register_on = self.entity


                if self.__hotswap_callback__:                
                    # retrieves callback everytime, useful for hotswapping
                    def wrapper(callback):
                        def inner_wrapper(*args, **kwargs):
                            if hasattr(this,callback):
                                try:
                                    return getattr(this,callback)(*args, **kwargs)
                                except:
                                    import traceback
                                    print self
                                    traceback.print_exc()
                                    return None
                            else:
                                return None
                        return inner_wrapper

                    register_on.register_callback(callback, wrapper(callback))
                else:
                    # just use the callback
                    register_on.register_callback(key, method)

    def has_component(self, *args, **kwargs):
        if self.entity is not None:
            return self.entity.has_component(*args, **kwargs)
        else:
            return None

    def get_component(self, *args, **kwargs):
        if self.entity is not None:
            return self.entity.get_component(*args, **kwargs)
        else:
            return None

    def find_parent_entity_with_component(self, *args, **kwargs):
        if self.entity is not None:
            return self.entity.find_parent_entity_with_component(*args, **kwargs)
        else:
            return None
    def __str__(self):
        return type(self).__name__