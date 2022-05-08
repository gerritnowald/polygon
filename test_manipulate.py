# -*- coding: utf-8 -*-
"""
Created on Sun May  8 06:36:43 2022

@author: Gerrit Nowald
"""

import numpy as np
import matplotlib.pyplot as plt

from polygon import polygon

Vertices = np.array([[0,0],[5,0],[5,2],[4,1]])
P = polygon(Vertices,0)

# P *= [2,0.5]
# P2 = P * [0.5,1]
# P2 = P / 2
# P2 = P.scale([-2,3])

# P += [2,4]
# P2 = P + [3,4]
# P2 = P - 2
# P2 = P.move([-2,3])

# P2 = P.rotateClockwise(45)

P2 = (P.rotate(45) - P.CenterMass)/2

P.plot(True)
P2.plot()
plt.axis('equal')
plt.show()