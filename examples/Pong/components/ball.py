#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen

from pyecs import *

class Ball(Component):
    """docstring for Ball"""
    def __init__(self, *args,**kwargs):
        super(Ball, self).__init__(*args,**kwargs)

