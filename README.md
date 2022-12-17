# polygon
Python module to calculate geometric properties of arbitrary 2D polygons:
- plotting with matplotlib kwargs (color, linestyle, label)
- area, lengths of edges, inner angles
- order of vertices (clockwise or anti-clockwise)
- centroid (center of mass)
- for triangles: centers and radii of incircle and circumscribed (outer) circle
- check if point is inside or on edge of polygon
- volume and surface areas of solid of revolution
- second moment of area (bending stiffness of beams)
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

### attributes (geometrical properties):
    
    v: Vertex
    e: Edge (next of v)
    - instance.IsClockwise                          Boolean, order of vertices
    - instance.Area
    - instance.Angles[v]                            inner angles
    - instance.EdgesLength[e]
    - instance.EdgesMiddle[xe,ye]                   midpoints of edges
    - instance.CenterMass[x,y]                      centroid / center of mass
    - instance.SecondMomentArea                     [Ixx, Iyy, Ixy], wrt origin
    - solid of revolution, if axis is specified:
        - instance.RotationVolume
        - instance.RotationSurfaces[e]
    - for triangles:
        - instance.CenterOuterCircle[x,y]           circumcenter / center of circumsribed (outer) circle
        - instance.RadiusOuterCircle                radius of circumsribed (outer) circle
        - instance.CenterInnerCircle[x,y]           center of incircle (inner circle)
        - instance.RadiusInnerCircle                radius of incircle (inner circle)


### methods:
    
    - print(instance)        gives number of vertices
    - abs(instance)          gives area or volume of solid of revolution if axis is defined
    
    - plotting (matplotlib kwargs can be used)
        - instance.plot(numbers=False, **plt_kwargs)        plots polygon, optionally numbers of vertices
        - for triangles:
            - instance.plotOutCircle(**plt_kwargs)          plots circumsribed (outer) circle
            - instance.plotIncircle(**plt_kwargs)           plots incircle (inner circle)
    
    - point testing
        - instance(point), instance.isPointInside(point)    true, if point [x,y] is inside of polygon (not on the edge)
        - instance.isPointOnEdge(point)                     true, if point [x,y] is on any edge of polygon
    
    - manipulation (translation, rotation & scaling)
        - instance + [dx,dy] , instance - [dx,dy] , instance.move([dx,dy])
                translation by distances dx,dy in x,y-direction
                                        
        - instance.rotate(angle,[cx,cy]) , instance.rotateClockwise(angle,[cx,cy])
                (counter)-clockwise rotation by angle / °
                with respect to point [cx,cy] (optional, default center of mass)
                                        
        - instance * [fx,fy] , instance / [fx,fy] , instance.scale([fx,fy],[cx,cy])
                scaling by factors fx, fy in x,y-direction (negative: flip)
                with respect to point [cx,cy] (optional, default center of mass)


## license:
MIT license. You are free to use the code any way you want, without liability or warranty.

Please reference my work if you use it.
