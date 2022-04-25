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

- poly_plot()               plot polygon

- isPointOnEdge(point)      true, if point is on any edge of polygon
- isPointInside(point)      true, if point is inside of polygon (not on the edge)

- poly_L()                  lengths of edges
- poly_CMvert()             centers of edges
- poly_angles()             inner angles

- poly_A()                  area
- poly_CM()                 center of mass
- poly_SMA()                second moment of area wrt center of mass

- poly_Vrot(axis=0)         volume of solid of revolution
- poly_Arot(axis=0)         surface areas of solid of revolution

Created on Mon Sep 13 15:25:19 2021

@author: Gerrit Nowald
"""

import numpy as np
import matplotlib.pyplot as plt

class polygon:
    
    def __init__(self,vert):
        
        # input checking
        self.vert = np.array(vert)
        # coordinates as 2 columns (min 3 rows)
        if self.vert.shape[0] < self.vert.shape[1]:
            self.vert = np.transpose(self.vert)
        # first = last vertice
        if not np.isclose(self.vert[-1,:], self.vert[0,:]).all():
            self.vert = np.append(self.vert,[self.vert[0,:]],axis=0)
        
        # inner angles
        self.angles = self.__poly_angles()
        # lengths of edges (Pythagorean theorem)
        self.edgesL = np.sqrt( np.sum( np.diff(self.vert, axis=0)**2, axis=1))
        # centers of edges
        self.edgesCM = ( self.vert[0:-1] + self.vert[1:] )/2
        # area (Gauss's area formula, 0th moment of area)
        self.__FM = self.vert[0:-1,0] * self.vert[1:,1] - self.vert[1:,0] * self.vert[0:-1,1]
        self.area = sum(self.__FM)/2
        # center of mass (1st moment of area / area)
        self.CM = (self.__FM @ self.edgesCM)/3/self.area
        # second moment of area wrt center of mass
        self.SecondMomentArea = self.__poly_SMA()
        
        # print attributes of polygon
        # print(self)
        
    # def __str__(self):
    
    # -------------------------------------------------------
    # geometrical properties of the polygon
    
    def __poly_angles(self):
        # inner angles
        vertext = np.append([self.vert[-2,:]],self.vert,axis=0)  # second last in front of first vertice
        vec = np.diff(vertext, axis=0)              # direction vectors of edges
        L   = np.linalg.norm(vec, ord=2, axis=1)    # length of edges
        return 180 - 180/np.pi*np.arccos( np.sum( vec[0:-1,:]*vec[1:,:], axis=1 ) / (L[0:-1]*L[1:]) )
    
    def __poly_SMA(self):
        # second moment of area wrt center of mass
        B = (self.vert[0:-1] + self.vert[1:])**2 - self.vert[0:-1]*self.vert[1:]
        A2 = (self.__FM @ B)/12 - self.CM**2*self.area
        return A2[::-1]
    
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
        for i in range(self.vert.shape[0]-1):# for each edge
            j     = i + 1
            PQ    =         point - self.vert[i,]  # Line from P1 to Q
            P12   = self.vert[j,] - self.vert[i,]  # Line from P1 to P2
            L12   = np.sqrt(np.dot(P12,P12))# length of P12
            N     = P12/L12                 # Normal along P12
            Dist  = abs(np.cross(N,PQ))     # Norm of distance vector
            # Consider rounding errors
            Limit = np.spacing(np.max(np.abs([self.vert[i,], self.vert[j,], point])))*10
            on    = Dist < Limit
            if on:
                L = np.dot(PQ,N)            # Projection of the vector from P1 to Q on the line:
                on = (L>=0.0 and L<=L12)    # Consider end points  
                return on
        return on
    
    def isPointInside(self, point=[0,0]):
        # A point is in a polygon, if a line from the point to infinity crosses the polygon an odd number of times.
        # Here, the line goes parallel to the x-axis in positive x-direction.
        # adapted from https://www.algorithms-and-technologies.com/point_in_polygon/python
        odd  = False    
        for j in range(self.vert.shape[0]-1):    # for each edge check if the line crosses
            i = j + 1                       # next vertice
            if self.vert[j,1] != self.vert[i,1]:      # edge not parallel to x-axis (singularity)
                # point between y-coordinates of edge
                if (self.vert[i,1] > point[1]) != (self.vert[j,1] > point[1]):
                    # x-coordinate of intersection
                    Qx = (self.vert[j,0]-self.vert[i,0])*(point[1]-self.vert[i,1])/(self.vert[j,1]-self.vert[i,1]) + self.vert[i,0]
                    if point[0] < Qx:       # point left of edge
                        odd = not odd       # line crosses edge
        return odd  # point is in polygon (not on the edge) if odd=true
     
    # -------------------------------------------------------
    # solid of revolution
    
    def poly_Arot(self, axis=0):
        # surface areas of solid of revolution (Pappus's centroid theorem)
        if axis == 0:
            return self.edgesL*2*np.pi*self.edgesCM[:,1]  # revolution around x-axis
        elif axis == 1:
            return self.edgesL*2*np.pi*self.edgesCM[:,0]  # revolution around y-axis
    
    def poly_Vrot(self, axis=0):
        # volume of solid of revolution (Pappus's centroid theorem)
        if axis == 0:
            return self.area*2*np.pi*self.CM[1]  # revolution around x-axis
        elif axis == 1:
            return self.area*2*np.pi*self.CM[0]  # revolution around y-axis