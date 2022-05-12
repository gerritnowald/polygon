# -*- coding: utf-8 -*-
"""
Created on Thu May 12 21:38:32 2022

@author: Gerrit Nowald
"""

import numpy as np
import matplotlib.pyplot as plt

from polygon_math import polygon


Vertices = np.random.rand(3,2)*10
triangle = polygon(Vertices)

plt.figure()

plt.subplot(221)
triangle.plot(numbers=True, c='k', marker='o', label='Polygon')
plt.plot(triangle.CenterMass[0],    triangle.CenterMass[1],    "r+", label='center of mass')
plt.plot(triangle.EdgesMiddle[:,0], triangle.EdgesMiddle[:,1], "ko")
triangle.plotOutCircle(c='b', linestyle='--', linewidth=0.7, label='circumscribed circle')
triangle.plotIncircle( c='g', linestyle='--', linewidth=0.7, label='incircle')


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
# fig, ax = plt.subplots(222)
for point in points:
    if heart(point):
        style = "yo"
    else:
        style = "bo"
    plt.plot(point[0], point[1], style)
# ax.set_axis_off()


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
beam.plot(c='k', label='crosssection')
plt.plot(beam.CenterMass[0], beam.CenterMass[1], "r+", label='center of mass')
plt.axis('equal')


Vertices = [[0,0],[5,0],[5,2],[4,1]]
P = polygon(Vertices)

Ptranslated = P + [3,4]
Protated    = P.rotateClockwise(45,[5,0])
Pscaled     = P / 2

plt.subplot(224)
P.plot(label='original', linestyle='--')
Ptranslated.plot(label='translated')
Protated.plot(label='rotated')
Pscaled.plot(label='scaled')
plt.axis('equal')

plt.tight_layout()
plt.savefig('examples.png')
# plt.show()