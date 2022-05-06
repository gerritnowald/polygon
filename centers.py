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


def plot_circ(R, C):
        angle = np.linspace(0, 2*np.pi, 50)
        x = C[0] + R*np.cos(angle)
        y = C[1] + R*np.sin(angle)
        plt.plot(x,y)


CenterInnerCircle = np.roll(triangle.EdgesLength, -1) @ vert / sum(triangle.EdgesLength)
RadiusInnerCircle = 2*triangle.Area/sum(triangle.EdgesLength)

plot_circ(RadiusInnerCircle, CenterInnerCircle)

plt.show()