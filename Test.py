# -*- coding: utf-8 -*-
"""
Created on Sun Sep 19 19:50:40 2021

@author: Dr. Gerrit Nowald
"""

from polygon import *

# -------------------------------------------------------
# Input

b = 5
h = 2
Vert = np.array([
    [0, 0],
    [b, 0],
    [b, h],
    [0, h],
    ])
A_analytic  = b*h
A2_analytic = np.array([b*h**3, b**3*h])/12


# a = 3
# h = 7
# Vert = np.array([
#     [0, 0],
#     [a, 0],
#     [a/2, h],
#     ])
# A_analytic  = 0.5*a*h
# A2_analytic = np.array([a*h**3/36, a**3*h/48])


# -------------------------------------------------------
# Calculation (Test)

Vert = close_loop(Vert)




# area
FM   = Vert[0:-1,0] * Vert[1:,1] - Vert[1:,0] * Vert[0:-1,1]
A    = sum(FM)/2   # 0th moment of area

# center of mass
CMVert = ( Vert[0:-1] + Vert[1:] )/2
A1   = (FM @ CMVert)/3    # 1st moment of area
S = A1/A




# stimmt
# Iy = 0
# Iz = 0
# for num in range(np.shape(Vert)[0]-1):
#     Iy += (Vert[num,0] * Vert[num+1,1] - Vert[num+1,0] * Vert[num,1])*((Vert[num,1] + Vert[num+1,1])**2 - Vert[num,1]*Vert[num+1,1])
#     Iz += (Vert[num,0] * Vert[num+1,1] - Vert[num+1,0] * Vert[num,1])*((Vert[num,0] + Vert[num+1,0])**2 - Vert[num,0]*Vert[num+1,0])
# Iy /= 12
# Iz /= 12
# A2 = np.array([Iy, Iz]) - S[::-1]**2*A



B = (Vert[0:-1] + Vert[1:])**2 - Vert[0:-1]*Vert[1:]
A2 = (FM @ B)/12 - S**2*A    # 2nd moment of area
A2 = A2[::-1]


print(A2/A2_analytic)

# -------------------------------------------------------
# Output

# print(f"Area: {poly_A(Vert)}")
# print(f"Lengths of edges: {poly_L(Vert)}")
# print(f"Inner angles: {poly_angles(Vert)}°")

A2 = poly_SMA(Vert)
print(f"second moment of area wrt x-axis: {A2[0]}")
print(f"second moment of area wrt y-axis: {A2[1]}")

# print(f"Volume of solid of revolution wrt x-axis: {poly_Vrot(Vert)}")
# print(f"Volume of solid of revolution wrt y-axis: {poly_Vrot(Vert,axis=1)}")

# print(f"Surface of areas solid of revolution wrt x-axis: {poly_Arot(Vert)}")
# print(f"Surface of areas solid of revolution wrt y-axis: {poly_Arot(Vert,axis=1)}")

# poly_plot(Vert)