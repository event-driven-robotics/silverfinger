# -*- coding: utf-8 -*-
"""
Created on Mon May  3 12:37:53 2021

@author: sbamford
"""

import numpy as np

def str3(num):
    return f'{num:.3f}'


def lineToPcb(axes, x1, y1, x2, y2, layer='Edge.Cuts', width=0.1, colour='k'):
    axes.plot([x1, x2], [y1, y2], colour)


def segmentToPcb(axes, x1, y1, x2, y2, layer='F.Cu', width=0.2, net=0, colour='k'):
    axes.plot([x1, x2], [y1, y2], colour)


def textToPcb(axes, x, y, text, rotation, colour='k'):
    axes.text(x, y, text, rotation=rotation)
    
    
def filledPolygonToPcb(axes, xArray, yArray, layer='F.Adhes', colour='k'):
    xArray = np.append(xArray, xArray[0])
    yArray = np.append(yArray, yArray[0])
    axes.plot(xArray, yArray, colour)
    
    
def writeConnector(axes, orientation, x, y, refNo, colour='k'):
    # x and y are xinnerext
    # connector component is defined wrt connector hole 1
    xl = x - orientation * 4.7
    xr = xl + orientation * 6.15
    yt = y
    yb = yt + orientation * 8.65
    #lineToPcb(file, axes, xl, yt, xr, yt)
    lineToPcb(axes, xl, yb, xr, yb, colour=colour)
    lineToPcb(axes, xl, yt, xl, yb, colour=colour)
    lineToPcb(axes, xr, yt, xr, yb, colour=colour)
    
    xHole = x + orientation * -2.95
    yHole = y + orientation * 1.8
    
    segments = [
    [-0.95, 1.8, -0.95, 1.8],
    [0.05, 1.8, 0.05, 1.8],
    [-2.45, 1.8, -2.45, 1.8],
    [-0.95, 1.8, -0.95, 1.225],
    [-1.3, 0.825, -1.3, -1.275],
    [-0.95, 1.225, -1.3, 0.825],
    [-2.54, -5.08, -4.1, -3.52],
    [-4.1, -3.52, -4.1, 1.025],
    [-4.1, 1.025, -3.525, 1.6],
    [-3.525, 1.6, -2.625, 1.6],
    [-2.625, 1.625, -2.45, 1.8],
    [-2.625, 1.6, -2.625, 1.625],
    [0.05, 1.8, 0.05, 1.6],
    [0.05, 1.6, 0.3, 1.35],
    [0.3, 1.35, 1.15, 1.35],
    [1.15, 1.35, 1.25, 1.25],
    [1.25, -3.83, 0, -5.08],
    [1.25, 1.25, 1.25, -3.83],
    [-1.265, -1.275, 0, -2.54],
    [-1.3, -1.275, -1.265, -1.275],
    [-3.7, 0.775, -3.7, -1.4],
    [-3.7, -1.4, -3.68, -1.4],
    [-2.375, 1.175, -3.3, 1.175],
    [-3.3, 1.175, -3.7, 0.775],
    [-3.68, -1.4, -2.54, -2.54],
    [-1.95, 1.6, -2.375, 1.175],
    [-1.95, 1.8, -1.95, 1.6],
    [-1.45, 1.8, -1.45, 1.45],
    [-1.45, 1.45, -2.54, 0],
    [-0.45, 0.9, 0, 0],
    [-0.45, 1.8, -0.45, 0.9],
    ]

    for x1, y1, x2, y2 in segments:
        x1 = xHole - orientation * x1
        x2 = xHole - orientation * x2
        y1 = yHole - orientation * y1
        y2 = yHole - orientation * y2
        segmentToPcb(axes, x1, y1, x2, y2, colour=colour)
    # final edge cuts
    lineToPcb(axes, xr, yt, x, yt, colour=colour)
    lineToPcb(axes, xl, yt, xl + orientation * 1.2, yt, colour=colour)
    # drawing rigid area
    xArray = np.array([xl, xr, xr, xl])
    yArray = np.array([yt, yt, yb, yb])
    filledPolygonToPcb(axes, xArray, yArray, layer='Dwgs.User', colour=colour)
    