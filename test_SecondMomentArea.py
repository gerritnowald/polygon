# -*- coding: utf-8 -*-
"""
Created on Mon May  9 09:48:16 2022

@author: Gerrit Nowald
"""

import matplotlib.pyplot as plt

from polygon import polygon

# -----------------------------------------------------------------------------
# examples

# rectangle
# L = 5
# t = 1
# Vertices = [[0,0],[0,L],[t,L],[t,0]]
# Ixx_analytic = [L**3*t/12, L*t**3/12]
# Ixy_analytic = 0


# L-shape symmetric
# L = 5
# t = 1
# Vertices = [[0,0],[0,L],[t,L],[t,t],[L,t],[L,0]]
# Ixx_analytic = t*(5*L**2-5*L*t+t**2)*(L**2-L*t+t**2)/12/(2*L-t)
# Ixy_analytic = L**2*t*(L-t)**2/4/(t-2*L)


# L-shape
a  = 4
b1 = 2
b2 = 3
c  = 1
Vertices = [[0,0],[0,a],[b1+b2,a],[b1+b2,a-c],[b1,a-c],[b1,0]]
A = a*b1 + b2*c
Sx = (b1/2*a*b1 + (b1+b2/2)*b2*c)/A
Sy = (a/2*a*b1 + (a-c/2)*b2*c)/A
Ixx_analytic = [
    a**3*b1/12 + (a/2-Sy)**2*a*b1 + c**3*b2/12 + (a-c/2-Sy)**2*b2*c ,
    a*b1**3/12 + (b1/2-Sx)**2*a*b1 + c*b2**3/12 + (b1+b2/2-Sx)**2*b2*c
    ]
Ixy_analytic = - (b1/2-Sx)*(a/2-Sy)*a*b1 - (b1+b2/2-Sx)*(a-c/2-Sy)*b2*c


P = polygon(Vertices)

# -----------------------------------------------------------------------------
# manipulation

# P -= P.CenterMass
# P *= [1,-1]


P2 = P

# P2 = P - [5,0]
# P2 = P - [0,5]
# P2 = P - [5,5]

# P2 = P.rotate(90,0)
# P2 = P.rotate(-90,0)
# P2 = P.rotate(180,0)

# P2 = P*[-1,1]
# P2 = P*[1,-1]
# P2 = P*[-1,-1]

# -----------------------------------------------------------------------------
# plot

plt.figure()
# P.plot()
P2.plot(True)
plt.plot(P2.CenterMass[0],P2.CenterMass[1],"+")
plt.axis('equal')
plt.show()

# -----------------------------------------------------------------------------
# comparison results

print(Ixx_analytic)
print(P2.SecondMomentArea[0])
print(P2.SecondMomentArea[1])

print(Ixy_analytic)
print(P2.SecondMomentArea[2])