# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

from generateLayoutPcbTemplate import writeTemplate
from generateLayoutPcbComponent import writeConnector, lineToPcb, segmentToPcb
from generateLayoutPcbComponent import filledPolygonToPcb, textToPcb

# Export to pcb file

def generateLayoutPcb(numSpirals, running,
                      numWiresBus, width,
                      edgeCuts, caps,
                      orientation,
                      busToCapTargets,
                      xBus, yBus,
                      xInner2d, yInner2d,
                      xOuter2d, yOuter2d,
                      xOffset, yOffset,
                      xInnerExt, yInnerExt,
                      xOuterExt, yOuterExt,
                      xOuterRet, yOuterRet,
                      xInnerBus, yInnerBus,
                      xOuterBus, yOuterBus):
    plt.close('all')
    fig, axes = plt.subplots(1, 1)
    plt.gca().invert_yaxis()
    axes.set_aspect('equal')
    step = 10
    with open('autoGen.kicad_pcb', 'w') as file:
        writeTemplate(file)
        for spiralIdx in range(numSpirals):
            # Place connectors
            writeConnector(file, axes, orientation[0, spiralIdx],
                           xInnerExt[0, spiralIdx] + xOffset[spiralIdx],
                           yInnerExt[0, spiralIdx] + yOffset[spiralIdx],
                           spiralIdx)
            
            # Silk screen - number the spirals
            xText = xInner2d[0, spiralIdx] * 0.75 + xOuter2d[0, spiralIdx] * 0.25 + xOffset[spiralIdx]
            yText = yInner2d[0, spiralIdx] * 0.75 + yOuter2d[0, spiralIdx] * 0.25 + yOffset[spiralIdx]
            textToPcb(file, axes, xText, yText, str(spiralIdx), 0)

            finalIndex = np.where(running[:, spiralIdx] == False)[0][0]
            
            # Silk screen - Quarter circles
            quarterCircleLineIds = list(range(0, finalIndex, 90))
            for lineIdx in quarterCircleLineIds:
                lineToPcb(file=file, axes=axes,
                      x1=xInner2d[lineIdx, spiralIdx] + xOffset[spiralIdx],
                      y1=yInner2d[lineIdx, spiralIdx] + yOffset[spiralIdx],
                      x2=xOuter2d[lineIdx, spiralIdx] + xOffset[spiralIdx],
                      y2=yOuter2d[lineIdx, spiralIdx] + yOffset[spiralIdx],
                      layer='F.SilkS', width=0.12)
                lineToPcb(file=file, axes=axes,
                      x1=xInner2d[lineIdx, spiralIdx] + xOffset[spiralIdx],
                      y1=yInner2d[lineIdx, spiralIdx] + yOffset[spiralIdx],
                      x2=xOuter2d[lineIdx, spiralIdx] + xOffset[spiralIdx],
                      y2=yOuter2d[lineIdx, spiralIdx] + yOffset[spiralIdx],
                      layer='B.SilkS', width=0.12)
            fullCircleLineIds = list(range(360, finalIndex, 360))
            for idx, lineIdx in enumerate(fullCircleLineIds):
                # Silk screen - number the spirals
                xText = xInner2d[lineIdx, spiralIdx] * 0.75 + xOuter2d[lineIdx, spiralIdx] * 0.25 + xOffset[spiralIdx]
                yText = yInner2d[lineIdx, spiralIdx] * 0.75 + yOuter2d[lineIdx, spiralIdx] * 0.25 + yOffset[spiralIdx]
                textToPcb(file, axes, xText, yText, str(idx + 1), 0)
        
            # peripheral edge
            lineToPcb(file=file, axes=axes,
                      x1=xInner2d[finalIndex, spiralIdx] + xOffset[spiralIdx],
                      y1=yInner2d[finalIndex, spiralIdx] + yOffset[spiralIdx],
                      x2=xOuter2d[finalIndex, spiralIdx] + xOffset[spiralIdx],
                      y2=yOuter2d[finalIndex, spiralIdx] + yOffset[spiralIdx],
                      layer='Edge.Cuts', width=0.1)
            # extension
            lineToPcb(file=file, axes=axes,
                      x1=xInner2d[0, spiralIdx] + xOffset[spiralIdx],
                      y1=yInner2d[0, spiralIdx] + yOffset[spiralIdx],
                      x2=xInnerExt[0, spiralIdx] + xOffset[spiralIdx],
                      y2=yInnerExt[0, spiralIdx] + yOffset[spiralIdx],
                      layer='Edge.Cuts', width=0.1)
            ''' We don't want this - we want to carry on to the connector
            lineToPcb(file=file, axes=axes,
                      x1=xInnerExt[0, spiralIdx] + xOffset[spiralIdx],
                      y1=yInnerExt[0, spiralIdx] + yOffset[spiralIdx],
                      x2=xOuterExt[0, spiralIdx] + xOffset[spiralIdx],
                      y2=yOuterExt[0, spiralIdx] + yOffset[spiralIdx],
                      layer='Edge.Cuts', width=0.1)
            '''
            lineToPcb(file=file, axes=axes,
                      x1=xOuterExt[0, spiralIdx] + xOffset[spiralIdx],
                      y1=yOuterExt[0, spiralIdx] + yOffset[spiralIdx],
                      x2=xOuterRet[0, spiralIdx] + xOffset[spiralIdx],
                      y2=yOuterRet[0, spiralIdx] + yOffset[spiralIdx],
                      layer='Edge.Cuts', width=0.1)
            lineToPcb(file=file, axes=axes,
                      x1=xOuterRet[0, spiralIdx] + xOffset[spiralIdx],
                      y1=yOuterRet[0, spiralIdx] + yOffset[spiralIdx],
                      x2=xOuter2d[0, spiralIdx] + xOffset[spiralIdx],
                      y2=yOuter2d[0, spiralIdx] + yOffset[spiralIdx],
                      layer='Edge.Cuts', width=0.1)
            
            # Bus extension
            for busIdx in range(numWiresBus):
                segmentToPcb(file=file, axes=axes,
                          x1=xInnerBus[busIdx, spiralIdx] + xOffset[spiralIdx],
                          y1=yInnerBus[busIdx, spiralIdx] + yOffset[spiralIdx],
                          x2=xOuterBus[busIdx, spiralIdx] + xOffset[spiralIdx],
                          y2=yOuterBus[busIdx, spiralIdx] + yOffset[spiralIdx],
                          layer='F.Cu', width=0.2, net=0)
    
            #inner edge
            segIds = list(range(0, finalIndex, step))
            segIds.append(finalIndex)
            for segIdxPrev, segIdxNext in zip(segIds[:-1], segIds[1:]):
                lineToPcb(file=file, axes=axes,
                          x1=xInner2d[segIdxPrev, spiralIdx] + xOffset[spiralIdx],
                          y1=yInner2d[segIdxPrev, spiralIdx] + yOffset[spiralIdx],
                          x2=xInner2d[segIdxNext, spiralIdx] + xOffset[spiralIdx],
                          y2=yInner2d[segIdxNext, spiralIdx] + yOffset[spiralIdx],
                          layer='Edge.Cuts', width=0.1)
            # outer edge
            for segIdxPrev, segIdxNext in zip(segIds[:-1], segIds[1:]):
                lineToPcb(file=file, axes=axes,
                          x1=xOuter2d[segIdxPrev, spiralIdx] + xOffset[spiralIdx],
                          y1=yOuter2d[segIdxPrev, spiralIdx] + yOffset[spiralIdx],
                          x2=xOuter2d[segIdxNext, spiralIdx] + xOffset[spiralIdx],
                          y2=yOuter2d[segIdxNext, spiralIdx] + yOffset[spiralIdx],
                          layer='Edge.Cuts', width=0.1)
            
            # adhesive line
            xi = xInner2d[:, spiralIdx]
            xo = xOuter2d[:, spiralIdx]
            yi = yInner2d[:, spiralIdx]
            yo = yOuter2d[:, spiralIdx]
            w = width[:, spiralIdx]
            xAdhesive = xOffset[spiralIdx] + xi + (xo-xi) / w # * 1.0 i.e. 1 mm wide
            yAdhesive = yOffset[spiralIdx] + yi + (yo-yi) / w # * 1.0 i.e. 1 mm wide
            xAdhesive = xAdhesive[segIds]
            yAdhesive = yAdhesive[segIds]
            if spiralIdx == 5:
                xAdhesive = np.append(xAdhesive, [102.1])
                yAdhesive = np.append(yAdhesive, [57.32 + 35])
            if spiralIdx == 6:
                xAdhesive = np.append(xAdhesive, [84, 73, 53, 47, 44.5, 39])
                yAdhesive = np.append(yAdhesive, [108, 112, 109, 90, 86, 81])
            filledPolygonToPcb(file=file, axes=axes,
                               xArray=xAdhesive,
                               yArray=yAdhesive,
                               layer='F.Adhes')
            
            # Edge cuts between caps
            xi, xo, yi, yo = edgeCuts[spiralIdx]
            for capIdx in range(len(xi)):
                lineToPcb(file=file, axes=axes,
                          x1=xi[capIdx] + xOffset[spiralIdx],
                          y1=yi[capIdx] + yOffset[spiralIdx],
                          x2=xo[capIdx] + xOffset[spiralIdx],
                          y2=yo[capIdx] + yOffset[spiralIdx],
                          layer='Edge.Cuts', width=0.1)
            # Cap plates
            xfic, yfic, xfoc, yfoc, xloc, yloc, xlic, ylic = caps[spiralIdx]
            for capIdx in range(len(xfic)):
                xCap = [xfic[capIdx], xfoc[capIdx], xloc[capIdx], xlic[capIdx]]
                xCap = np.array(xCap) + xOffset[spiralIdx]
                yCap = [yfic[capIdx], yfoc[capIdx], yloc[capIdx], ylic[capIdx]]
                yCap = np.array(yCap) + yOffset[spiralIdx]
                filledPolygonToPcb(file, axes, xCap, yCap, layer='F.Cu')
                
            # Coiled buses
            xBusTemp = xBus[spiralIdx]
            yBusTemp = yBus[spiralIdx]
            for capIdx, (x1, x2, y1, y2) in enumerate(zip(
                                            xBusTemp[:-1], xBusTemp[1:],
                                            yBusTemp[:-1], yBusTemp[1:])):
                for busIdx in range(numWiresBus):
                    if busToCapTargets[spiralIdx, busIdx] > capIdx:
                        segmentToPcb(file=file, axes=axes,
                          x1=x1[busIdx] + xOffset[spiralIdx],
                          y1=y1[busIdx] + yOffset[spiralIdx],
                          x2=x2[busIdx] + xOffset[spiralIdx],
                          y2=y2[busIdx] + yOffset[spiralIdx],
                          layer='F.Cu', width=0.2, net=0)

        # straight caps
        capCols = 61
        xStart = 15.6
        yStart = -21 + 35
        yEnd = yStart + 7.3
        y1Top = yStart + 0.5
        y1Bot = y1Top + 2.0
        y2Top = y1Bot + 0.5
        y2Bot = y2Top + 2.0
        xEnd = xStart + capCols * 2.5
        lineToPcb(file, axes, xStart, yStart, xStart, yEnd, layer='Edge.Cuts', width=0.1)
        lineToPcb(file, axes, xEnd, yStart, xEnd, yEnd, layer='Edge.Cuts', width=0.1)
        xPrev = xStart
        for capIdx in range(capCols):
            xNext = xPrev + 2.5
            lineToPcb(file, axes, xPrev, yStart, xNext, yStart, layer='Edge.Cuts', width=0.1)
            lineToPcb(file, axes, xPrev, yEnd, xNext, yEnd, layer='Edge.Cuts', width=0.1)
            x1 = xPrev + 0.3
            x2 = xNext - 0.3
            y1 = y1Top + (capIdx -1) % 2
            y2 = y1Bot + (capIdx -1) % 2
            xCap = [x1, x1, x2, x2]
            yCap = [y1, y2, y2, y1]
            filledPolygonToPcb(file, axes, xCap, yCap, layer='F.Cu')
            y1 = y2Top + (capIdx -1) % 2
            y2 = y2Bot + (capIdx -1) % 2
            xCap = [x1, x1, x2, x2]
            yCap = [y1, y2, y2, y1]
            filledPolygonToPcb(file, axes, xCap, yCap, layer='F.Cu')
            xPrev = xNext
            
        # connectors for straight caps
        connectorsX = 20.3 + np.arange(5) * 36.7
        connectorsY = np.array([34, 40, 15, 20, 20]) -8.3 + 35
        for idx, (x, y) in enumerate(zip(connectorsX, connectorsY)):
            writeConnector(file, axes, 1, x, y, idx + 7)
            # Buses for connectors for straight caps
            busX = x - 3
            for busIdx in range(6):
                segmentToPcb(file=file, axes=axes,
                          x1=busX,
                          y1=yEnd,
                          x2=busX,
                          y2=y,
                          layer='F.Cu', width=0.2, net=0)
                busX += 0.5
            # Edge cut along bus sides
            lineToPcb(file=file, axes=axes,
                      x1= x - 3.5,
                      y1=yEnd,
                      x2=x - 3.5,
                      y2=y,
                      layer='Edge.Cuts', width=0.1)
            lineToPcb(file=file, axes=axes,
                      x1=busX,
                      y1=yEnd,
                      x2=busX,
                      y2=y,
                      layer='Edge.Cuts', width=0.1)

        #don't forget the final close bracket
        file.write(')\n')

