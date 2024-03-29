# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import warnings
import copy

# #############################################################################
# selector class
# #############################################################################

class polygon():
    """
    geometry calculation of arbitrary 2D polygons:  
        - area, centroid (center of mass)
        - second moment of area (bending stiffness of beams)
        - triangles: incircle and circumscribed (outer) circle
        - solid of revolution: volume, surface areas, center of mass
        - check if point is inside or on edge of polygon
        - move, rotate and scale polygon
        - plotting with matplotlib arguments (e.g. color, linestyle, label)


    creating a polygon object:

    Vertices = [[x0,y0],[x1,y1],[x2,y2],...]   # 2D-coordinates of vertices
    instance = polygon(Vertices)
        
        - polygon can be open or closed (i.e. first = last vertex)
        - holes can be defined by self-intersecting and opposite order of vertices inside than outside


    creating a solid of revolution
        
    instance = polygon(Vertices, axis)

        axis: 0: revolution around x-axis
              1: revolution around y-axis


    attributes of polygon object (geometrical properties):
        
        v: Vertex
        e: Edge (next of v)
        - IsClockwise                          Boolean, order of vertices
        - Area
        - Angles[v]                            inner angles
        - EdgesLength[e]
        - EdgesMiddle[xe,ye]                   midpoints of edges
        - CenterMass[x,y]                      centroid / center of mass
        - SecondMomentArea                     [Ixx, Iyy, Ixy], with respect to origin
        - solid of revolution:
            - RotationVolume
            - RotationSurfaces[e]
            - CenterMassCrossSection[r,z]      CenterMass[r,z] now relates to solid
        - triangles:
            - CenterOuterCircle[x,y]           circumcenter / center of circumsribed (outer) circle
            - RadiusOuterCircle                radius of circumsribed (outer) circle
            - CenterInnerCircle[x,y]           center of incircle (inner circle)
            - RadiusInnerCircle                radius of incircle (inner circle)


    methods of polygon object:
        
        - abs(instance)          returns area or volume of solid of revolution
        
        - plotting (matplotlib optional arguments can be used)
            - plot                              contour of polygon
            - plotCenterMass
            - plotCenterEdges
            - solid of revolution:
                - plot3d                        3D wireframe plot of solid
                - plotRotationAxis              only keyword arguments
                - plotCenterMassCrossSection    for 2D plot
            - triangles:
                - plotOutCircle                 circumscribed (outer) circle
                - plotIncircle                  incircle (inner circle)
        
        - point testing
            - instance(point), isPointInside(point)    true, if point [x,y] is inside of polygon (not on the edge)
            - isPointOnEdge(point)                     true, if point [x,y] is on any edge of polygon
        
        - manipulation (translation, rotation & scaling)
            - instance + [dx,dy] , instance - [dx,dy] , move([dx,dy])
                    translation by distances dx,dy in x,y-direction
            
            - centerOrigin()
                    moves origin of coordinate system to center of mass
                                            
            - rotate(angle,[cx,cy]) , rotateClockwise(angle,[cx,cy])
                    (counter)-clockwise rotation by angle / °
                    with respect to point [cx,cy] (optional, default center of mass)
                                            
            - instance * [fx,fy] , instance / [fx,fy] , scale([fx,fy],[cx,cy])
                    scaling by factors fx, fy in x,y-direction (negative: flip)
                    with respect to point [cx,cy] (optional, default center of mass)

    @author: Gerrit Nowald
    """
    
    def __new__(self, Vertices, axis=None):
        """input checks for vertices and selection of specialized class"""
        
        # -------------------------------------------------------
        # input checks
        
        vert = np.array(Vertices)   # shallow copy
        
        # coordinates as 2 columns (min 3 rows)
        if vert.shape[0] < vert.shape[1]:
            vert = vert.T
        
        # first = last vertex
        if not np.isclose(vert[-1,], vert[0,]).all():
            vert = np.append(vert, [vert[0,]], axis=0)
        
        # -------------------------------------------------------
        # choose subclass
        
        isTriangle = len(vert)-1 == 3
        isSolidRev = axis is not None
        
        if isTriangle and not isSolidRev:
            return _triangle(vert, axis)
        
        elif isSolidRev and not isTriangle:
            return _solid(vert, axis)
        
        elif isSolidRev and isTriangle:
            return _solid_and_triangle(vert, axis)
        
        else:
            return _polygonBase(vert, axis)

