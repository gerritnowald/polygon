# -*- coding: utf-8 -*-
"""
Created on Sat Dec 17 12:37:05 2022

@author: Gerrit Nowald
"""

import numpy as np
import matplotlib.pyplot as plt

from polygon_math import polygon

# -----------------------------------------------------------------------------
# socket

Vertices = [
    [2.5, 0],
    [4, 0],
    [4, 6],
    [1, 6],
    # [2.5, 6],
    # [1, 4.5],
    [1, 1.5]
]
socket = polygon(Vertices, axis=1)


plt.close('all')

# plt.figure()
# plt.axvline(x = 0, color='k', linestyle = '-.' )
# socket.plot()
# plt.plot(socket.CenterMass[0], socket.CenterMass[1], 'r+')
# plt.plot(socket.CenterMassCrossSection[0], socket.CenterMassCrossSection[1], 'g+')
# plt.grid()
# plt.axis('equal')
# plt.show()

# -----------------------------------------------------------------------------
# beam

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


plt.figure()
beam.plot(c='k', label='crosssection')
plt.plot(beam.CenterMass[0], beam.CenterMass[1], "r+", label='center of mass')
plt.legend()
plt.xlabel('x / cm')
plt.ylabel('y / cm')
plt.axis('equal')
plt.show()

print(f"second moment of area x-axis: { int(beam.SecondMomentArea[0])} cm^4")
print(f"second moment of area y-axis: { int(beam.SecondMomentArea[1])} cm^4")
print(f"product second moment of area: {int(beam.SecondMomentArea[2])} cm^4")