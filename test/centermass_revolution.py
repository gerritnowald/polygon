# -*- coding: utf-8 -*-
"""
Created on Sat Dec 17 12:37:05 2022

@author: Gerrit Nowald
"""

import numpy as np
import matplotlib.pyplot as plt

import sys
sys.path.insert(0,'..')
from polygon_math import polygon

# -----------------------------------------------------------------------------
# socket

Vertices = [
    [0, 0],
    [2, 0],
    # [2, 4],
    [0, 4]
]

# Vertices = [
#     [2.5, 0],
#     [4, 0],
#     [4, 6],
#     [1, 6],
#     # [2.5, 6],
#     # [1, 4.5],
#     [1, 1.5]
# ]

socket = polygon(Vertices, axis=1)

print(socket.CenterMass)


plt.close('all')

plt.figure()
socket.plot()
socket.plotRotationAxis()
socket.plotCenterMass(marker='o',color='b')
plt.plot(socket.CenterMassCrossSection[0], socket.CenterMassCrossSection[1], 'g+')
plt.grid()
plt.axis('equal')
plt.show()