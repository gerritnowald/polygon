# -*- coding: utf-8 -*-
"""
Created on Wed Dec 21 19:07:21 2022

@author: Gerrit Nowald
"""

class polygon():
    def __new__(cls, vert, axis=None):
        triangle = vert == 3
        solidrev = axis is not None
        if triangle and not solidrev:
            return super().__new__(_triangle)
        elif solidrev and not triangle:
            return super().__new__(_solid)
        elif solidrev and triangle:
            return super().__new__(_triangle_solid)
        else:
            return super().__new__(cls)
    def __init__(self, vert, axis=None):
        self.polygon_attribute = 1
    def polygon_method(self):
        print('polygon')

class _triangle(polygon):
    def __init__(self, vert, axis=None):
        super().__init__(vert, axis)
        self.triangle_attribute = 2
    def triangle_method(self):
        print('triangle')

class _solid(polygon):
    def __init__(self, vert, axis):
        super().__init__(vert, axis)
        self.solid_attribute = 3
    def solid_method(self):
        print('solid of revolution')

class _triangle_solid(_triangle, _solid):
    def __init__(self, vert, axis):
        super().__init__(vert, axis)


P = polygon(2)
# P = polygon(2,axis=0)
# P = polygon(3)
# P = polygon(3,axis=0)