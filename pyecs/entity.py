#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division

from events import Events

from collections import defaultdict


class Entity(Events):
    __uid__ = 0
    __tags__ = defaultdict(set)
    """docstring for Entity"""
    def __init__(self, parent = None):
        super(Entity, self).__init__()
        self.uid = Entity.__uid__
        Entity.__uid__ += 1

        self.components = defaultdict(list)
        self.parent = parent
        self.children = list()
        self.tags = set()

    def add_tag(self, tag):
        Entity.__tags__[tag].add(self)
        self.tags.add(tag)

    def remove_tag(self, tag):
        if tag in self.tags:
            Entity.__tags__[tag].remove(self)



    def add_component(self, component):
        if component not in self.components[type(component)]:
            component.entity = self
            component.register_callbacks()
            self.components[type(component)].append(component)
            self.fire_callbacks("component_added", component, component.entity)

            return component
        return None

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
        entity.fire_callbacks("entity_added", self, entity)
        
        return entity
        
    def has_component(self, component_type):
        return len(self.components[component_type])>0

    def get_component(self, component_type):
        if len(self.components[component_type])>0:
            return self.components[component_type][0]
        else:
            return None

    def find_root(self):
        entity = self
        while entity.parent is not None:
            entity = entity.parent

        return entity

    def find_all_entities_with_component(self, component_type):
        return self.find_root().find_entities_with_component(component_type)

    def find_entities_with_component(self, component_type):
        return self.find_entities(lambda entity: entity.has_component(component_type))

    def first_or_none(self, lst):
        if len(lst) == 0:
            return None
        else:
            return lst[0]

    def find_entity_with_component(self, component_type):
        return self.first_or_none(self.find_entities_with_component(component_type))

    def find_entities_with_tag(self, tag):
        return Entity.__tags__[tag]

    def find_entity_with_tag(self, tag):
        return self.first_or_none(list(self.find_entities_with_tag(tag)))

    def find_entities_with_tags(self, tags):
        # finds all entities that have all of the given tags
        entities = None
        for tag in tags:
            if entities is None:
                entities = self.find_entities_with_tag(tag).copy()
            else:
                entities.intersection_update(self.find_entities_with_tag(tag))
        return entities

    def find_entity_with_tags(self, tags):
        return self.first_or_none(list(self.find_entities_with_tags(tags)))


    def find_entities(self, predicate):
        entities = []
        stack = [self]
        while len(stack) > 0:
            entity = stack.pop()
            if predicate(entity):
                entities.append(entity)

            stack.extend([child for child in entity.children])

        return entities
