#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division

from events import Events
from component import Component

from collections import defaultdict


class Entity(Events):
    __uid__ = 0
    __tags__ = defaultdict(set)
    @classmethod
    def _reset_global(CLS):
        Entity.__uid__ = 0
        Entity.__tags__ = defaultdict(set)

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
            self.tags.remove(tag)


    def add_component(self, component):
        if component not in self.components[type(component)]:
            component.entity = self
            component.register_callbacks()
            self.components[type(component)].append(component)
            Component.__added_components__[type(component)].append(component)
            self.fire_callbacks("component_added", component, component.entity)
            component.fire_callbacks("component_attached")
            return component
        return None

    def remove_component(self, component):
        if component in self.components[type(component)]:
            ent = component.entity
            component.entity = None
            self.components[type(component)].remove(component)
            Component.__added_components__[type(component)].remove(component)
            self.fire_callbacks("component_removed", component, self)
            component.fire_callbacks("component_detached", ent)

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

    def remove_entity(self, entity):
        if entity in self.children:
            entity.parent = None
            self.children.remove(entity)
            entity.fire_callbacks("entity_removed", self, entity)
            return True   # was removed
        else:
            return False  # was not removed

    def remove_from_parent(self):
        if self.parent is not None:
            return self.parent.remove_entity(self)
        else:
            return False # was not removed

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

    def entity_path(self):
        path = [self]

        entity = self
        while entity.parent is not None:
            entity = entity.parent
            path.append(entity)
        path = reversed(path)
        return path

    def uid_path(self):
        path = '.'.join([str(e.uid) for e in self.entity_path()])

        return path

    def find_all_entities_with_component(self, component_type):
        return self.find_root().find_entities_with_component(component_type)

    def find_entities_with_component(self, component_type):
        return self.find_entities(lambda entity: entity.has_component(component_type))


    def find_entity_with_component(self, component_type):
        return self.first_or_none(self.find_entities_with_component(component_type))

    @classmethod
    def first_or_none(CLS, lst):
        if len(lst) == 0:
            return None
        else:
            return lst[0]

    @classmethod
    def find_entities_with_tag(CLS, tag):
        return Entity.__tags__[tag]

    @classmethod
    def find_entity_with_tag(CLS, tag):
        return CLS.first_or_none(list(CLS.find_entities_with_tag(tag)))

    @classmethod
    def find_entities_with_tags(CLS, tags):
        # finds all entities that have all of the given tags
        entities = None
        for tag in tags:
            if entities is None:
                entities = CLS.find_entities_with_tag(tag).copy()
            else:
                entities.intersection_update(CLS.find_entities_with_tag(tag))
        return entities

    @classmethod
    def find_entity_with_tags(CLS, tags):
        return CLS.first_or_none(list(CLS.find_entities_with_tags(tags)))


    def find_entities(self, predicate):
        entities = []
        stack = [self]
        while len(stack) > 0:
            entity = stack.pop()
            if predicate(entity):
                entities.append(entity)

            stack.extend(reversed(entity.children))

        return entities
        
    def traverse_entities(self, callback):
        stack = [self]
        while len(stack)>0:
            entity = stack.pop()
            stack.extend(reversed(entity.children))

            callback(entity)

    def traverse_entities_accum(self, callback, accum = None):
        stack = [self]
        while len(stack)>0:
            entity = stack.pop()
            for child in reversed(entity.children):
                stack.append(child)

            accum = callback(entity, accum)

        return accum
        
    def all_components(self):
        components = [components for component_type,components in self.components.iteritems()]
        components = [item for sublist in components for item in sublist] #http://stackoverflow.com/a/952952/798588

        return components
		
    def __str__(self):
        return "Entity %s, %s" % (self.uid_path(),  self.print_components(_return=True))

    def print_components(self, _return=False):
        components = map(str,self.all_components())
        components = ', '.join(components)
        if _return:
            return components
        else:
            print components

    def print_structure(self, _return=False):
        lines = self.traverse_entities_accum(
            lambda entity,lines: 
                lines + [(entity.uid_path(), entity.print_components(_return=True))],
            [])

        fst_column_width = max([len(a) for a,b in lines])
        fst_column_width += 4

        lines = [a + str(' '*(fst_column_width-len(a))) + b  for a,b in lines]

        lines = '\n'.join(lines)

        if _return:
            return lines
        else:
            print lines
