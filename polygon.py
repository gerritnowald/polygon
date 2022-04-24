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

- isPointOnEdge(vert, point)    true, if point is on any edge of polygon
- isPointInPolygon(vert, point) true, if point is inside of polygon (not on the edge)

- poly_L(vert)                  lengths of edges
- poly_CMvert(vert)             centers of edges
- poly_angles(vert)             inner angles

- poly_A(vert)                  area
- poly_CM(vert)                 center of mass
- poly_SMA(vert)                second moment of area wrt center of mass

- poly_Vrot(vert, axis=0)       volume of solid of revolution
- poly_Arot(vert, axis=0)       surface areas of solid of revolution

Created on Mon Sep 13 15:25:19 2021

@author: Gerrit Nowald
"""

import numpy as np
import matplotlib.pyplot as plt

class polygon:
    
    def __init__(self,vert):
        # coordinates as 2 columns (min 3 rows)
        if vert.shape[0] < vert.shape[1]:
            vert = np.transpose(vert)
        # first = last vertice
        if not np.isclose(vert[-1,:], vert[0,:]).all():
            vert = np.append(vert,[vert[0,:]],axis=0)
        self.vert = vert

    # -------------------------------------------------------
    #  plot
    
    def poly_plot(self):
        plt.plot(self.vert[:,0],self.vert[:,1])
    
    # -------------------------------------------------------
    # points
    
    def isPointOnEdge(self, point):
        # computes the distance of a point from each edge. The point is on an edge,
        # if the point is between the vertices and the distance is smaller than the rounding error.
        # https://de.mathworks.com/matlabcentral/answers/351581-points-lying-within-line
        vert = self.vert
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
    
    def isPointInPolygon(self, point=[0,0]):
        # A point is in a polygon, if a line from the point to infinity crosses the polygon an odd number of times.
        # Here, the line goes parallel to the x-axis in positive x-direction.
        # adapted from https://www.algorithms-and-technologies.com/point_in_polygon/python
        vert = self.vert
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
    
    def poly_L(self):
        # lengths of edges (Pythagorean theorem)
        return np.sqrt( np.sum( np.diff(self.vert, axis=0)**2, axis=1))
    
    def poly_CMvert(self):
        # centers of edges
        return (  self.vert[0:-1] + self.vert[1:] )/2
    
    def poly_angles(self):
        # inner angles
        vert = self.vert
        vert = np.append([vert[-2,:]],vert,axis=0)  # second last in front of first vertice
        vec = np.diff(vert, axis=0)                 # direction vectors of edges
        L   = np.linalg.norm(vec, ord=2, axis=1)    # length of edges
        return 180 - 180/np.pi*np.arccos( np.sum( vec[0:-1,:]*vec[1:,:], axis=1 ) / (L[0:-1]*L[1:]) )
    
    # -------------------------------------------------------
    # area
    
    def poly_A(self, flagFM=False):
        # area (Gauss's area formula)
        vert = self.vert
        FM   = vert[0:-1,0] * vert[1:,1] - vert[1:,0] * vert[0:-1,1]
        A    = sum(FM)/2   # 0th moment of area
        if flagFM == False:
            return A
        else:
            return A, FM
    
    def poly_CM(self):
        # center of mass
        CMvert = self.poly_CMvert()
        A, FM  = self.poly_A(flagFM=True)
        A1     = (FM @ CMvert)/3    # 1st moment of area
        return A1/A
    
    def poly_SMA(self):
        # second moment of area wrt center of mass
        vert = self.vert
        B = (vert[0:-1] + vert[1:])**2 - vert[0:-1]*vert[1:]
        A, FM  = self.poly_A(flagFM=True)
        CM = self.poly_CM()
        A2 = (FM @ B)/12 - CM**2*A    # 2nd moment of area
        return A2[::-1]
    
    # -------------------------------------------------------
    # solid of revolution
    
    def poly_Arot(self, axis=0):
        # surface areas of solid of revolution (Pappus's centroid theorem)
        L      = self.poly_L()
        CMvert = self.poly_CMvert()
        if axis == 0:
            return L*2*np.pi*CMvert[:,1]  # revolution around x-axis
        elif axis == 1:
            return L*2*np.pi*CMvert[:,0]  # revolution around y-axis
    
    def poly_Vrot(self, axis=0):
        # volume of solid of revolution (Pappus's centroid theorem)
        A  = self.poly_A()
        CM = self.poly_CM()
        if axis == 0:
            return A*2*np.pi*CM[1]  # revolution around x-axis
        elif axis == 1:
            return A*2*np.pi*CM[0]  # revolution around y-axis