# -*- coding: utf-8 -*-
"""
Created on Mon May  9 09:48:16 2022

@author: Gerrit Nowald
"""

import matplotlib.pyplot as plt

import sys
sys.path.insert(0,'..')
from polygon_math import polygon

# -----------------------------------------------------------------------------
# examples

# rectangle
L = 5
t = 1
Vertices = [[0,0],[0,L],[t,L],[t,0]]
I_analytic = [L**3*t/12, L*t**3/12, 0]


# L-shape symmetric
# L = 5
# t = 1
# Vertices = [[0,0],[0,L],[t,L],[t,t],[L,t],[L,0]]
# Ixx = t*(5*L**2-5*L*t+t**2)*(L**2-L*t+t**2)/12/(2*L-t)
# Ixy = L**2*t*(L-t)**2/4/(t-2*L)
# I_analytic = [Ixx, Ixx, Ixy]


# L-shape
# a  = 4
# b1 = 2
# b2 = 3
# c  = 1
# Vertices = [[0,0],[0,a],[b1+b2,a],[b1+b2,a-c],[b1,a-c],[b1,0]]
# A = a*b1 + b2*c
# Sx = (b1/2*a*b1 + (b1+b2/2)*b2*c)/A
# Sy = (a/2*a*b1 + (a-c/2)*b2*c)/A
# I_analytic = [
    # a**3*b1/12 + (a/2-Sy)**2*a*b1 + c**3*b2/12 + (a-c/2-Sy)**2*b2*c ,
    # a*b1**3/12 + (b1/2-Sx)**2*a*b1 + c*b2**3/12 + (b1+b2/2-Sx)**2*b2*c,
    # - (b1/2-Sx)*(a/2-Sy)*a*b1 - (b1+b2/2-Sx)*(a-c/2-Sy)*b2*c
    # ]

# -----------------------------------------------------------------------------
# manipulation

P = polygon(Vertices).centerOrigin()


dx = 5
dy = 2

# dx = -5
# dy = 2

# dx = 2
# dy = -5

# dx = -5
# dy = -7

P += [dx, dy]


# P = P.rotate(180,0)
# P = P.rotate(90,0)
# P = P.rotate(-90,0)

# P *= [-1,-1]
# P *= [1,-1]
# P *= [-1,1]

# -----------------------------------------------------------------------------
# comparison results

I_analytic[0] += P.CenterMass[1]**2 * P.Area
I_analytic[1] += P.CenterMass[0]**2 * P.Area
I_analytic[2] -= P.CenterMass[0]*P.CenterMass[1] * P.Area

print(I_analytic)
print(P.SecondMomentArea)

# -----------------------------------------------------------------------------
# plot

plt.close('all')

plt.figure()
P.plot(numbers=True, label='Polygon')
P.plotCenterMass(label='center of mass')
plt.legend()
plt.axis('equal')
plt.show()
