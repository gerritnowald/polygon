# -*- coding: utf-8 -*-
"""
Geometry calculation of arbitrary 2D polygons

Input:
- Vert=[x,y]: 2D array of columns of 2D-Coordinates of vertices
    Polygon can be open or closed (i.e. first = last vertice)
    Area is positive for anti-clockwise order of vertices
    holes can be defined by cutting in and clockwise order

functions:
- poly_A(Vert)              Area
- poly_L(Vert)              Lengths of edges
- poly_angles(Vert)         Inner angles
- poly_CM(Vert)             Center of mass
- poly_CMVert(Vert)         Centers of edges
- poly_SMA(Vert)            Second moment of area wrt center of mass
- poly_Vrot(Vert, axis=0)   Volume of solid of revolution
- poly_Arot(Vert, axis=0)   Surface areas of solid of revolution
- poly_plot(Vert)           plot polygon

Created on Mon Sep 13 15:25:19 2021

@author: Dr. Gerrit Nowald
"""

import numpy as np
import matplotlib.pyplot as plt

# -------------------------------------------------------
# functions

def _close_loop(Vert):
    if Vert.shape[0] < Vert.shape[1]:
        Vert = np.transpose(Vert)   # coordinates as 2 columns (min 3 rows) 
    if not np.isclose(Vert[-1,:], Vert[0,:]).all():
        Vert = np.append(Vert,[Vert[0,:]],axis=0)   # first = last vertice
    return Vert
   
    
def poly_A(Vert, flagFM=False):
    # Area (Gauss's area formula)
    Vert = _close_loop(Vert)
    FM   = Vert[0:-1,0] * Vert[1:,1] - Vert[1:,0] * Vert[0:-1,1]
    A    = sum(FM)/2   # 0th moment of area
    if flagFM == False:
        return A
    else:
        return A, FM


def poly_CMVert(Vert):
    # Centers of edges
    Vert = _close_loop(Vert)
    return ( Vert[0:-1] + Vert[1:] )/2
    

def poly_CM(Vert):
    # Center of Mass
    CMVert = poly_CMVert(Vert)
    A, FM  = poly_A(Vert, flagFM=True)
    A1     = (FM @ CMVert)/3    # 1st moment of area
    return A1/A


def poly_SMA(Vert):
    # second moment of area wrt center of mass
    Vert = _close_loop(Vert)
    B = (Vert[0:-1] + Vert[1:])**2 - Vert[0:-1]*Vert[1:]
    A, FM  = poly_A(Vert, flagFM=True)
    CM = poly_CM(Vert)
    A2 = (FM @ B)/12 - CM**2*A    # 2nd moment of area
    return A2[::-1]


def poly_L(Vert):
    # Lengths of edges (Pythagorean theorem)
    Vert = _close_loop(Vert)
    return np.sqrt( np.sum( np.diff(Vert, axis=0)**2, axis=1))


def poly_Vrot(Vert, axis=0):
    # volume of solid of revolution (Pappus's centroid theorem)
    A  = poly_A(Vert)
    CM = poly_CM(Vert)
    if axis == 0:
        return A*2*np.pi*CM[1]  # revolution around x-axis
    elif axis == 1:
        return A*2*np.pi*CM[0]  # revolution around y-axis


def poly_Arot(Vert, axis=0):
    # Surface areas of solid of revolution (Pappus's centroid theorem)
    L      = poly_L(Vert)
    CMVert = poly_CMVert(Vert)
    if axis == 0:
        return L*2*np.pi*CMVert[:,1]  # revolution around x-axis
    elif axis == 1:
        return L*2*np.pi*CMVert[:,0]  # revolution around y-axis    


def poly_angles(Vert):
    # inner angles
    Vert = _close_loop(Vert)
    Vert = np.append([Vert[-2,:]],Vert,axis=0)  # second last in front of first vertice
    vec = np.diff(Vert, axis=0)                 # direction vectors of edges
    L   = np.linalg.norm(vec, ord=2, axis=1)    # length of edges
    return 180 - 180/np.pi*np.arccos( np.sum( vec[0:-1,:]*vec[1:,:], axis=1 ) / (L[0:-1]*L[1:]) )


def poly_plot(Vert):
    # plot Polygon
    CM     = poly_CM(Vert)
    CMVert = poly_CMVert(Vert)
    Vert   = _close_loop(Vert)
    plt.plot(Vert[:,0],Vert[:,1])           # borders
    plt.plot(CM[0],CM[1],"+")               # Center of Mass
    plt.plot(CMVert[:,0],CMVert[:,1],"o")   # Centers of edges 