# -*- coding: utf-8 -*-
"""
Created on Sat Dec 17 12:37:05 2022

@author: Gerrit Nowald
"""

import matplotlib.pyplot as plt

import sys
sys.path.insert(0,'..')
from polygon_math import polygon

# -----------------------------------------------------------------------------
# definition

Vertices = [
    [0, 0],
    [2, 0],
    # [2, 4],
    [0, 4]
]

solid = polygon(Vertices, axis=1)

# -----------------------------------------------------------------------------
# manipulation

# solid *= [-1,1]
# solid *= [1,-1]

# solid -= [0,5]
# solid -= [5,0]

# -----------------------------------------------------------------------------
# output

print(solid.RotationVolume)
print(solid.RotationSurfaces)
print(solid.CenterMass)

# -----------------------------------------------------------------------------
# plot

plt.close('all')

plt.figure()
solid.plot(numbers=True)
solid.plotRotationAxis()
solid.plotCenterMass(marker='o',color='b')
solid.plotCenterMassCrossSection()
plt.grid()
plt.axis('equal')
plt.show()
