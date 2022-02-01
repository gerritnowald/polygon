# polygon
Python module to calculate properties of arbitrary 2D polygons such as area, center of mass, solid of revolution and more!

Input:
- Vert=[x,y]: 2D array of columns of 2D-Coordinates of vertices;
    Polygon can be open or closed (i.e. first = last vertice);
    Area is positive for anti-clockwise order of vertices;
    holes can be defined by cutting in and clockwise order

functions:
- poly_A:      Area
- poly_L:      Lengths of edges
- poly_angles: Inner angles
- poly_CM:     Center of mass
- poly_CMVert: Centers of edges
- poly_SMA:    Second moment of area wrt center of mass
- poly_Vrot:   Volume of solid of revolution
- poly_Arot:   Surface areas of solid of revolution
- poly_plot:   plot polygon
