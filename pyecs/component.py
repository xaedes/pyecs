#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    

from collections import defaultdict
from .decorators import callback

class Component(object):
    __added_components__ = defaultdict(list)
    """docstring for Component"""
    def __init__(self, entity = None):
        super(Component, self).__init__()
        self.entity = entity
        self.__hotswap_callback__ = False

    def register_callbacks(self):
        callbacks = [method for method in dir(self) if callable(getattr(self, method))]
        this = self
        for callback in callbacks:
            if hasattr(getattr(self,callback),"__callback__"):
                if self.__hotswap_callback__:                
                    # retrieves callback everytime, useful for hotswapping
                    def wrapper(callback):
                        def inner_wrapper(*args, **kwargs):
                            if hasattr(this,callback):
                                try:
                                    return getattr(this,callback)(*args, **kwargs)
                                except:
                                    import traceback
                                    traceback.print_exc()
                                    return None
                            else:
                                return None
                        return inner_wrapper
                    self.entity.register_callback(callback, wrapper(callback))
                else:
                    # just use the callback
                    self.entity.register_callback(callback, getattr(this,callback))

    def get_component(self, component_type):
        if self.entity is not None:
            return self.entity.get_component(component_type)
        else:
            return None

    def find_parent_entity_with_component(self, component_type):
        if self.entity is not None:
            return self.entity.find_parent_entity_with_component(component_type)
        else:
            return None

    @callback
    def component_added(self, component, entity):
        if self == component:
            Component.__added_components__[type(component)].append(component)

    @callback
    def component_removed(self, component, entity):
        if self == component:
            Component.__added_components__[type(component)].remove(component)
