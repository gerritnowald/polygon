# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 07:25:18 2023

@author: Gerrit Nowald
"""

import matplotlib.pyplot as plt

import sys
sys.path.insert(0,'..')
from polygon_math import polygon

# -----------------------------------------------------------------------------
# definition

Vertices = [
    [2.5, 0],
    [4, 0],
    [4, 6],
    [2.5, 6],
    [1, 4.5],
    [1, 1.5],
]

socket = polygon(Vertices, axis=1)
        
# -----------------------------------------------------------------------------
# plot

plt.close('all')
plt.figure()

socket.plot3d('b-', Ncross = 6, label='socket')
socket.plotRotationAxis(label='axis of rotation')
socket.plotCenterMass('ro', label='center of mass')

plt.legend()
plt.xlabel('mm')
plt.ylabel('mm')
plt.gca().set_zlabel('axial / mm')

plt.gca().view_init(azim=30, elev=15)
# plt.axis('off')
plt.tight_layout()
plt.show()


plt.figure()
socket.plot(numbers=True, label='crosssection')
socket.plotRotationAxis(label='axis of rotation')
socket.plotCenterMass('bo', label='solid center of mass')
socket.plotCenterMassCrossSection(label='centroid crosssection')
plt.legend()
plt.xlabel('radial / mm')
plt.ylabel('axial / mm')
plt.axis('equal')
plt.show()