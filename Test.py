# -*- coding: utf-8 -*-
"""
Created on Sun Sep 19 19:50:40 2021

@author: Gerrit Nowald
"""

import numpy as np
import matplotlib.pyplot as plt

from polygon import polygon

plt.close('all')

# def main():
    
# -------------------------------------------------------
# triangle

a = 3
h = 7

A_analytic  = 0.5*a*h
A2_analytic = np.array([a*h**3/36, a**3*h/48])

vert = [
    [0, 0],
    [a, 0],
    [a/2, h],
    ]
triangle = polygon(vert)

# plot polygon
triangle.poly_plot()

# plot center of mass
plt.plot(triangle.CM[0],triangle.CM[1],"+")

# plot centers of edges 
plt.plot(triangle.edgesCM[:,0],triangle.edgesCM[:,1],"o")

# geometry of polygon
print(f"Area: {triangle.area}")
print(f"Lengths of edges: {triangle.edgesL}")
print(f"Inner angles: {triangle.angles}°")

# second moment of area
print(f"second moment of area wrt x-axis: {triangle.SecondMomentArea[0]}")
print(f"second moment of area wrt y-axis: {triangle.SecondMomentArea[1]}")

# geometry of solid of revolution
print(f"Volume of solid of revolution wrt x-axis: {triangle.poly_Vrot()}")
print(f"Volume of solid of revolution wrt y-axis: {triangle.poly_Vrot(axis=1)}")
print(f"Surface of areas solid of revolution wrt x-axis: {triangle.poly_Arot()}")
print(f"Surface of areas solid of revolution wrt y-axis: {triangle.poly_Arot(axis=1)}")

# -------------------------------------------------------
# rectangle

# b = 5
# h = 2

# A_analytic  = b*h
# A2_analytic = np.array([b*h**3, b**3*h])/12

# vert = [
#     [0, 0],
#     [b, 0],
#     [b, h],
#     [0, h],
#     ]

# -------------------------------------------------------
# heart

# N = 1000
# points = np.hstack(( np.random.rand(N,1)*6-3, np.random.rand(N,1)*10-2 ))
# vert = [
#     [0, 0],
#     [1.75,4],
#     [1.5,6],
#     [1,7],
#     [0.25,6],
#     [0,5],
#     [-0.25,6],
#     [-1,7],
#     [-1.5,6],
#     [-1.75,4],
#     ]

# heart = polygon(vert)

# plt.figure()
# for point in points:
#     if heart.isPointInside(point):
#         style = "y+"   
#     else:
#         style = "b+"
#     plt.plot(point[0],point[1],style)
# plt.show()


# if __name__ == "__main__":
#     main()