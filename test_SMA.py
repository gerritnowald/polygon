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



Vertices = [[0,0],[0,L],[t,L],[t,t],[L,t],[L,0]]
P = polygon(Vertices)
Sx = P.CenterMass[0]
Sy = P.CenterMass[1]


plt.figure()
P.plot()
plt.plot(Sx,Sy,"+")
plt.axis('equal')
plt.show()


vert = np.array(Vertices)
if not np.isclose(vert[-1,], vert[0,]).all():
    vert = np.append(vert,[vert[0,]],axis=0)
FM = vert[:-1,0] * vert[1:,1] - vert[1:,0] * vert[:-1,1]
B = (vert[:-1] + vert[1:])**2 - vert[:-1]*vert[1:]


Ixx_analytic = t*(5*L**2-5*L*t+t**2)*(L**2-L*t+t**2)/12/(2*L-t)
Ixy_analytic = L**2*t*(L-t)**2/4/(t-2*L)

print(Ixx_analytic)
print(P.SecondMomentArea[0])
print(P.SecondMomentArea[1])


print(Ixy_analytic)