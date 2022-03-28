# -*- coding: utf-8 -*-
"""
geometry calculation of arbitrary 2D polygons

input:
- vert=[x,y]: 2D array of columns of 2D-coordinates of vertices
    Polygon can be open or closed (i.e. first = last vertice)
    Area is positive for anti-clockwise order of vertices
    holes can be defined by cutting in and clockwise order
- point=[x,y]: point to be tested
- axis: 0: with respect to x-axis
        1: with respect to y-axis

functions:
- poly_plot(vert)               plot polygon
- poly_A(vert)                  area
- poly_L(vert)                  lengths of edges
- poly_angles(vert)             inner angles
- poly_CM(vert)                 center of mass
- poly_CMvert(vert)             centers of edges
- poly_SMA(vert)                second moment of area wrt center of mass
- poly_Vrot(vert, axis=0)       volume of solid of revolution
- poly_Arot(vert, axis=0)       surface areas of solid of revolution
- isPointInPolygon(vert, point) true, if point is inside of polygon (not on the edge)

Created on Mon Sep 13 15:25:19 2021

@author: Gerrit Nowald
"""

import numpy as np
import matplotlib.pyplot as plt

# -------------------------------------------------------
# input check

def _close_loop(vert):
    if vert.shape[0] < vert.shape[1]:
        vert = np.transpose(vert)   # coordinates as 2 columns (min 3 rows) 
    if not np.isclose(vert[-1,:], vert[0,:]).all():
        vert = np.append(vert,[vert[0,:]],axis=0)   # first = last vertice
    return vert

# -------------------------------------------------------
# points

def isPointInPolygon(vert, point=[0,0]):
    # A point is in a polygon, if a line from the point to infinity crosses the polygon an odd number of times.
    # Here, the line goes parallel to the x-axis in positive x-direction.
    # adapted from https://www.algorithms-and-technologies.com/point_in_polygon/python
    vert = _close_loop(vert)
    odd  = False    
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
# edges

def poly_L(vert):
    # lengths of edges (Pythagorean theorem)
    vert = _close_loop(vert)
    return np.sqrt( np.sum( np.diff(vert, axis=0)**2, axis=1))

def poly_CMvert(vert):
    # centers of edges
    vert = _close_loop(vert)
    return ( vert[0:-1] + vert[1:] )/2

def poly_angles(vert):
    # inner angles
    vert = _close_loop(vert)
    vert = np.append([vert[-2,:]],vert,axis=0)  # second last in front of first vertice
    vec = np.diff(vert, axis=0)                 # direction vectors of edges
    L   = np.linalg.norm(vec, ord=2, axis=1)    # length of edges
    return 180 - 180/np.pi*np.arccos( np.sum( vec[0:-1,:]*vec[1:,:], axis=1 ) / (L[0:-1]*L[1:]) )

# -------------------------------------------------------
# area

def poly_A(vert, flagFM=False):
    # area (Gauss's area formula)
    vert = _close_loop(vert)
    FM   = vert[0:-1,0] * vert[1:,1] - vert[1:,0] * vert[0:-1,1]
    A    = sum(FM)/2   # 0th moment of area
    if flagFM == False:
        return A
    else:
        return A, FM

def poly_CM(vert):
    # center of mass
    CMvert = poly_CMvert(vert)
    A, FM  = poly_A(vert, flagFM=True)
    A1     = (FM @ CMvert)/3    # 1st moment of area
    return A1/A

def poly_SMA(vert):
    # second moment of area wrt center of mass
    vert = _close_loop(vert)
    B = (vert[0:-1] + vert[1:])**2 - vert[0:-1]*vert[1:]
    A, FM  = poly_A(vert, flagFM=True)
    CM = poly_CM(vert)
    A2 = (FM @ B)/12 - CM**2*A    # 2nd moment of area
    return A2[::-1]

# -------------------------------------------------------
# solid of revolution

def poly_Arot(vert, axis=0):
    # surface areas of solid of revolution (Pappus's centroid theorem)
    L      = poly_L(vert)
    CMvert = poly_CMvert(vert)
    if axis == 0:
        return L*2*np.pi*CMvert[:,1]  # revolution around x-axis
    elif axis == 1:
        return L*2*np.pi*CMvert[:,0]  # revolution around y-axis

def poly_Vrot(vert, axis=0):
    # volume of solid of revolution (Pappus's centroid theorem)
    A  = poly_A(vert)
    CM = poly_CM(vert)
    if axis == 0:
        return A*2*np.pi*CM[1]  # revolution around x-axis
    elif axis == 1:
        return A*2*np.pi*CM[0]  # revolution around y-axis

# -------------------------------------------------------
#  plot

def poly_plot(vert):
    # plot Polygon
    CM     = poly_CM(vert)
    CMvert = poly_CMvert(vert)
    vert   = _close_loop(vert)
    plt.plot(vert[:,0],vert[:,1])           # borders
    plt.plot(CM[0],CM[1],"+")               # Center of Mass
    plt.plot(CMvert[:,0],CMvert[:,1],"o")   # Centers of edges 