# #############################################################################
# base class
# #############################################################################

class _polygonBase():
    
    # -------------------------------------------------------
    # constructor (geometrical properties)
    
    def __init__(self, vert, axis):
        """calculates geometrical properties of polygon"""
        
        self.Vertices = vert
        self._axis    = axis
        
        self.EdgesMiddle, self._AreaSigned, self.IsClockwise, self.CenterMass, self.SecondMomentArea, self._Ixy = self._geom2D(vert)
        self.Area = abs(self._AreaSigned)
        
        self.EdgesLength, self.Angles = self._edges(vert)
        
    # -------------------------------------------------------
    # geometrical properties of polygon
    
    @staticmethod
    def _geom2D(vert):
        """calculates area, centroid and second moment of area of polygon"""
        
        # centers of edges
        ri   = vert[:-1]
        rip1 = vert[1:]
        EdgesMiddle = (ri + rip1)/2
        
        # area (Gauss's area formula, 0th moment of area)
        # https://en.wikipedia.org/wiki/Shoelace_formula
        xi   =   ri[:,0]
        yi   =   ri[:,1]
        xip1 = rip1[:,0]
        yip1 = rip1[:,1]
        FM   = xi*yip1 - xip1*yi
        AreaSigned  = sum(FM)/2
        IsClockwise = AreaSigned < 0   # area negative for clockwise order of vertices
        
        # center of mass (1st moment of area / area)
        CenterMass = FM @ EdgesMiddle /3/AreaSigned
        
        # second moment of area
        # https://en.wikipedia.org/wiki/Second_moment_of_area
        Brr    = ri**2 + ri*rip1 + rip1**2
        Bxy    = xi*yip1 + 2*xi*yi + 2*xip1*yip1 + xip1*yi
        IyyIxx = FM @ Brr / 12
        Ixy    = FM @ Bxy / 24
        SecondMomentArea = np.hstack(( abs(IyyIxx[::-1]), -Ixy*(-1)**IsClockwise ))
        
        return EdgesMiddle, AreaSigned, IsClockwise, CenterMass, SecondMomentArea, Ixy
    
    @staticmethod
    def _edges(vert):
        """calculates lengths of edges and inner angles of polygon"""
        
        # lengths of edges
        vertext = np.append([vert[-2,]], vert, axis=0) # second last in front of first vertex
        vec = np.diff(vertext, axis=0)                 # direction vectors of edges
        L   = np.linalg.norm(vec, ord=2, axis=1)       # length of edges (Pythagorean theorem)
        EdgesLength = L[1:]
        
        # inner angles (law of cosines)
        angles = np.pi - np.arccos( np.sum( vec[:-1,]*vec[1:,], axis=1 ) / (L[:-1]*L[1:]) )
        
        return EdgesLength, np.degrees(angles)
    
    # -------------------------------------------------------
    # dunder methods
    
    def __repr__(self):
        return f'polygon({self.Vertices})'
    
    def __str__(self):
        return f'Polygon with {len(self.Vertices)-1} vertices'
    
    def __abs__(self):
        """returns area"""
        return self.Area
    
    # -------------------------------------------------------
    # methods plotting
    
    def plot(self, *plt_args, numbers = False, ax = None, **plt_kwargs):
        """
        contour of polygon
        numbers: optional, numbers of vertices & edges
        """
        if ax is None:
            ax = plt.gca()
        # plot contour of polygon
        ax.plot(self.Vertices[:,0], self.Vertices[:,1], *plt_args, **plt_kwargs)
        # plot numbers of vertices & edges
        if numbers:
            for i in range(len(self.Vertices)-1):
                ax.text(self.Vertices[i,0],    self.Vertices[i,1],    str(i), c='r' )
                ax.text(self.EdgesMiddle[i,0], self.EdgesMiddle[i,1], str(i) )
        return ax
    
    def plotCenterMass(self, *plt_args, ax = None, **plt_kwargs):
        if ax is None:
            ax = plt.gca()
        if not plt_args:
            if 'color' not in plt_kwargs:
                plt_kwargs['color']  = 'r'
            if 'marker' not in plt_kwargs:
                plt_kwargs['marker'] = '+'
        CenterMass = copy.copy(self.CenterMass)
        # 3D CenterMass
        if ax.name == "3d":
            if self._axis == 0:
                CenterMass = CenterMass[::-1]
            CenterMass.insert(0, 0)
        ax.plot( *CenterMass, *plt_args, **plt_kwargs )
        return ax
    
    def plotCenterEdges(self, *plt_args, ax = None, **plt_kwargs):
        if ax is None:
            ax = plt.gca()
        if not plt_args:
            if 'color' not in plt_kwargs:
                plt_kwargs['color']     = 'k'
            if 'marker' not in plt_kwargs:
                plt_kwargs['marker']    = 'o'
            if 'linestyle' not in plt_kwargs:
                plt_kwargs['linestyle'] = ''
        ax.plot( self.EdgesMiddle[:,0], self.EdgesMiddle[:,1], *plt_args, **plt_kwargs )
        return ax
    
    @staticmethod
    def _plot_circ(*plt_args, radius = 1, center = (0,0), Npoints = 50, ax = None, **plt_kwargs ):
        """circle in (or parallel to) x,y plane"""
        if ax is None:
            ax = plt.gca()
        # calculate circle coordinates
        angle = np.linspace(0, 2*np.pi, Npoints+1)
        x = center[0] + radius*np.cos(angle)
        y = center[1] + radius*np.sin(angle)
        # plot circle
        try:    # center has 3 components --> parallel to x,y plane
            z = center[2] * np.ones( Npoints+1 )
            ax.plot( x, y, z, *plt_args, **plt_kwargs )
        except: # center has 2 components --> in x,y plane
            ax.plot( x, y, *plt_args, **plt_kwargs )
            ax.axis('equal')
        return ax
    
    # -------------------------------------------------------
    # methods manipulation
    
    # translation
    @staticmethod
    def _move(vert, distances):
        return vert + distances
    
    def move(self, distances):
        """creates copy of polygon translated in x,y direction"""
        Vertices_new = self._move(self.Vertices, distances)
        return polygon(Vertices_new, self._axis)
    def centerOrigin(self):
        """creates copy of polygon with center of mass at origin"""
        return self.move(- self.CenterMass )
    def __add__(self, distances):
        """creates copy of polygon translated in x,y direction"""
        return self.move(distances)
    def __sub__(self, distances):
        """creates copy of polygon translated in x,y direction"""
        return self.move(- np.array(distances) )
    
    
    # rotation (wrt to point, default center of mass)
    @staticmethod
    def _rotate(vert, angle, point):
        alpha = np.radians(angle)
        R = [[np.cos(alpha), np.sin(alpha)], [-np.sin(alpha), np.cos(alpha)]]
        return (vert - point) @ R + point
    
    def rotate(self, angle, point = None):
        """creates copy of polygon rotated in counter-clockwise direction"""
        if point is None:
            point = self.CenterMass
        Vertices_new = self._rotate(self.Vertices, angle, point)
        return polygon(Vertices_new, self._axis)
    def rotateClockwise(self, angle, point=None):
        """creates copy of polygon rotated in clockwise direction"""
        return self.rotate(-angle, point)
    
    
    # scaling (wrt to point, default center of mass)
    @staticmethod
    def _scale(vert, factors, point):
        return (vert - point)*factors + point
    
    def scale(self, factors, point = None):
        """creates scaled copy of polygon"""
        if point is None:
            point = self.CenterMass
        Vertices_new = self._scale(self.Vertices, factors, point)
        return polygon(Vertices_new, self._axis)
    def __mul__(self, factors):
        """creates scaled copy of polygon"""
        return self.scale(factors)
    def __truediv__(self, factors):
        """creates scaled copy of polygon"""
        return self.scale( 1/np.array(factors) )
    
    # -------------------------------------------------------
    # methods point testing
    
    @staticmethod
    def _isPointOnEdge(vert, point):
        """
        computes the distance of a point from each edge. The point is on an 
        edge, if the point is between the vertices and the distance is smaller
        than the rounding error.
        https://de.mathworks.com/matlabcentral/answers/351581-points-lying-within-line
        """
        for i in range(vert.shape[0] - 1):  # for each edge
            PQ    =      point - vert[i,]   # Line from P1 to Q
            P12   = vert[i+1,] - vert[i,]   # Line from P1 to P2
            L12   = np.sqrt(np.dot(P12,P12))# length of P12
            N     = P12/L12                 # Normal along P12
            Dist  = abs(np.cross(N,PQ))     # Norm of distance vector
            # Consider rounding errors
            Limit = np.spacing( np.max(np.abs([vert[i,], vert[i+1,], point])) )*10
            on    = Dist < Limit
            if on:
                L = np.dot(PQ,N)            # Projection of the vector from P1 to Q on the line:
                on = (L>=0.0 and L<=L12)    # Consider end points  
                return on
        return on
    
    def isPointOnEdge(self, point):
        """returns Boolean"""
        return self._isPointOnEdge(self.Vertices, point)
    
    
    @staticmethod
    def _isPointInside(vert, point = [0,0]):
        """
        A point is in a polygon, if a line from the point to infinity crosses 
        the polygon an odd number of times.
        Here, the line goes parallel to the x-axis in positive x-direction.
        adapted from https://www.algorithms-and-technologies.com/point_in_polygon/python
        """
        odd = False    
        for j in range(vert.shape[0]-1):    # for each edge check if the line crosses
            i = j + 1                       # next vertex
            # edge parallel to x-axis (singularity)
            if vert[j,1] == vert[i,1]:
                continue
            # point not between y-coordinates of edge
            if (vert[i,1] > point[1]) == (vert[j,1] > point[1]):
                continue
            # x-coordinate of intersection
            Qx = (vert[j,0]-vert[i,0])*(point[1]-vert[i,1])/(vert[j,1]-vert[i,1]) + vert[i,0]
            if point[0] < Qx:       # point left of edge
                odd = not odd       # line crosses edge
        return odd  # point is in polygon (not on the edge) if odd=true
    
    def isPointInside(self, point = [0,0]):
        """returns Boolean"""
        return self._isPointInside(self.Vertices, point = point)
    def __call__(self, point=[0,0]):
        """returns True, if point [x,y] is inside of polygon (not on the edge)"""
        return self.isPointInside(point)

