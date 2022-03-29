# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 15:11:12 2022

@author: Gerrit Nowald
"""

import numpy as np
import matplotlib.pyplot as plt

from polygon import *

# -------------------------------------------------------
# input

# rectangle
b = 5
h = 2
vert = np.array([
    [0, 0],
    [b, 0],
    [b, h],
    [0, h],
    [0, 0],
    ])

point = np.array([5,2])

# -------------------------------------------------------
# function

def isPointOnEdge(vert, point):
    # computes the distance of a point from each edge. The point is on an edge,
    # if the point is between the vertices and the distance is smaller than the rounding error.
    # https://de.mathworks.com/matlabcentral/answers/351581-points-lying-within-line
    for i in range(vert.shape[0]-1):# for each edge
        j     = i + 1
        PQ    =    point - vert[i,]       # Line from P1 to Q
        P12   = vert[j,] - vert[i,]       # Line from P1 to P2
        L12   = np.sqrt(np.dot(P12,P12))  # length of P12
        N     = P12/L12                   # Normal along P12
        Dist  = abs(np.cross(N,PQ))     # Norm of distance vector
        Limit = np.spacing(np.max(np.abs([vert[i,], vert[j,], point])))*10   # Consider rounding errors
        on    = Dist < Limit
        if on:
            L = np.dot(PQ,N)            # Projection of the vector from P1 to Q on the line:
            on = (L>=0.0 and L<=L12)    # Consider end points  
            return on
    return on

# -------------------------------------------------------
# test

poly_plot(vert)

plt.plot(point[0],point[1],"r+")

print(f'Point on edge: {isPointOnEdge(vert, point)}')