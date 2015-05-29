#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen

from pyecs import *

class Paddle(Component):
    """docstring for Paddle"""
    def __init__(self, *args,**kwargs):
        super(Paddle, self).__init__(*args,**kwargs)

