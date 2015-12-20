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
        self.imported_callable_attr_from_entity = ["has_component","get_component","find_parent_entity_with_component"]
        self.imported_attr_from_entity = ["__uid__","children","parent","components","tags"]

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


    def __getattr__(self, attr):
        '''
        @summary:    import attr from self.entity
        @param attr:
        @result: 
        '''
        if (attr in self.imported_attr_from_entity) or (attr in self.imported_callable_attr_from_entity):
            if (self.entity is not None) and hasattr(self.entity, attr):
                return getattr(self.entity, attr)
            else:
                if attr in self.imported_attr_from_entity:
                    return None
                else:
                    return lambda *args,**kwargs: None
        else:
            raise AttributeError()


    def __str__(self):
        return type(self).__name__
