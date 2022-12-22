# -*- coding: utf-8 -*-
"""
https://stackoverflow.com/questions/74874119/python-overlapping-non-exclusive-inheritance-to-have-methods-available-based

@author: Gerrit Nowald
"""

class _polygonBase():
    def __init__(self, vert, axis):
        self.polygon_attribute = 1
    def polygon_method(self):
        print('polygon')

class _triangle(_polygonBase):
    def __init__(self, vert, axis):
        super().__init__(vert, axis)
        self.triangle_attribute = 2
    def triangle_method(self):
        print('triangle')

class _solid(_polygonBase):
    def __init__(self, vert, axis):
        super().__init__(vert, axis)
        self.solid_attribute = 3
    def solid_method(self):
        print('solid of revolution')

class _solid_and_triangle(_triangle, _solid):
    def __init__(self, vert, axis):
        super().__init__(vert, axis)

class polygon():
    def __new__(self, vert, axis=None):
        isTriangle = vert == 3
        isSolidRev = axis is not None
        if isTriangle and not isSolidRev:
            return _triangle(vert, axis)
        elif isSolidRev and not isTriangle:
            return _solid(vert, axis)
        elif isSolidRev and isTriangle:
            return _solid_and_triangle(vert, axis)
        else:
            return _polygonBase(vert, axis)


# P = polygon(2)
# P = polygon(2,axis=0)
# P = polygon(3)
P = polygon(3,axis=0)
