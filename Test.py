# -*- coding: utf-8 -*-
"""
Created on Sun Sep 19 19:50:40 2021

@author: Dr. Gerrit Nowald
"""

from polygon import *

# -------------------------------------------------------
# Input

Vert = np.array([
    [0, 0],
    [2, 0],
    [2, 4],
    [0, 4],
    ])

# Vert = np.array([
#     [0, 0],
#     [4, 0],
#     [2, 2],
#     ])

Vert = close_loop(Vert)




# area
FM   = Vert[0:-1,0] * Vert[1:,1] - Vert[1:,0] * Vert[0:-1,1]
A    = sum(FM)/2   # 0th moment of area

# center of mass
CMVert = ( Vert[0:-1] + Vert[1:] )/2
A1   = (FM @ CMVert)/3    # 1st moment of area
S = A1/A







B = (Vert[0:-1] + Vert[1:])**2 - Vert[0:-1]*Vert[1:]
A2 = (FM @ B)/12    # 2nd moment of area










# -------------------------------------------------------
# Output

# print(f"Area: {poly_A(Vert)}")
# print(f"Lengths of edges: {poly_L(Vert)}")

# print(f"Volume of solid of revolution wrt x-axis: {poly_Vrot(Vert)}")
# print(f"Volume of solid of revolution wrt y-axis: {poly_Vrot(Vert,axis=1)}")

# print(f"Surface of areas solid of revolution wrt x-axis: {poly_Arot(Vert)}")
# print(f"Surface of areas solid of revolution wrt y-axis: {poly_Arot(Vert,axis=1)}")

# print(f"Inner angles: {poly_angles(Vert)}°")

# poly_plot(Vert)