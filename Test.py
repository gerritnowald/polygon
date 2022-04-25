# -*- coding: utf-8 -*-
"""
Created on Sun Sep 19 19:50:40 2021

@author: Gerrit Nowald
"""

import numpy as np
import matplotlib.pyplot as plt

from polygon import polygon

plt.close('all')


def main():
    
    # -------------------------------------------------------
    # triangle
    
    a = 3
    h = 7
    
    Area_analytic = 0.5*a*h
    SecondMomentArea_analytic = np.array([a*h**3/36, a**3*h/48])
    
    Vertices = [
        [0, 0],
        [a, 0],
        [a/2, h],
        ]
    triangle = polygon(Vertices)
    
    
    # print attributes of polygon
    # print(triangle)
    
    # plot polygon
    triangle.plot()
    
    # plot center of mass
    plt.plot(triangle.CenterMass[0],triangle.CenterMass[1],"+")
    
    # plot middles of edges 
    plt.plot(triangle.EdgesMiddle[:,0],triangle.EdgesMiddle[:,1],"o")
    
    # geometry of polygon
    print(f"Area: {triangle.Area}")
    print(f"Lengths of edges: {triangle.EdgesLength}")
    print(f"Inner angles: {triangle.Angles}°")
    
    # second moment of area
    print(f"second moment of area wrt x-axis: {triangle.SecondMomentArea[0]}")
    print(f"second moment of area wrt y-axis: {triangle.SecondMomentArea[1]}")
    
    # geometry of solid of revolution
    print(f"Volume of solid of revolution wrt x-axis: {triangle.RotationVolume[0]}")
    print(f"Volume of solid of revolution wrt y-axis: {triangle.RotationVolume[1]}")
    print(f"Surface of areas solid of revolution wrt x-axis: {triangle.RotationSurfaces[:,0]}")
    print(f"Surface of areas solid of revolution wrt y-axis: {triangle.RotationSurfaces[:,1]}")
    
    # -------------------------------------------------------
    # rectangle
    
    # b = 5
    # h = 2
    
    # Area_analytic = b*h
    # SecondMomentArea_analytic = np.array([b*h**3, b**3*h])/12
    
    # Vertices = [
    #     [0, 0],
    #     [b, 0],
    #     [b, h],
    #     [0, h],
    #     ]
    
    # -------------------------------------------------------
    # heart
    
    N = 1000
    points = np.hstack(( np.random.rand(N,1)*6-3, np.random.rand(N,1)*10-2 ))
    Vertices = [
        [0, 0],
        [1.75,4],
        [1.5,6],
        [1,7],
        [0.25,6],
        [0,5],
        [-0.25,6],
        [-1,7],
        [-1.5,6],
        [-1.75,4],
        ]
    
    heart = polygon(Vertices)
    
    plt.figure()
    for point in points:
        if heart.isPointInside(point):
            style = "y+"   
        else:
            style = "b+"
        plt.plot(point[0],point[1],style)
    plt.show()


if __name__ == "__main__":
    main()