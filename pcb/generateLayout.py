# -*- coding: utf-8 -*-
"""
2021_01_21

@author: sim

a number of interwoven spirals

it's assumed that the outer edge is at the surface of the sphere
it's assumed that the inner edge is touching the base of the hemisphere

each segment has: 

    planeRotation = an angle round from 0,
    elevationFromCentre = angle up from horizontal, from centre of sphere
    innerRadius = distance of inner edge out from centre of sphere

    ... calculable from these for each segment:

    elevationfromBase = angle of elevation
    width = from inner to outer edges
    height = from base at outer edge
    outerRadius = radius of outer edge projected down onto base plane
    widthAtBase = the width projected down onto the base plane
    
    ... diffs from previous segment
    
    innerStep = 2D length of segment
    outerStep = 3D length of segment
    printRotation = amount to rotate segment on 2D design

    ... 
    
    x/yInner/Outer2d
    x/y/z/Inner/Outer3d

"""

import numpy as np

# all measurements in either mm or deg

# targets
numSpirals = 7
diameterOfSphere = 20
pitchBetweenTurns = 0.7 # distance from edge to edge along circumference
startElevation = 10 # up from horizontal, out from centre

capPitch = 2.4
capWidth = 2.0
capSpacingToCut = 0.2

lenBus = np.array([25, 22, 45, 50, 45, 40, 30])
numWiresBus = 6
pitchBus = 0.5
widthBus = (numWiresBus + 1) * pitchBus # The specification for the zif connector

# modelling directives
spiralEndIds = np.array([450, 540, 630, 720, 810, 900, 1440])
spiralEndIdsActual = np.ones((numSpirals), dtype=np.int64) * 10000

orientation = np.array([1, -1, 1, -1, 1, -1, 1])[np.newaxis, :]
extensionAngleMod = np.array([70, 70, 75, 85, 90, 100, 110])
direction = orientation * 90 + 90 + extensionAngleMod

xOffset = np.array([6, 57, 114, 141, 67, 103, 0])
yOffset = np.array([20, 5, -10, 40, -10, 40, 5])
xOffset = xOffset  + 22 # for the pcb
yOffset = yOffset  + 75 # for the pcb

# each value is the index of the cap that the vbus targets
# one row per spiral; one col per bus wire
busToCapTargets = np.array([
    [26, 25, 24, 2, 1, 0],
    [25, 24, 23, 2, 1, 0],
    [24, 23, 22, 2, 1, 0],
    [23, 22, 21, 2, 1, 0],
    [22, 21, 20, 2, 1, 0],
    [21, 20, 19, 2, 1, 0],
    [19, 18, 17, 2, 1, 0],
    ])    

anglePerSegment = 1
# spiralEndIds assumed 1 deg per segment, therefore normalisation
spiralEndIds = (spiralEndIds / anglePerSegment).astype(int)

# In case less than 8 spirals
spiralEndIds = spiralEndIds[:numSpirals]
direction = direction[:, :numSpirals]
xOffset = xOffset[:numSpirals]
yOffset = yOffset[:numSpirals]

# constraints
minRadiusAtBase = 2.5 # could be as low as 1.8
minPitchBetweenTouchingLayers = 0.15 # thickness of pcb plus adhesive
relaxationOuter = 0.2 # factor by which outer spiral should twist outwards to restore the ideal space filling
relaxationInner = 0.04 # factor by which outer spiral should twist outwards to restore the ideal space filling

# calculable from the above
radiusOfSphere = diameterOfSphere / 2
demiCircumference = diameterOfSphere * np.pi / 4 * (90-startElevation) / 90
     # circumference from lowest turn up to top of sphere
numTurns = demiCircumference / pitchBetweenTurns
elevationPerTurn = (90-startElevation) / numTurns
maxRadiusAtBase = minRadiusAtBase + minPitchBetweenTouchingLayers * numTurns

turnsPerSegment = anglePerSegment / 360
segmentsPerTurn = int(360 / anglePerSegment) # we use this for indexing


