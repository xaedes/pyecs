#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division

from Events import Events

from collections import defaultdict

class Entity(Events):
    """docstring for Entity"""
    def __init__(self, parent = None):
        super(Entity, self).__init__()
        self.components = defaultdict(list)
        self.parent = parent
        self.children = list()

    def fire_callbacks(self, key, *args, **kwargs):
        # fire callbacks in this entity
        if key in self.callbacks:
            for callback in self.callbacks[key]:
                callback(*args,**kwargs)

        # propagate to children
        for child in self.children:
            child.fire_callbacks(key, *args, **kwargs)

    def add_component(self, component):
        if component not in self.components[type(component)]:
            component.entity = self
            component.register_callbacks()
            self.components[type(component)].append(component)
            self.fire_callbacks("component_added", component, component.entity)

    def remove_component(self, component):
        if component in self.components[type(component)]:
            self.components[type(component)].remove(component)
            component.entity = None
            self.fire_callbacks("component_removed", component, self)

    def find_parent_entity_with_component(self, component_type):
        entity = self.parent
        while entity is not None and not entity.has_component(component_type):
            entity = entity.parent
        
        return entity

    def add_entity(self, entity):
        self.children.append(entity)
        entity.parent = self
        self.fire_callbacks("entity_added", self, entity)
        
    def has_component(self, component_type):
        return len(self.components[component_type])>0

    def get_component(self, component_type):
        if len(self.components[component_type])>0:
            return self.components[component_type][0]
        else:
            return None