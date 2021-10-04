# polygon
Python module to calculate properties of arbitrary 2D polygons such as area, center of mass, solid of revolution and more!

Input:
- Vert: 2D array of 2D-Coordinates of vertices, Vert=[x,y]
    Polygon can be open or closed (first = last vertice)
    Area is positive for anti-clockwise order of vertices
    holes can be defined by opposite order

functions:
- poly_A(Vert)              Area
- poly_L(Vert)              Lengths of edges
- poly_angles(Vert)         Inner angles
- poly_CM(Vert)             Center of mass
- poly_CMVert(Vert)         Centers of edges
- poly_Vrot(Vert, axis=0)   Volume of solid of revolution
- poly_Arot(Vert, axis=0)   Surface areas of solid of revolution
- poly_plot(Vert)           plot polygon
