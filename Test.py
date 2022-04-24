# -*- coding: utf-8 -*-
"""
Created on Sun Sep 19 19:50:40 2021

@author: Gerrit Nowald
"""

import numpy as np
import matplotlib.pyplot as plt

from polygon import polygon

# -------------------------------------------------------
# Input

# rectangle
# point = np.array([4,1])
# b = 5
# h = 2
# vert = np.array([
#     [0, 0],
#     [b, 0],
#     [b, h],
#     [0, h],
#     ])
# A_analytic  = b*h
# A2_analytic = np.array([b*h**3, b**3*h])/12


# triangle
# N = 1000
# points = np.hstack(( np.random.rand(N,1)*5-1, np.random.rand(N,1)*10-1.5 ))
# a = 3
# h = 7
# vert = np.array([
#     [0, 0],
#     [a, 0],
#     [a/2, h],
#     ])
# A_analytic  = 0.5*a*h
# A2_analytic = np.array([a*h**3/36, a**3*h/48])

# -------------------------------------------------------
# Output

# plot polygon
# heart.poly_plot()

# plot center of mass
# CM     = poly_CM(vert)
# plt.plot(CM[0],CM[1],"+")

# plot centers of edges 
# CMvert = poly_CMvert(vert)
# plt.plot(CMvert[:,0],CMvert[:,1],"o")

# geometry of polygon
# print(f"Area: {poly_A(vert)}")
# print(f"Lengths of edges: {poly_L(vert)}")
# print(f"Inner angles: {poly_angles(vert)}°")

# second moment of area
# A2 = poly_SMA(vert)
# print(f"second moment of area wrt x-axis: {A2[0]}")
# print(f"second moment of area wrt y-axis: {A2[1]}")

# geometry of solid of revolution
# print(f"Volume of solid of revolution wrt x-axis: {poly_Vrot(vert)}")
# print(f"Volume of solid of revolution wrt y-axis: {poly_Vrot(vert,axis=1)}")
# print(f"Surface of areas solid of revolution wrt x-axis: {poly_Arot(vert)}")
# print(f"Surface of areas solid of revolution wrt y-axis: {poly_Arot(vert,axis=1)}")

# test of specific point
# plt.plot(point[0],point[1],"r+")
# print(f'Point on edge: {isPointOnEdge(vert, point)}')
# print(f'Point in polygon: {isPointInPolygon(vert, point)}')

# -------------------------------------------------------
# heart

N = 1000
points = np.hstack(( np.random.rand(N,1)*6-3, np.random.rand(N,1)*10-2 ))
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
heart = polygon(vert)

# tests for random points
for point in points:
    if heart.isPointInPolygon(point):
        style = "y+"   
    else:
        style = "b+"
    plt.plot(point[0],point[1],style)