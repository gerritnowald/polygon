# -*- coding: utf-8 -*-
"""
Created on Thu May 12 21:38:32 2022

@author: Gerrit Nowald
"""

import numpy as np
import matplotlib.pyplot as plt

import sys
sys.path.insert(0,'..')
from polygon_math import polygon


plt.close('all')
plt.style.use('dark_background')
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)



Vertices = np.random.rand(3,2)*10
triangle = polygon(Vertices)

triangle.plot('o-', ax=ax1)
triangle.plotCenterMass(ax=ax1)
triangle.plotCenterEdges('co', ax=ax1)
triangle.plotOutCircle('--', ax=ax1, linewidth=0.7)
triangle.plotIncircle('--', ax=ax1, linewidth=0.7)
ax1.axis('off')



Vertices = [
    [0, 0],
    [1.75, 4],
    [1.5, 6],
    [1, 7],
    [0.25, 6],
    [0, 5],
    [-0.25, 6],
    [-1, 7],
    [-1.5, 6],
    [-1.75, 4],
    ]
heart = polygon(Vertices)

N = 500
points = np.hstack(( np.random.rand(N,1)*6 - 3, np.random.rand(N,1)*10 - 2 ))

for point in points:
    if heart(point):
        style = "yo"
    else:
        style = "bo"
    ax2.plot(*point, style)
ax2.axis('off')



Vertices = [
    [2.5, 0],
    [4, 0],
    [4, 6],
    [2.5, 6],
    [1, 4.5],
    [1, 1.5]
]
socket = polygon(Vertices, axis=1)

ax3.axis('off')
ax3 = fig.add_subplot(2, 2, 3, projection='3d')
socket.plot3d(Ncross = 6, ax=ax3, color='gold')
socket.plotCenterMass('ro', ax=ax3)
ax3.view_init(azim=30, elev=15)
ax3.axis('off')



Vertices = [[0,0],[5,0],[5,2],[4,1]]
P = polygon(Vertices)

Ptranslated = P + [3,4]
Protated    = P.rotateClockwise(45,[5,0])
Pscaled     = P / 2

P.plot('--', ax=ax4)
Ptranslated.plot(ax=ax4)
Protated.plot(ax=ax4)
Pscaled.plot(ax=ax4)
ax4.axis('equal')
ax4.axis('off')



fig.tight_layout()
# fig.savefig('examples.png', transparent=True)
fig.show()