def sin(x):
    return np.sin(x / 180 * np.pi)
def cos(x):
    return np.cos(x / 180 * np.pi)
def tan(x):
    return np.tan(x / 180 * np.pi)

def arcsin(x):
    return np.arcsin(x) * 180 / np.pi
def arccos(x):
    return np.arccos(x) * 180 / np.pi
def arctan(x):
    return np.arctan(x) * 180 / np.pi


planeRotation = np.zeros((1, 1)) # the same for all spirals
elevationFromCentre = np.array(
    [startElevation + elevationPerTurn * n 
     for n in range(numSpirals)])[np.newaxis, :]
innerRadius = np.array(
    [maxRadiusAtBase - minPitchBetweenTouchingLayers * n
     for n in range(numSpirals)])[np.newaxis, :]

outerRadius = cos(elevationFromCentre) * radiusOfSphere
height = sin(elevationFromCentre) * radiusOfSphere
widthAtBase = outerRadius - innerRadius
elevationfromBase = arctan(height / widthAtBase)
width = height / sin(elevationfromBase)

xInner2d = np.zeros((1, numSpirals))
yInner2d = np.zeros((1, numSpirals))
xOuter2d = width * cos(direction - 90)
yOuter2d = width * sin(direction - 90)

xInner3d = innerRadius
yInner3d = np.zeros((1, numSpirals))
#zInner3d = np.array([0, 0, 0, 0])[np.newaxis, :] # will be all zeros
xOuter3d = innerRadius + widthAtBase
yOuter3d = np.zeros((1, numSpirals))
zOuter3d = height

# Extension
xInnerExt = lenBus * sin(direction - extensionAngleMod)
yInnerExt = -lenBus * cos(direction - extensionAngleMod)
xOuterRet = widthBus * cos(direction - 90)
yOuterRet = widthBus * sin(direction - 90)
xOuterExt = xInnerExt + widthBus * cos(direction - extensionAngleMod)
yOuterExt = (yInnerExt + widthBus * sin(direction - extensionAngleMod))

# Bus
busSpacings = np.arange(pitchBus, pitchBus * (numWiresBus + 1), pitchBus)[:, np.newaxis]
xInnerBus = busSpacings * cos(direction - 90)
yInnerBus = busSpacings * sin(direction - 90)
xOuterBus = xInnerExt + busSpacings * cos(direction - extensionAngleMod)
yOuterBus = (yInnerExt + busSpacings * sin(direction - extensionAngleMod))

#Labels


segIdx = 0
# We use the direction when we calculate the step from the previous segment
# to the next.
# Therefore we initialise it halfway through that step
running = np.ones((1, numSpirals), dtype=bool)
numRunning = numSpirals
cumDistOuter = np.zeros((1, numSpirals))

