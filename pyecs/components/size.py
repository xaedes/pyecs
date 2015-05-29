#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen
from pyecs import *

class Size(Component):
    """docstring for Size"""
    def __init__(self, size, *args,**kwargs):
        super(Size, self).__init__(*args,**kwargs)
        self.size = size