# #############################################################################
# triangle class
# #############################################################################

class _triangle(_polygonBase):
    
    # -------------------------------------------------------
    # constructor (geometrical properties)
    
    def __init__(self, vert, axis):
        """calculates geometrical properties of triangle"""
        super().__init__(vert, axis)
    
        self.CenterOuterCircle, self.RadiusOuterCircle = self._OuterCircle(vert)
        self.CenterInnerCircle, self.RadiusInnerCircle = self._incircle(vert, self.Area, self.EdgesLength)
    
    # -------------------------------------------------------
    # geometrical properties of the triangle
    
    @staticmethod
    def _incircle(vert, Area, EdgesLength):
        """
        center & radius of incircle (inner circle)
        https://en.wikipedia.org/wiki/Incenter
        """
        CenterInnerCircle = np.roll(EdgesLength, -1) @ vert[:-1,] / sum(EdgesLength)
        RadiusInnerCircle = 2*Area / sum(EdgesLength)
        return CenterInnerCircle, RadiusInnerCircle
    
    @staticmethod
    def _OuterCircle(vert):
        """
        center & radius of circumscribed (outer) circle
        https://en.wikipedia.org/wiki/Circumscribed_circle
        """
        vertP = vert[:-1,:] - vert[0,:]      # coordinate transformation
        DP  = np.cross(vertP[:,0], vertP[:,1])[0]
        LSQ = np.linalg.norm(vertP, axis=1)**2
        UP  = np.cross(vertP, LSQ, axis=0)[0,:] /DP/2
        UP  = UP[::-1]*np.array([-1, 1])     # orthogonal vector
        Center = UP + vert[0,:]              # coordinate transformation
        Radius = np.linalg.norm(UP, ord=2)
        return Center, Radius
    
    # -------------------------------------------------------
    # methods plotting
    
    def plotOutCircle(self, *plt_args, **plt_kwargs):
        """circumscribed (outer) circle"""
        ax = self._plot_circ(*plt_args, radius = self.RadiusOuterCircle, center = self.CenterOuterCircle, **plt_kwargs)
        return ax
    
    def plotIncircle(self, *plt_args, **plt_kwargs):
        """inner circle"""
        ax = self._plot_circ(*plt_args, radius = self.RadiusInnerCircle, center = self.CenterInnerCircle, **plt_kwargs)
        return ax

