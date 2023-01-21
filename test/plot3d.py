# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 07:25:18 2023

@author: Gerrit Nowald
"""

import numpy as np
import matplotlib.pyplot as plt

def plot(Vertices, *plt_args, numbers = False, ax = None, **plt_kwargs):
    # plots contour of polygon, optionally with numbers of vertices
    if ax is None:
        ax = plt.gca()
    ax.plot(Vertices[:,0], Vertices[:,1], *plt_args, **plt_kwargs)
    if numbers:
        for i in range(len(Vertices)-1):
            ax.text(Vertices[i,0], Vertices[i,1], str(i) )

Vertices = np.array([
    [2.5, 0],
    [4, 0],
    [4, 6],
    [2.5, 6],
    [1, 4.5],
    [1, 1.5],
    [2.5, 0],
])

plt.close('all')
plt.figure()
plot(Vertices, '--', numbers=True, label='crosssection')
# socket.plotRotationAxis(label='axis of rotation')
# socket.plotCenterMass('bo', label='solid center of mass')
# socket.plotCenterMassCrossSection(label='centroid crosssection')
plt.legend()
plt.xlabel('radial / mm')
plt.ylabel('axial / mm')
plt.axis('equal')
plt.show()