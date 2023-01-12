# -*- coding: utf-8 -*-
"""
Created on Thu May 12 21:38:32 2022

@author: Gerrit Nowald
"""

import numpy as np
import matplotlib.pyplot as plt

from polygon_math import polygon


plt.figure()
plt.style.use('dark_background')



Vertices = np.random.rand(3,2)*10
triangle = polygon(Vertices)

plt.subplot(221)
triangle.plot(marker='o')
triangle.plotCenterMass()
triangle.plotCenterEdges()
triangle.plotOutCircle(linestyle='--', linewidth=0.7)
triangle.plotIncircle(linestyle='--', linewidth=0.7)
plt.axis('off')



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

plt.subplot(222)
for point in points:
    if heart(point):
        style = "yo"
    else:
        style = "bo"
    plt.plot(*point, style)
plt.axis('off')



Vertices = [
    [0, 0],
    [10, 0],
    [10, 1],
    [6, 2],
    [6, 18],
    [10, 19],
    [10, 20],
    [0, 20],
    [0, 19],
    [4, 18],
    [4, 2],
    [0, 1]
]
beam = polygon(Vertices)

plt.subplot(223)
beam.plot()
beam.plotCenterMass()
plt.axis('equal')
plt.axis('off')



Vertices = [[0,0],[5,0],[5,2],[4,1]]
P = polygon(Vertices)

Ptranslated = P + [3,4]
Protated    = P.rotateClockwise(45,[5,0])
Pscaled     = P / 2

plt.subplot(224)
P.plot(linestyle='--')
Ptranslated.plot()
Protated.plot()
Pscaled.plot()
plt.axis('equal')
plt.axis('off')



# Vertices = [
#     [2.5, 0],
#     [4, 0],
#     [4, 6],
#     [2.5, 6],
#     [1, 4.5],
#     [1, 1.5]
# ]
# socket = polygon(Vertices, axis=1)

# socket.plot()
# plt.plot([0,0], [0,6], 'w-.')
# plt.axis('equal')
# plt.axis('off')



plt.tight_layout()
# plt.savefig('examples.png', transparent=True)
plt.show()