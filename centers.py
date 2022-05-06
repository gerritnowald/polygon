# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 20:18:21 2022

@author: Gerrit Nowald
"""

import numpy as np
import matplotlib.pyplot as plt

from polygon import polygon


vert = np.random.rand(3,2)*10

triangle = polygon(vert)

plt.figure()
triangle.plot(True)
plt.axis('equal')
triangle.plot_CircumscribedCircle()
triangle.plot_Incircle()
plt.show()