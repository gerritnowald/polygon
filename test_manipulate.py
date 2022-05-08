# -*- coding: utf-8 -*-
"""
Created on Sun May  8 06:36:43 2022

@author: Gerrit Nowald
"""

import numpy as np
import matplotlib.pyplot as plt

from polygon import polygon

Vertices = [[0,0],[5,0],[5,2],[4,1]]

P = polygon(Vertices,0)

P2 = P.move(-3)



P.plot(True)
P2.plot()
plt.axis('equal')
plt.show()