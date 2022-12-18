# polygon
Python module to calculate geometric properties of arbitrary 2D polygons:
- plotting with matplotlib kwargs (color, linestyle, label)
- area, lengths of edges, inner angles
- order of vertices (clockwise or anti-clockwise)
- centroid (center of mass)
- triangles: centers and radii of incircle and circumscribed (outer) circle
- solid of revolution: volume, surface areas, center of mass
- second moment of area (bending stiffness of beams)
- check if point is inside or on edge of polygon
- translation, rotation and scaling

![](https://github.com/gerritnowald/polygon/blob/main/examples/examples.png)

Article with examples and explanations:
https://gerritnowald.wordpress.com/2022/05/17/polygon-module-object-oriented/

## installation
```
pip install polygon-math
```

## examples:
https://github.com/gerritnowald/polygon/blob/main/examples/examples.ipynb

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
- axis:
	- 0: revolution with respect to x-axis
	- 1: revolution with respect to y-axis

### attributes of polygon object (geometrical properties):
    
    v: Vertex
    e: Edge (next of v)
    - IsClockwise                          Boolean, order of vertices
    - Area
    - Angles[v]                            inner angles
    - EdgesLength[e]
    - EdgesMiddle[xe,ye]                   midpoints of edges
    - CenterMass[x,y]                      centroid / center of mass
    - SecondMomentArea                     [Ixx, Iyy, Ixy], wrt origin
    - solid of revolution, if axis is specified:
        - RotationVolume
        - RotationSurfaces[e]
        - CenterMassCrossSection[r,z]      CenterMass[r,z] now relates to solid
    - for triangles:
        - CenterOuterCircle[x,y]           circumcenter / center of circumsribed (outer) circle
        - RadiusOuterCircle                radius of circumsribed (outer) circle
        - CenterInnerCircle[x,y]           center of incircle (inner circle)
        - RadiusInnerCircle                radius of incircle (inner circle)


### methods of polygon object:
    
    - print(instance)        gives number of vertices
    - abs(instance)          gives area or volume of solid of revolution if axis is defined
    
    - plotting (matplotlib kwargs can be used)
        - plot(numbers=False, **plt_kwargs)        plots polygon, optionally numbers of vertices
        - plot_CenterMass(**plt_kwargs)            plots center of mass, default style red cross
        - for solid of revolution:
            - plot_rotation_axis(**plt_kwargs)     plots axis of rotation, default linestyle black dash-dotted
        - for triangles:
            - plotOutCircle(**plt_kwargs)          plots circumsribed (outer) circle
            - plotIncircle(**plt_kwargs)           plots incircle (inner circle)
    
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


## license:
MIT license. You are free to use the code any way you want, without liability or warranty.

Please reference my work if you use it.
