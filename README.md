# polygon
Python module to calculate geometric properties of arbitrary 2D polygons such as area, center of mass (centroid), solid of revolution and more!

The functions are explained in detail in this blog post:
https://gerritnowald.wordpress.com/2022/04/02/polygon-module/


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
    - instance.EdgesMiddle[xe,ye]			midpoints of edges
    - instance.CenterMass[x,y]              centroid / center of mass
    - instance.SecondMomentArea[axis]       wrt center of mass
    - instance.RotationVolume[axis]         solid of revolution
    - instance.RotationSurfaces[e,axis]     solid of revolution
	- triangles:
		- instance.CenterOuterCircle[x,y]   circumcenter / center of circumsribed (outer) circle
		- instance.RadiusOuterCircle		radius of circumsribed (outer) circle
    

methods:

    point = [x,y]: point to be tested
    - instance.isPointOnEdge(point)     true, if point is on any edge of polygon
    - instance.isPointInside(point)     true, if point is inside of polygon (not on the edge)
    - instance.plot(numbers=False)      plots edges of polygon, optionally numbers of vertices
	- triangles:
		- instance.plotplot_CircumscribedCircle()	plots circumsribed (outer) circle
