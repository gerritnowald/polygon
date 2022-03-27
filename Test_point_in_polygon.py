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
# Vert = np.array([
#     [0, 0],
#     [b, 0],
#     [b, h],
#     [0, h],
#     ])


# triangle
a = 3
h = 7
Vert = np.array([
    [0, 0],
    [a, 0],
    [a/2, h],
    ])

# -------------------------------------------------------
# Function

def point_in_polygon(polygon, point):
    """
    alorithm by ClaasM https://github.com/ClaasM/Algorithms/
    Taken from https://www.algorithms-and-technologies.com/point_in_polygon/python
    
    Raycasting Algorithm, performs the even-odd-rule to find out whether a point is in a given polygon.
    This runs in O(n) where n is the number of edges of the polygon.
     *
    :param polygon: an array representation of the polygon where polygon[i][0] is the x Value of the i-th point and polygon[i][1] is the y Value.
    :param point:   an array representation of the point where point[0] is its x Value and point[1] is its y Value
    :return: whether the point is in the polygon (not on the edge, just turn < into <= and > into >= for that)
    """

    # A point is in a polygon if a line from the point to infinity crosses the polygon an odd number of times
    odd = False
    # For each edge (In this case for each point of the polygon and the previous one)
    i = 0
    j = len(polygon) - 1
    while i < len(polygon) - 1:
        i += 1
        # If a line from the point into infinity crosses this edge
        # One point needs to be above, one below our y coordinate
        # ...and the edge doesn't cross our Y corrdinate before our x coordinate (but between our x coordinate and infinity)
        if ( ((polygon[i][1] > point[1]) != (polygon[j][1] > point[1])) and (point[0] < ((polygon[j][0] - polygon[i][0]) * (point[1] - polygon[i][1]) / (polygon[j][1] - polygon[i][1])) + polygon[i][0]) ):
            odd = not odd   # Invert odd
        j = i
    return odd  # If the number of crossings was odd, the point is in the polygon

# -------------------------------------------------------
# Test

pg.poly_plot(Vert)
plt.plot(Point[0],Point[1],"+")

Vert = pg._close_loop(Vert)

print(f'Point in polygon: {point_in_polygon(Vert, Point)}')