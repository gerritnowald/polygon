# -*- coding: utf-8 -*-
"""
Created on Sun Dec 18 10:40:32 2022

@author: Gerrit Nowald
"""

import matplotlib.pyplot as plt

import sys
sys.path.insert(0,'..')
from polygon_math import polygon


Vertices = [
    [1, 0],
    [4, 0],
    [4, 6],
    [1, 6],
]
socket = polygon(Vertices, axis=0) - [0,2]


plt.close('all')

plt.figure()
socket.plot()
socket.plotRotationAxis()
socket.plotCenterMass()
socket.plotCenterMassCrossSection()
plt.grid()
plt.axis('equal')
plt.show()