while np.any(running[-1, :]):
    segIdx += 1
    planeRotation = np.append(planeRotation, planeRotation[-1] + anglePerSegment)
    if planeRotation[-1] < 360:
        elevationFromCentre = np.append(elevationFromCentre,
            elevationFromCentre[-1, np.newaxis, :] + 
            elevationPerTurn * turnsPerSegment * numRunning,
            axis=0)
        innerRadius = np.append(innerRadius,
            innerRadius[-1, np.newaxis, :] - 
            minPitchBetweenTouchingLayers * turnsPerSegment * numRunning,
            axis=0)    
    else:
        # After making one complete rotation, we follow existing elevations
        # find previous max elevationFromCentre
        maxElevationFromCentre = np.max(elevationFromCentre[1-segmentsPerTurn])
        newElevationsFromCentre = []
        newInnerRadii = []
        minInnerRadius = np.min(innerRadius[1-segmentsPerTurn])
        for spiralIdx in range(numSpirals):
            if running[-1, spiralIdx]:
                newElevationFromCentre = max(
                    maxElevationFromCentre + elevationPerTurn,
                    elevationFromCentre[-1, spiralIdx] - 
                    relaxationOuter * anglePerSegment *
                    outerRadius[-1, spiralIdx] /
                    radiusOfSphere) # wind out by some angle - base the ngle on outerRadius - if further in, wind out more slowly.
                maxElevationFromCentre = newElevationFromCentre
                newElevationsFromCentre.append(newElevationFromCentre)
                newInnerRadius = min(
                    minInnerRadius - minPitchBetweenTouchingLayers,
                    innerRadius[-1, spiralIdx] + 
                    relaxationInner * anglePerSegment *
                    minPitchBetweenTouchingLayers * 
                    innerRadius[-1, spiralIdx] / maxRadiusAtBase) # wind out by some angle - base the ngle on outerRadius - if further in, wind out more slowly.
                minInnerRadius = newInnerRadius
                newInnerRadii.append(newInnerRadius)
            else:
                newElevationsFromCentre.append(0.00001) # Don't include spirals not running                                           
                newInnerRadii.append(maxRadiusAtBase) # Don't include spirals not running                                           
        elevationFromCentre = np.append(elevationFromCentre,
            (np.array(newElevationsFromCentre))[np.newaxis, :],
            axis=0)
        innerRadius = np.append(innerRadius,
            (np.array(newInnerRadii))[np.newaxis, :],
            axis=0)
    outerRadius = np.append(outerRadius,
        cos(elevationFromCentre[-1, np.newaxis, :]) * radiusOfSphere,
        axis=0)
    height = np.append(height,
        sin(elevationFromCentre[-1, np.newaxis, :]) * radiusOfSphere,
        axis=0)
    widthAtBase = np.append(widthAtBase,
        outerRadius[-1, np.newaxis, :] - innerRadius[-1, np.newaxis, :],
        axis=0)
    #widthAtBaseIsPositive = widthAtBase[-1, np.newaxis, :] >= 0
    elevationfromBase = np.append(elevationfromBase,
        arctan(height[-1, np.newaxis, :] / np.abs(widthAtBase[-1, np.newaxis, :])),        
        axis=0)
    width = np.append(width,
        height[-1, np.newaxis, :] / sin(elevationfromBase[-1, np.newaxis, :]),
        axis=0)
    
    # how long are the inner and outer edges of this segment
    distanceInner = innerRadius[-1, :] * np.pi * 2 * turnsPerSegment
    distanceOuter = outerRadius[-1, :] * np.pi * 2 * turnsPerSegment
    # distanceOuter is a slight underestimate, because it also rose slightly
    # away from the plane, twisting the segment - we'll ignore this for now
    cumDistOuter = np.append(cumDistOuter,
        cumDistOuter[-1, np.newaxis, :] + distanceOuter * running[-1, :],
    axis=0)

    xInner2d = np.append(xInner2d, 
        xInner2d[-1, np.newaxis, :] + 
        distanceInner * cos(direction[-1, np.newaxis, :]),
        axis=0)
    yInner2d = np.append(yInner2d, 
        yInner2d[-1, np.newaxis, :] + 
        distanceInner * sin(direction[-1, np.newaxis, :]),
        axis=0)
    # We plot outer wrt inner using the width
    xOuter2d = np.append(xOuter2d, 
        xInner2d[-1, np.newaxis, :] + 
        width[-1, np.newaxis, :] * cos(direction[-1, np.newaxis, :] - 90),
        axis=0)
    yOuter2d = np.append(yOuter2d, 
        yInner2d[-1, np.newaxis, :] + 
        width[-1, np.newaxis, :] * sin(direction[-1, np.newaxis, :] - 90),
        axis=0)

    # update direction
    direction = np.append(direction,
        direction[-1, np.newaxis, :] + 
        arctan((distanceOuter - distanceInner) / width[-1, np.newaxis, :]),
        axis=0)
    
    # Are segments finished?
    running = np.append(running,
        np.logical_and(
            outerRadius[-1, :] > pitchBetweenTurns / 2,
            np.logical_and(segIdx < spiralEndIds,
                           running[-1, :]))[np.newaxis, :],
        axis=0)
    numRunning = np.sum(running[-1, :])
    for idx in range(numSpirals):
        if not running[-1, idx]:
            if spiralEndIdsActual[idx] > segIdx:
                spiralEndIdsActual[idx] = segIdx
    
    xInner3d = np.append(xInner3d,
        innerRadius[-1, np.newaxis, :] * cos(planeRotation[-1, np.newaxis]),
        axis=0)
    yInner3d = np.append(yInner3d,
        innerRadius[-1, np.newaxis, :] * sin(planeRotation[-1, np.newaxis]),
        axis=0)
    #zInner3d = np.array([0, 0, 0, 0])[np.newaxis, :] # will be all zeros
    xOuter3d = np.append(xOuter3d,
        (innerRadius[-1, np.newaxis, :] + widthAtBase[-1, np.newaxis, :])
         * cos(planeRotation[-1, np.newaxis]),
        axis=0)
    yOuter3d = np.append(yOuter3d,
        (innerRadius[-1, np.newaxis, :] + widthAtBase[-1, np.newaxis, :])
         * sin(planeRotation[-1, np.newaxis]),
        axis=0)
    zOuter3d = np.append(zOuter3d, height[-1, np.newaxis, :], axis=0)

