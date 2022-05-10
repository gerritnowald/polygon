# -*- coding: utf-8 -*-
"""
Created on Mon May  9 09:48:16 2022

@author: Gerrit Nowald
"""

import numpy as np
import matplotlib.pyplot as plt

from polygon import polygon


L = 5
t = 1


# Vertices = [[0,0],[0,L],[t,L],[t,0]]    # rectangle
Vertices = [[0,0],[0,L],[t,L],[t,t],[L,t],[L,0]]  # L shape

P = polygon(Vertices)
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


plt.figure()
# P.plot()
P2.plot(True)
plt.plot(P2.CenterMass[0],P2.CenterMass[1],"+")
plt.axis('equal')
plt.show()


vert = P2.Vertices
    
ri   = vert[:-1]
rip1 = vert[1:]

xi   = ri[:,0]
yi   = ri[:,1]
xip1 = rip1[:,0]
yip1 = rip1[:,1]

EdgesMiddle = (ri + rip1)/2

FM = xi*yip1 - xip1*yi
AreaSigned = sum(FM)/2
Area = abs(AreaSigned)

CenterMass = (FM @ EdgesMiddle)/3/AreaSigned

# https://en.wikipedia.org/wiki/Second_moment_of_area
Brr    = ri**2 + ri*rip1 + rip1**2
Bxy    = xi*yip1 + 2*xi*yi + 2*xip1*yip1 + xip1*yi
# IyyIxx = abs(FM @ Brr)/12 - Area*CenterMass**2  # correct
IyyIxx =   abs( (FM @ Brr)/12 - AreaSigned*CenterMass**2 )  # correct
Ixy    = - abs( (FM @ Bxy)/24 - AreaSigned*CenterMass[0]*CenterMass[1] )

SecondMomentArea = np.hstack((IyyIxx[::-1], Ixy))


Ixx_analytic = t*(5*L**2-5*L*t+t**2)*(L**2-L*t+t**2)/12/(2*L-t)

Ixy_analytic = L**2*t*(L-t)**2/4/(t-2*L)

Ixy_own = ( (t+(L-t)/2-P.CenterMass[1])*(t/2-P.CenterMass[0])*t*(L-t) +
           (t/2-P.CenterMass[1])*(L/2-P.CenterMass[0])*L*t )


# print(Ixx_analytic)
# print(L**3*t/12)
# print(SecondMomentArea[0])
# print(L*t**3/12)
# print(SecondMomentArea[1])


print(Ixy_analytic)
# print(Ixy_own)
print(SecondMomentArea[2])