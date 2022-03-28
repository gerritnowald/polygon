# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 20:00:48 2022

@author: Gerrit Nowald
"""

import numpy as np
import matplotlib.pyplot as plt
import polygon as pg

import time

# -------------------------------------------------------
# Input

N = 1000



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
# Points = np.hstack(( np.random.rand(N,1)*5-1, np.random.rand(N,1)*10-1.5 ))
# a = 3
# h = 7
# vert = np.array([
#     [0, 0],
#     [a, 0],
#     [a/2, h],
#     ])

# heart
Points = np.hstack(( np.random.rand(N,1)*6-3, np.random.rand(N,1)*10-2 ))
vert = np.array([
    [0, 0],
    [1.75,4],
    [1.5,6],
    [1,7],
    [0.25,6],
    [0,5],
    [-0.25,6],
    [-1,7],
    [-1.5,6],
    [-1.75,4],
    ])

# -------------------------------------------------------
# Function

def point_in_polygon(vert, point=[0,0]):
    """
    A point is in a polygon, if a line from the point to infinity crosses the polygon an odd number of times.
    Here, the line goes parallel to the x-axis in positive x-direction.
    
    vert  = [x,y]: 2D array of columns of 2D-Coordinates of vertices
    point = [x,y]: point to be tested
    odd (Boolean): whether the point is in the polygon (not on the edge)
    
    adapted from ClaasM https://www.algorithms-and-technologies.com/point_in_polygon/python
    """
    odd = False    
    for j in range(vert.shape[0]-1):    # for each edge check if the line crosses
        i = j + 1                       # next vertice
        if vert[j,1] != vert[i,1]:      # edge not parallel to x-axis (singularity)
            # point between y-coordinates of edge
            if (vert[i,1] > point[1]) != (vert[j,1] > point[1]):
                # x-coordinate of intersection
                Qx = (vert[j,0]-vert[i,0])*(point[1]-vert[i,1])/(vert[j,1]-vert[i,1]) + vert[i,0]
                if point[0] < Qx:       # point left of edge
                    odd = not odd       # line crosses edge
    return odd  # point is in polygon (not on the edge) if odd=true

# -------------------------------------------------------
# Test

pg.poly_plot(vert)

vert = pg._close_loop(vert)

start_time = time.time()

for Point in Points:
    if point_in_polygon(vert, Point):
        plt.plot(Point[0],Point[1],"r+")
    else:
        plt.plot(Point[0],Point[1],"b+")
        
print(f"elapsed time: {time.time() - start_time} s")