# calculate caps

#capPitch = 2.4
#capWidth = 2.0
#capSpacingToCut = 0.2
edgeCuts = []
caps = []
xBus = []
yBus = []

busSteps = np.array(list(range(1, numWiresBus + 1)))[np.newaxis, :] * pitchBus

totalCaps = 0
for spiralIdx in range(numSpirals):
    capBoundaryIds = np.searchsorted(cumDistOuter[:, spiralIdx],
        np.arange(capPitch, cumDistOuter[-1, spiralIdx], capPitch))
    capFirstEdgeIds = np.searchsorted(cumDistOuter[:, spiralIdx],
        np.arange(capSpacingToCut, cumDistOuter[-1, spiralIdx], capPitch))
    capLastEdgeIds = np.searchsorted(cumDistOuter[:, spiralIdx],
        np.arange(capPitch - capSpacingToCut, cumDistOuter[-1, spiralIdx], capPitch))

    numCaps = len(capBoundaryIds)
    capFirstEdgeIds = capFirstEdgeIds[:numCaps]
    capLastEdgeIds = capLastEdgeIds[:numCaps]

    # Boundary cuts
    xOuterBoundary = xOuter2d[capBoundaryIds, spiralIdx]
    xInnerBoundary = xInner2d[capBoundaryIds, spiralIdx]
    yOuterBoundary = yOuter2d[capBoundaryIds, spiralIdx]
    yInnerBoundary = yInner2d[capBoundaryIds, spiralIdx]
    widthBoundary = width[capBoundaryIds, spiralIdx]
    xInnerEdgeCut = (xOuterBoundary + 
                      (xInnerBoundary-xOuterBoundary) / widthBoundary * capPitch)
    yInnerEdgeCut = (yOuterBoundary + 
                      (yInnerBoundary-yOuterBoundary) / widthBoundary * capPitch)
    edgeCuts.append((xInnerEdgeCut, xOuterBoundary, yInnerEdgeCut, yOuterBoundary))

    # cap coords: f=first, l=last; i=inner, o=outer, c=cap
    xfo = xOuter2d[capFirstEdgeIds, spiralIdx]
    xfi = xInner2d[capFirstEdgeIds, spiralIdx]
    yfo = yOuter2d[capFirstEdgeIds, spiralIdx]
    yfi = yInner2d[capFirstEdgeIds, spiralIdx]
    xlo = xOuter2d[capLastEdgeIds, spiralIdx]
    xli = xInner2d[capLastEdgeIds, spiralIdx]
    ylo = yOuter2d[capLastEdgeIds, spiralIdx]
    yli = yInner2d[capLastEdgeIds, spiralIdx]
    xfic = (xfo + (xfi-xfo) / widthBoundary * (capWidth + capSpacingToCut))
    xlic = (xlo + (xli-xlo) / widthBoundary * (capWidth + capSpacingToCut))
    yfic = (yfo + (yfi-yfo) / widthBoundary * (capWidth + capSpacingToCut))
    ylic = (ylo + (yli-ylo) / widthBoundary * (capWidth + capSpacingToCut))

    xfoc = (xfo + (xfi-xfo) / widthBoundary * capSpacingToCut)
    xloc = (xlo + (xli-xlo) / widthBoundary * capSpacingToCut)
    yfoc = (yfo + (yfi-yfo) / widthBoundary * capSpacingToCut)
    yloc = (ylo + (yli-ylo) / widthBoundary * capSpacingToCut)

    caps.append((xfic, yfic, xfoc, yfoc, xloc, yloc, xlic, ylic))
    totalCaps += numCaps

    # Bus
    # Expand the dimension of these arrays to then do outer product
    capBoundaryIds = np.insert(capBoundaryIds, 0, 0)
    xOuterBoundary = xOuter2d[capBoundaryIds, spiralIdx, np.newaxis]
    xInnerBoundary = xInner2d[capBoundaryIds, spiralIdx, np.newaxis]
    yOuterBoundary = yOuter2d[capBoundaryIds, spiralIdx, np.newaxis]
    yInnerBoundary = yInner2d[capBoundaryIds, spiralIdx, np.newaxis]
    widthBoundary = width[capBoundaryIds, spiralIdx, np.newaxis]
    xBus.append(xInnerBoundary +
                      (xOuterBoundary-xInnerBoundary) / widthBoundary * busSteps)
    yBus.append(yInnerBoundary +
                      (yOuterBoundary-yInnerBoundary) / widthBoundary * busSteps)

