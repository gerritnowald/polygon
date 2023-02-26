# polygon
Python module to calculate geometric properties of arbitrary 2D polygons:
- area, centroid (center of mass)
- second moment of area (bending stiffness of beams)
- triangles: incircle and circumscribed (outer) circle
- solid of revolution: volume, surface areas, center of mass
- check if point is inside or on edge of polygon
- move, rotate and scale polygon
- plotting with matplotlib arguments (e.g. color, linestyle, label)

![](https://github.com/gerritnowald/polygon/blob/main/examples/examples.png)

## examples:
https://github.com/gerritnowald/polygon/blob/main/examples/examples.ipynb

## installation:
```
pip install polygon-math
```

### creating a polygon object:
```
from polygon_math import polygon
Vertices = [[x0,y0],[x1,y1],[x2,y2],...]   # 2D-coordinates of vertices
instance = polygon(Vertices)
```
- polygon can be open or closed (i.e. first = last vertex)
- holes can be defined by self-intersecting and opposite order of vertices inside than outside

### creating a solid of revolution:
```
instance = polygon(Vertices, axis)
```
- axis = 0: revolution around x-axis
- axis = 1: revolution around y-axis

### attributes of polygon object (geometrical properties):
    
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

### methods of polygon object:
    
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

### prerequisites
- NumPy
- Matplotlib

## license:
MIT license. You are free to use the code any way you want, without liability or warranty.

Please reference my work if you use it.