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

socket.plot3d('b-', Ncross = 6, rotAx = True)
plt.gca().view_init(azim=30, elev=15)

# socket.plotCenterMass('bo', label='solid center of mass')

# plt.legend()
# plt.xlabel('mm')
# plt.ylabel('mm')
# plt.gca().set_zlabel('axial / mm')

plt.axis('off')
plt.tight_layout()
plt.show()