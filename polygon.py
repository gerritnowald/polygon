# -*- coding: utf-8 -*-
"""
geometry calculation of arbitrary 2D polygons

instance = polygon(Vertices)
    Vertices = [[x0,y0],[x1,y1],[x2,y2],...]: 2D-coordinates of vertices
    Polygon can be open or closed (i.e. first = last vertex)
    Area is positive for anti-clockwise order of vertices
    holes can be defined by cutting in and clockwise order

attributes:
    v: Vertex
    e: Edge (next of v)
    axis: 0: wrt x, 
          1: wrt y
    - instance.Area
    - instance.Angles[v]                    inner angles
    - instance.EdgesLength[e]
    - instance.EdgesMiddle[xe,ye]
    - instance.CenterMass[x,y]
    - instance.SecondMomentArea[axis]       wrt center of mass
    - instance.RotationVolume[axis]         solid of revolution
    - instance.RotationSurfaces[e,axis]     solid of revolution

methods:
    point = [x,y]: point to be tested
    - instance.isPointOnEdge(point)     true, if point is on any edge of polygon
    - instance.isPointInside(point)     true, if point is inside of polygon (not on the edge)
    - instance.plot()                   plots edges of polygon

@author: Gerrit Nowald
"""

import numpy as np
import matplotlib.pyplot as plt

class polygon:
    
    def __init__(self,vertices):
        
        # input checking
        self.Vertices = np.array(vertices)
        # coordinates as 2 columns (min 3 rows)
        if self.Vertices.shape[0] < self.Vertices.shape[1]:
            self.Vertices = np.transpose(self.Vertices)
        # first = last vertex
        if not np.isclose(self.Vertices[-1,:], self.Vertices[0,:]).all():
            self.Vertices = np.append(self.Vertices,[self.Vertices[0,:]],axis=0)
        
        # inner angles
        self.Angles = self.__poly_angles()
        # lengths of edges (Pythagorean theorem)
        self.EdgesLength = np.sqrt( np.sum( np.diff(self.Vertices, axis=0)**2, axis=1))
        # centers of edges
        self.EdgesMiddle = ( self.Vertices[0:-1] + self.Vertices[1:] )/2
        # area (Gauss's area formula, 0th moment of area)
        self.__FM = self.Vertices[0:-1,0] * self.Vertices[1:,1] - self.Vertices[1:,0] * self.Vertices[0:-1,1]
        self.Area = sum(self.__FM)/2
        # center of mass (1st moment of area / area)
        self.CenterMass = (self.__FM @ self.EdgesMiddle)/3/self.Area
        # second moment of area wrt center of mass
        self.SecondMomentArea = self.__poly_SMA()
        
        # volume of solid of revolution (Pappus's centroid theorem)
        self.RotationVolume = 2*np.pi*self.CenterMass[::-1]*self.Area
        # surface areas of solid of revolution (Pappus's centroid theorem)
        self.RotationSurfaces = 2*np.pi*self.EdgesMiddle[:,::-1]*(np.vstack((self.EdgesLength,self.EdgesLength))).T
        
        
    # def __str__(self):
        # number of edges
    
    # -------------------------------------------------------
    # geometrical properties of the polygon
    
    def __poly_angles(self):
        # inner angles
        vertext = np.append([self.Vertices[-2,:]],self.Vertices,axis=0)  # second last in front of first vertex
        vec = np.diff(vertext, axis=0)              # direction vectors of edges
        L   = np.linalg.norm(vec, ord=2, axis=1)    # length of edges
        return 180 - 180/np.pi*np.arccos( np.sum( vec[0:-1,:]*vec[1:,:], axis=1 ) / (L[0:-1]*L[1:]) )
    
    def __poly_SMA(self):
        # second moment of area wrt center of mass
        B  = (self.Vertices[0:-1] + self.Vertices[1:])**2 - self.Vertices[0:-1]*self.Vertices[1:]
        A2 = (self.__FM @ B)/12 - self.CenterMass**2*self.Area
        return A2[::-1]
    
    # -------------------------------------------------------
    #  plot
    
    def plot(self):
        plt.plot(self.Vertices[:,0],self.Vertices[:,1])
    
    # -------------------------------------------------------
    # points
    
    def isPointOnEdge(self, point):
        # computes the distance of a point from each edge. The point is on an edge,
        # if the point is between the vertices and the distance is smaller than the rounding error.
        # https://de.mathworks.com/matlabcentral/answers/351581-points-lying-within-line
        for i in range(self.Vertices.shape[0]-1):# for each edge
            j     = i + 1
            PQ    =         point - self.Vertices[i,]  # Line from P1 to Q
            P12   = self.Vertices[j,] - self.Vertices[i,]  # Line from P1 to P2
            L12   = np.sqrt(np.dot(P12,P12))# length of P12
            N     = P12/L12                 # Normal along P12
            Dist  = abs(np.cross(N,PQ))     # Norm of distance vector
            # Consider rounding errors
            Limit = np.spacing(np.max(np.abs([self.Vertices[i,], self.Vertices[j,], point])))*10
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
        for j in range(self.Vertices.shape[0]-1):        # for each edge check if the line crosses
            i = j + 1                                    # next vertex
            if self.Vertices[j,1] != self.Vertices[i,1]: # edge not parallel to x-axis (singularity)
                # point between y-coordinates of edge
                if (self.Vertices[i,1] > point[1]) != (self.Vertices[j,1] > point[1]):
                    # x-coordinate of intersection
                    Qx = (self.Vertices[j,0]-self.Vertices[i,0])*(point[1]-self.Vertices[i,1])/(self.Vertices[j,1]-self.Vertices[i,1]) + self.Vertices[i,0]
                    if point[0] < Qx:       # point left of edge
                        odd = not odd       # line crosses edge
        return odd  # point is in polygon (not on the edge) if odd=true