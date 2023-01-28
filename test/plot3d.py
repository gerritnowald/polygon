# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 07:25:18 2023

@author: Gerrit Nowald
"""

import matplotlib.pyplot as plt
import numpy as np

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
# 

def _plot_circ(*plt_args, radius = 1, center = (0,0), Npoints = 50, ax = None, **plt_kwargs ):
    # plots circle in x,y plane
    if ax is None:
        ax = plt.gca()
    # calculate circle coordinates
    angle = np.linspace(0, 2*np.pi, Npoints+1)
    x = center[0] + radius*np.cos(angle)
    y = center[1] + radius*np.sin(angle)
    # plot circle
    try:
        z = center[2] * np.ones( Npoints+1 )
        ax.plot( x, y, z, *plt_args, **plt_kwargs )
    except:
        ax.plot( x, y, *plt_args, **plt_kwargs )
        ax.axis('equal')

def plot3d(Vertices, *plt_args, Ncross = 8, Nedge = 0, rotAx = False, ax = None, **plt_kwargs):
    # plots solid of revolution
    vert = np.array(Vertices)
    if ax is None:
        ax = plt.axes(projection='3d')
    if 'label' in plt_kwargs:
        label = plt_kwargs.pop('label')
    # plot cross-sections
    for angle in np.linspace(0, 2*np.pi, Ncross+1):
        ax.plot(vert[:,0]*np.cos(angle), vert[:,0]*np.sin(angle), vert[:,1], *plt_args, **plt_kwargs)
    if label:
        ax.plot([],[], label=label)
    # plot circumferential edges
    for i in range(len(vert)-1):
        coord = np.linspace( vert[i,:], vert[i+1,:], Nedge+1, endpoint=False )
        for point in coord:
            _plot_circ(*plt_args, radius = point[0], center = (0, 0, point[1] ) )
    # plot axis of rotation
    if rotAx:
        plt.plot([0,0], [0,0], [min(vert[:,1]), max(vert[:,1])], 'k-.')
        
# -----------------------------------------------------------------------------
# plot

plt.close('all')
plt.figure()

# socket.plot3d('b-', Ncross = 6, rotAx = True)
plot3d(Vertices, 'b-', Ncross = 6, rotAx = True, label='socket')

socket.plotCenterMass('ro', label='center of mass')

plt.legend()
plt.xlabel('mm')
plt.ylabel('mm')
plt.gca().set_zlabel('axial / mm')

plt.gca().view_init(azim=30, elev=15)
# plt.axis('off')
plt.tight_layout()
plt.show()


# plt.figure()
# socket.plot(numbers=True, label='crosssection')
# socket.plotRotationAxis(label='axis of rotation')
# socket.plotCenterMass('bo', label='solid center of mass')
# socket.plotCenterMassCrossSection(label='centroid crosssection')
# plt.legend()
# plt.xlabel('radial / mm')
# plt.ylabel('axial / mm')
# plt.axis('equal')
# plt.show()