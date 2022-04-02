# polygon
Python module to calculate geometric properties of arbitrary 2D polygons such as area, center of mass, solid of revolution and more!

The functions are explained in detail in this blog post:
https://gerritnowald.wordpress.com/2022/04/02/polygon-module/

inputs:
- vert=[x,y]: column-array of 2D-coordinates of vertices
    Polygon can be open or closed (i.e. first = last vertice)
    Area is positive for anti-clockwise order of vertices
    holes can be defined by cutting in and clockwise order
- point=[x,y]: point to be tested
- axis: 0: with respect to x-axis
        1: with respect to y-axis

functions:

- poly_plot(vert):               plot polygon

- isPointOnEdge(vert, point):    true, if point is on any edge of polygon
- isPointInPolygon(vert, point): true, if point is inside of polygon (not on the edge)

- poly_L(vert):                  lengths of edges
- poly_CMvert(vert):             centers of edges
- poly_angles(vert):             inner angles

- poly_A(vert):                  area
- poly_CM(vert):                 center of mass
- poly_SMA(vert):                second moment of area wrt center of mass

- poly_Vrot(vert, axis=0):       volume of solid of revolution
- poly_Arot(vert, axis=0):       surface areas of solid of revolution
