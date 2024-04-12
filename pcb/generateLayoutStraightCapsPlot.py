# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

from generateLayoutPlotComponent import writeConnector, lineToPcb, segmentToPcb
from generateLayoutPlotComponent import filledPolygonToPcb

# Export to pcb file

plt.close('all')
fig, axes = plt.subplots(1, 1)
plt.gca().invert_yaxis()
axes.set_aspect('equal')

colours = ['r', 'orange', 'y', 'g', 'b']
xLayerOffset = 0
yLayerOffset = 0
for colour in colours:
    capCols = 61
    xStart = 15.6 + xLayerOffset
    yStart = -21 + 35 + yLayerOffset
    yEnd = yStart + 7.3
    y1Top = yStart + 0.5
    y1Bot = y1Top + 2.0
    y2Top = y1Bot + 0.5
    y2Bot = y2Top + 2.0
    xEnd = xStart + capCols * 2.5
    lineToPcb(axes, xStart, yStart, xStart, yEnd, layer='Edge.Cuts', width=0.1, colour=colour)
    lineToPcb(axes, xEnd, yStart, xEnd, yEnd, layer='Edge.Cuts', width=0.1, colour=colour)
    xPrev = xStart
    for capIdx in range(capCols):
        xNext = xPrev + 2.5
        lineToPcb(axes, xPrev, yStart, xNext, yStart, layer='Edge.Cuts', width=0.1, colour=colour)
        lineToPcb(axes, xPrev, yEnd, xNext, yEnd, layer='Edge.Cuts', width=0.1, colour=colour)
        x1 = xPrev + 0.3
        x2 = xNext - 0.3
        y1 = y1Top + (capIdx -1) % 2
        y2 = y1Bot + (capIdx -1) % 2
        xCap = [x1, x1, x2, x2]
        yCap = [y1, y2, y2, y1]
        filledPolygonToPcb(axes, xCap, yCap, layer='F.Cu', colour=colour)
        y1 = y2Top + (capIdx -1) % 2
        y2 = y2Bot + (capIdx -1) % 2
        xCap = [x1, x1, x2, x2]
        yCap = [y1, y2, y2, y1]
        filledPolygonToPcb(axes, xCap, yCap, layer='F.Cu', colour=colour)
        xPrev = xNext
        
    # connectors for straight caps
    connectorsX = 20.3 + np.arange(5) * 36.7 + xLayerOffset
    connectorsY = np.array([34, 40, 15, 20, 20]) -8.3 + 35 + yLayerOffset
    for idx, (x, y) in enumerate(zip(connectorsX, connectorsY)):
        writeConnector(axes, 1, x, y, idx + 7, colour=colour)
        # Buses for connectors for straight caps
        busX = x - 3
        for busIdx in range(6):
            segmentToPcb(axes=axes,
                      x1=busX,
                      y1=yEnd,
                      x2=busX,
                      y2=y,
                      layer='F.Cu', width=0.2, net=0, colour=colour)
            busX += 0.5
        # Edge cut along bus sides
        lineToPcb(axes=axes,
                  x1= x - 3.5,
                  y1=yEnd,
                  x2=x - 3.5,
                  y2=y,
                  layer='Edge.Cuts', width=0.1, colour=colour)
        lineToPcb(axes=axes,
                  x1=busX,
                  y1=yEnd,
                  x2=busX,
                  y2=y,
                  layer='Edge.Cuts', width=0.1, colour=colour)
    xLayerOffset += 36.7
    yLayerOffset += 0.1
    
