# -*- coding: utf-8 -*-
"""
geometry calculation of arbitrary 2D polygons:
- area, lengths of edges, inner angles
- order of vertices (clockwise or anti-clockwise)
- centroid (center of mass)
- check if point is inside or on edge of polygon
- volume and surfaces of solid of revolution
- second moment of area (bending stiffness of beams)
- for triangles: centers and radii of incircle and circumscribed (outer) circle


creating a polygon object:

Vertices = [[x0,y0],[x1,y1],[x2,y2],...]   # 2D-coordinates of vertices
instance = polygon(Vertices)
    
    - polygon can be open or closed (i.e. first = last vertex)
    - holes can be defined by self-intersecting and opposite order of vertices inside than outside


attributes:
    
    v: Vertex
    e: Edge (next of v)
    axis: 0: wrt x, 
          1: wrt y
    - instance.IsClockwise                  Boolean, order of vertices
    - instance.Area
    - instance.Angles[v]                    inner angles
    - instance.EdgesLength[e]
    - instance.EdgesMiddle[xe,ye]			midpoints of edges
    - instance.CenterMass[x,y]              centroid / center of mass
    - instance.SecondMomentArea[axis]       wrt center of mass
    - instance.RotationVolume[axis]         solid of revolution
    - instance.RotationSurfaces[e,axis]     solid of revolution
	- triangles:
		- instance.CenterOuterCircle[x,y]   circumcenter / center of circumsribed (outer) circle
		- instance.RadiusOuterCircle		radius of circumsribed (outer) circle
        - instance.CenterInnerCircle[x,y]   center of incircle (inner circle)
        - instance.RadiusInnerCircle        radius of incircle (inner circle)


methods:
    
    point = [x,y]: point to be tested
    - instance.isPointOnEdge(point)     true, if point is on any edge of polygon
    - instance.isPointInside(point)     true, if point is inside of polygon (not on the edge)
    - instance.plot(numbers=False)      plots edges of polygon, optionally numbers of vertices
	- triangles:
		- instance.plot_CircumscribedCircle()	plots circumsribed (outer) circle
        - instance.plot_Incircle()              plots incircle (inner circle)

@author: Gerrit Nowald
"""

import numpy as np
import matplotlib.pyplot as plt

# -----------------------------------------------------------------------------
# base class
# -----------------------------------------------------------------------------

class _polygonBase():
    
    # -------------------------------------------------------
    # constructor (geometrical properties)
    
    def __init__(self,vert):
        
        # inner angles & lengths of edges
        self.Angles, L   = self._poly_angles(vert)
        self.EdgesLength = L[1:]
        
        # centers of edges
        self.EdgesMiddle = ( vert[:-1] + vert[1:] )/2
        
        # area (Gauss's area formula, 0th moment of area)
        # https://en.wikipedia.org/wiki/Shoelace_formula
        FM = vert[:-1,0] * vert[1:,1] - vert[1:,0] * vert[:-1,1]
        AreaSigned = sum(FM)/2
        self.IsClockwise = AreaSigned < 0   # area negative for clockwise order of vertices
        self.Area = abs(AreaSigned)
        
        # center of mass (1st moment of area / area)
        self.CenterMass = (FM @ self.EdgesMiddle)/3/AreaSigned
        
        # second moment of area wrt center of mass
        B = (vert[:-1] + vert[1:])**2 - vert[:-1]*vert[1:]
        self.SecondMomentArea = abs(FM @ B)/12 - self.CenterMass**2*self.Area
        
        # solid of revolution (Pappus's centroid theorem)
        # https://en.wikipedia.org/wiki/Pappus%27s_centroid_theorem
        self.RotationVolume   = 2*np.pi*self.Area*self.CenterMass[::-1]
        self.RotationSurfaces = 2*np.pi*self.EdgesLength[:,None]*self.EdgesMiddle[:,::-1]
                
        self.Vertices = vert
    
    # -------------------------------------------------------
    # geometrical properties of the polygon
    
    def _poly_angles(self,vert):
        # inner angles & length of edges
        vertext = np.append([vert[-2,]],vert,axis=0)   # second last in front of first vertex
        vec = np.diff(vertext, axis=0)                 # direction vectors of edges
        L   = np.linalg.norm(vec, ord=2, axis=1)       # length of edges (Pythagorean theorem)
        # law of cosines
        angles = 180*(1 - 1/np.pi*np.arccos( np.sum( vec[:-1,]*vec[1:,], axis=1 ) / (L[:-1]*L[1:]) ))
        return angles, L
    
    # -------------------------------------------------------
    # print method (number of vertices)
    
    def __str__(self):
        return f'Polygon with {len(self.Vertices)-1} vertices'
    
    # -------------------------------------------------------
    # methods plotting
    
    def _plot_circ(self, R, C):
        angle = np.linspace(0, 2*np.pi, 50)
        x = C[0] + R*np.cos(angle)
        y = C[1] + R*np.sin(angle)
        plt.plot(x,y)
    
    def plot(self,numbers=False):
        plt.plot(self.Vertices[:,0],self.Vertices[:,1])
        if numbers:
            for i in range(len(self.Vertices)-1):
                plt.text(self.Vertices[i,0], self.Vertices[i,1], str(i) )
    
    # -------------------------------------------------------
    # methods point testing
    
    def isPointOnEdge(self, point):
        # computes the distance of a point from each edge. The point is on an edge,
        # if the point is between the vertices and the distance is smaller than the rounding error.
        # https://de.mathworks.com/matlabcentral/answers/351581-points-lying-within-line
        vert = self.Vertices
        for i in range(vert.shape[0]-1):    # for each edge
            PQ    =      point - vert[i,]   # Line from P1 to Q
            P12   = vert[i+1,] - vert[i,]   # Line from P1 to P2
            L12   = np.sqrt(np.dot(P12,P12))# length of P12
            N     = P12/L12                 # Normal along P12
            Dist  = abs(np.cross(N,PQ))     # Norm of distance vector
            # Consider rounding errors
            Limit = np.spacing(np.max(np.abs([vert[i,], vert[i+1,], point])))*10
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
        vert = self.Vertices
        odd  = False    
        for j in range(vert.shape[0]-1):    # for each edge check if the line crosses
            i = j + 1                       # next vertex
            if vert[j,1] != vert[i,1]:      # edge not parallel to x-axis (singularity)
                # point between y-coordinates of edge
                if (vert[i,1] > point[1]) != (vert[j,1] > point[1]):
                    # x-coordinate of intersection
                    Qx = (vert[j,0]-vert[i,0])*(point[1]-vert[i,1])/(vert[j,1]-vert[i,1]) + vert[i,0]
                    if point[0] < Qx:       # point left of edge
                        odd = not odd       # line crosses edge
        return odd  # point is in polygon (not on the edge) if odd=true

