# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 07:25:18 2023

@author: Gerrit Nowald
"""

import numpy as np
import matplotlib.pyplot as plt

def _plot_circ(*plt_args, radius = 1, center = (0,0,0), Npoints = 50, ax = None, **plt_kwargs ):
    if ax is None:
        ax = plt.gca()
    # calculate circle coordinates
    angle = np.linspace(0, 2*np.pi, Npoints+1)
    x = center[0] + radius*np.cos(angle)
    y = center[1] + radius*np.sin(angle)
    if len(center) == 3:
        z = center[2] * np.ones( Npoints+1 )
    coord = np.vstack((x, y, z)).T
    # plot circle
    if ax.name == "3d":
        ax.plot( coord[:,0], coord[:,1], coord[:,2], *plt_args, **plt_kwargs )
    else:
        ax.plot( coord[:,0], coord[:,1], *plt_args, **plt_kwargs )
        ax.axis('equal')
            
def plot3d(Vertices, *plt_args, Ncross = 8, Nedge = 1, rotAx = False, numbers = False, ax = None, **plt_kwargs):
    # plots solid of revolution, optionally with numbers of vertices
    if ax is None:
        ax = plt.axes(projection='3d')
    # plot cross-sections
    for angle in np.linspace(0, 2*np.pi, Ncross+1):
        ax.plot(Vertices[:,0]*np.cos(angle), Vertices[:,0]*np.sin(angle), Vertices[:,1], *plt_args, **plt_kwargs)
    # plot circumferential edges
    for i in range(len(Vertices)-1):
        coord = np.linspace( Vertices[i,:], Vertices[i+1,:], Nedge+2 )
        for vert in coord:
            _plot_circ(*plt_args, radius = vert[0], center = (0, 0, vert[1] ), linestyle=':' )
    # plot axis of rotation
    if rotAx:
        plt.plot([0,0], [0,0], [min(Vertices[:,1]), max(Vertices[:,1])], 'k-.')
    # plot numbers of vertices & edges
    if numbers:
        for i in range(len(Vertices)-1):
            ax.text(Vertices[i,0], 0, Vertices[i,1], str(i), c='r' )
            # ax.text(self.EdgesMiddle[i,0], self.EdgesMiddle[i,1], str(i) )

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

plot3d(Vertices, 'b--', Ncross = 5, Nedge = 10 )

# socket.plotCenterMass('bo', label='solid center of mass')

# plt.legend()
# plt.xlabel('mm')
# plt.ylabel('mm')
# plt.gca().set_zlabel('axial / mm')

plt.axis('off')

plt.show()