#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    

from funcy import decorator, any

@decorator
def with_component(function, component_type, required = False):
    self = function._args[0]

    # get component
    component = self.get_component(component_type)
    
    # check if required component is not available
    if required and (component is None):
        return None

    # populate function's kwargs with components
    component_name = component_type.__name__.lower()
    function._kwargs[component_name] = component


    return function()

@decorator
def with_components(function, optional = [], required = []):
    self = function._args[0]

    # get components
    optional = dict([(component_type.__name__.lower(),self.get_component(component_type)) for component_type in optional])
    required = dict([(component_type.__name__.lower(),self.get_component(component_type)) for component_type in required])

    # check if any required component is not available
    if any(component is None for component in required.itervalues()):
        return None

    # populate function's kwargs with components
    for component_name, component in optional.iteritems():
        function._kwargs[component_name] = component

    for component_name, component in required.iteritems():
        function._kwargs[component_name] = component


    return function()

def callback(function):
    if type(function) == str:
        key = function
        def outer(function):
            function.__callback__ = True
            function.__component_callback__ = False
            function.__callback_key__ = key

            return function
        return outer
    else:
        key = None
        
    function.__callback__ = True
    function.__component_callback__ = False
    function.__callback_key__ = key
    return function

def component_callback(function):
    if type(function) == str:
        key = function
        def outer(function):
            function.__callback__ = True
            function.__component_callback__ = True
            function.__callback_key__ = key
            return function
        return outer
    else:
        key = None

    function.__callback__ = True
    function.__component_callback__ = True
    function.__callback_key__ = key
    return function