# Export to pcb file
from generateLayoutPcb import generateLayoutPcb


generateLayoutPcb(numSpirals, running,
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
                  xOuterBus, yOuterBus)


# 3d plot

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for idx in range(numSpirals):
    ax.plot(xInner3d[:spiralEndIdsActual[idx], idx],
            yInner3d[:spiralEndIdsActual[idx], idx],
            np.zeros((spiralEndIdsActual[idx])), 'k')
    ax.plot(xOuter3d[:spiralEndIdsActual[idx], idx],
            yOuter3d[:spiralEndIdsActual[idx], idx],
            zOuter3d[:spiralEndIdsActual[idx], idx], 'k')
    # initial edges
    ax.plot([xInner3d[0, idx],
             xOuter3d[0, idx]],
            [yInner3d[0, idx],
             yOuter3d[0, idx]],
            [0,
             zOuter3d[0, idx]], 'k')
    # final edges
    ax.plot([xInner3d[spiralEndIdsActual[idx] - 1, idx],
             xOuter3d[spiralEndIdsActual[idx] - 1, idx]],
            [yInner3d[spiralEndIdsActual[idx] - 1, idx],
             yOuter3d[spiralEndIdsActual[idx] - 1, idx]],
            [0,
             zOuter3d[spiralEndIdsActual[idx] - 1, idx]], 'k')


# Create cubic bounding box to simulate equal aspect ratio
Xb = radiusOfSphere*np.mgrid[-1:2:2,-1:2:2,-1:2:2][0].flatten() #+ radiusOfSphere
Yb = radiusOfSphere*np.mgrid[-1:2:2,-1:2:2,-1:2:2][1].flatten() #+ radiusOfSphere
Zb = radiusOfSphere*np.mgrid[-1:2:2,-1:2:2,-1:2:2][2].flatten() + radiusOfSphere/2
# Comment or uncomment following both lines to test the fake bounding box:
for xb, yb, zb in zip(Xb, Yb, Zb):
   ax.plot([xb], [yb], [zb], 'w')

plt.grid()
plt.show()


print('Total edge length: ', np.sum(cumDistOuter[-1, :]))