# -----------------------------------------------------------------------------
# triangle class
# -----------------------------------------------------------------------------

class _triangle(_polygonBase):
    
    # -------------------------------------------------------
    # constructor (geometrical properties)
    
    def __init__(self,vert):
        
        super().__init__(vert)
    
        # circumscribed (outer) circle
        self.CenterOuterCircle, self.RadiusOuterCircle = self._circumcenter(vert)
        
        # incircle (inner circle)
        # https://en.wikipedia.org/wiki/Incenter
        self.CenterInnerCircle = np.roll(self.EdgesLength, -1) @ vert[:-1,] / sum(self.EdgesLength)
        self.RadiusInnerCircle = 2*self.Area/sum(self.EdgesLength)
    
    # -------------------------------------------------------
    # geometrical properties of the triangle
    
    def _circumcenter(self,vert):
        # center of circumscribed circle
        # https://en.wikipedia.org/wiki/Circumscribed_circle
        vertP = vert[:-1,:] - vert[0,:]      # coordinate transformation
        DP  = np.cross(vertP[:,0],vertP[:,1])[0]
        LSQ = np.linalg.norm(vertP, axis=1)**2
        UP  = np.cross(vertP,LSQ,axis=0)[0,:]/DP/2
        UP  = UP[::-1]*np.array([-1, 1])     # orthogonal vector
        Center = UP + vert[0,:]              # coordinate transformation
        Radius = np.linalg.norm(UP, ord=2)
        return Center, Radius
    
    # -------------------------------------------------------
    # methods plotting
    
    def plot_CircumscribedCircle(self):
        self._plot_circ( R=self.RadiusOuterCircle, C=self.CenterOuterCircle)
    
    def plot_Incircle(self):
        self._plot_circ( R=self.RadiusInnerCircle, C=self.CenterInnerCircle)

# -----------------------------------------------------------------------------
# main class
# -----------------------------------------------------------------------------

class polygon():
    
    def __new__(self, Vertices):
        
        # input checks
        vert = np.array(Vertices)
        # coordinates as 2 columns (min 3 rows)
        if vert.shape[0] < vert.shape[1]:
            vert = vert.T
        # first = last vertex
        if not np.isclose(vert[-1,], vert[0,]).all():
            vert = np.append(vert,[vert[0,]],axis=0)
        
        # choose subclass
        if len(vert)-1 == 3:
            return _triangle(vert)
        else:
            return _polygonBase(vert)