# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 20:00:48 2022

@author: Gerrit Nowald
"""

import numpy as np
import matplotlib.pyplot as plt
import polygon as pg

# -------------------------------------------------------
# Input

Point = [1, 2]


# rectangle
# b = 5
# h = 2
# vert = np.array([
#     [0, 0],
#     [b, 0],
#     [b, h],
#     [0, h],
#     ])


# triangle
a = 3
h = 7
vert = np.array([
    [0, 0],
    [a, 0],
    [a/2, h],
    ])

# -------------------------------------------------------
# Function

def point_in_polygon(vert, point):
    """
    alorithm by ClaasM https://github.com/ClaasM/Algorithms/
    Taken from https://www.algorithms-and-technologies.com/point_in_polygon/python
    
    Raycasting Algorithm, performs the even-odd-rule to find out whether a point is in a given polygon.
    A point is in a polygon, if a line from the point to infinity crosses the polygon an odd number of times.
    This runs in O(n) where n is the number of edges of the polygon.
    
    :param vert:    an array representation of the polygon where vert[i,0] is the x Value of the i-th point and vert[i,1] is the y Value.
    :param point:   an array representation of the point where point[0] is its x Value and point[1] is its y Value
    :return:        whether the point is in the polygon (not on the edge, just turn < into <= and > into >= for that)
    """

    odd = False    
    for j in range(vert.shape[0]-1):    # for each edge
        i = j + 1
        # If a line from the point into infinity crosses this edge
        # One point needs to be above, one below our y coordinate
        # ...and the edge doesn't cross our y corrdinate before our x coordinate (but between our x coordinate and infinity)
        if ( 
            ( (vert[i,1] > point[1]) != (vert[j,1] > point[1]) ) and
            ( point[0] < (vert[j,0]-vert[i,0])*(point[1]-vert[i,1])/(vert[j,1]-vert[i,1]) + vert[i,0] ) 
            ):
            odd = not odd
    return odd

# -------------------------------------------------------
# Test

pg.poly_plot(vert)
plt.plot(Point[0],Point[1],"+")

vert = pg._close_loop(vert)

print(f'Point in polygon: {point_in_polygon(vert, Point)}')