# #############################################################################
# solid of revolution class
# #############################################################################

class _solid(_polygonBase):
    
    # -------------------------------------------------------
    # constructor (geometrical properties)
    
    def __init__(self, vert, axis):
        """calculates geometrical properties of solid of revolution"""
        super().__init__(vert, axis)
    
        if min(vert[:,1-axis]) * max(vert[:,1-axis]) < 0:
            warnings.warn('solid of revolution self-intersecting (axis of rotation intersects cross-section)')
        
        self.RotationVolume, self.CenterMass, self.CenterMassCrossSection = self._geom3D(axis, self._AreaSigned, self.CenterMass, self._Ixy)
        self.RotationSurfaces = self._surfaces(axis, self.EdgesLength, self.EdgesMiddle)
    
    # -------------------------------------------------------
    # geometrical properties of the solid
    
    @staticmethod
    def _geom3D(axis, _AreaSigned, CenterMass, _Ixy):
        """calculates volume and 3D center of mass"""
        # Pappus's centroid theorem
        # https://en.wikipedia.org/wiki/Pappus%27s_centroid_theorem
        RotationVolumeSigned = 2*np.pi * _AreaSigned * CenterMass[1-axis]
        
        # center of mass (in polar coordinates related to product of inertia)
        zS = 2*np.pi * _Ixy / RotationVolumeSigned
        CenterMass, CenterMassCrossSection = [0, zS] , CenterMass
        if axis == 0:
            CenterMass = CenterMass[::-1]
        
        return abs(RotationVolumeSigned), CenterMass, CenterMassCrossSection
    
    
    @staticmethod
    def _surfaces(axis, EdgesLength, EdgesMiddle):
        """calculates surface areas"""
        return 2*np.pi * EdgesLength * abs(EdgesMiddle[:,1-axis])
    
    # -------------------------------------------------------
    # dunder methods
    
    def __repr__(self):
        return f'polygon({self.Vertices}, axis={self._axis})'
    
    def __str__(self):
        return f'Solid of revolution, cross-section polygon with {len(self.Vertices)-1} vertices'
    
    def __abs__(self):
        """returns volume"""
        return self.RotationVolume
    
    # -------------------------------------------------------
    # methods plotting
    
    def plot3d(self, *plt_args, Ncross = 8, Nedge = 0, ax = None, **plt_kwargs):
        """
        3D wireframe plot of solid 
        Ncross: optional, number of cross-sections
        Nedge:  optional, number of circles per edge
        """
        vert = copy.copy(self.Vertices)
        if self._axis == 0:
            vert = vert[:, ::-1]    # x & y switched --> tilted 90°
        if ax is None:
            ax = plt.axes(projection='3d')
        # single label for 3D wireframe
        if 'label' in plt_kwargs:
            label = plt_kwargs.pop('label')
            ax.plot([],[], *plt_args, label=label, **plt_kwargs)
        # plot cross-sections
        for angle in np.linspace(0, 2*np.pi, Ncross+1):
            ax.plot(vert[:,0]*np.cos(angle), vert[:,0]*np.sin(angle), vert[:,1], *plt_args, **plt_kwargs)
        # plot circumferential edges
        for i in range(len(vert)-1):
            coord = np.linspace( vert[i,:], vert[i+1,:], Nedge+1, endpoint=False )
            for point in coord:
                self._plot_circ(*plt_args, radius = point[0], center = (0, 0, point[1] ), **plt_kwargs )
        return ax
    
    
    def plotRotationAxis(self, color = 'k', linestyle = '-.', ax = None, **plt_kwargs):
        """only keyword arguments"""
        if ax is None:
            ax = plt.gca()
        if ax.name == "3d":
            ax.plot([0,0], [0,0], [ax.get_zlim()[0], ax.get_zlim()[1]], 
                    color = color, linestyle = linestyle, **plt_kwargs )
        else:
            if self._axis == 0:
                ax.axhline(y = 0, color = color, linestyle = linestyle, **plt_kwargs)
            elif self._axis == 1:
                ax.axvline(x = 0, color = color, linestyle = linestyle, **plt_kwargs)
        return ax
    
    def plotCenterMassCrossSection(self, *plt_args, ax = None, **plt_kwargs):
        """for 2D plot"""
        if ax is None:
            ax = plt.gca()
        if not plt_args:
            if 'color' not in plt_kwargs:
                plt_kwargs['color']  = 'g'
            if 'marker' not in plt_kwargs:
                plt_kwargs['marker'] = '+'
        ax.plot( *self.CenterMassCrossSection, *plt_args, **plt_kwargs )
        return ax

# #############################################################################
# solid of revolution & triangle class
# #############################################################################

class _solid_and_triangle(_triangle, _solid):
    def __init__(self, vert, axis):
        """calculates geometrical properties of solid of revolution"""
        super().__init__(vert, axis)
