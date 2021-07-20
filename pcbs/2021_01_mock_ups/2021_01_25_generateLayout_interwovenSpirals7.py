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

#%%
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# all measurements in either mm or deg

# targets
numSpirals = 7
diameterOfSphere = 20
pitchBetweenTurns = 0.7 # distance from edge to edge along circumference
startElevation = 10 # up from horizontal, out from centre
sensorPitch = 1

# modelling directives
spiralEndIds = np.array([450, 540, 630, 720, 810, 900, 1440, 1200])
spiralEndIdsActual = np.ones((numSpirals), dtype=np.int) * 10000
direction = np.array([1.4, 1.5, 1.7, 2, 2.2, 2.5, 3.1, 2])[np.newaxis, :] * 90
xOffset = np.array([34, 15, 2, -5, 5, 28, 78, 0])
yOffset = np.array([-6, -25, -50, -80, -112, -142, -160, -350])

# Alternative compact layout
direction = np.array([1.4, 1.5, 1.7, 2, 0.4, 3.7, 1.1])[np.newaxis, :] * 90
xOffset = np.array([0, -20, 15, -25, 10, 20, 40])
yOffset = np.array([0, -16, -25, -45, 5, -5, -65])
showCircle = False

xMirror = np.array([1, 1, 1, 1, 1, 1, 1, 1])
anglePerSegment = 1
xOffsetCircle = 80
yOffsetCircle = -80

# In case less than 8 spirals
spiralEndIds = spiralEndIds[:numSpirals]
direction = direction[:, :numSpirals]
xOffset = xOffset[:numSpirals]
yOffset = yOffset[:numSpirals]
xMirror = xMirror[:numSpirals]

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

segIdx = 0
# We use the direction when we calculate the step from the previous segment
# to the next.
# Therefore we initialise it halfway through that step
running = np.ones((1, numSpirals), dtype=np.bool)
numRunning = numSpirals
cumDistOuter = np.zeros((numSpirals))
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
    cumDistOuter = cumDistOuter + distanceOuter * running[-1, :]

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

# Plot 2d    

plt.close('all')
fig, axes = plt.subplots(1, 1)

for idx in range(numSpirals):
    axes.text(xOffset[idx], yOffset[idx], str(idx))
    axes.plot(xMirror[idx] * xInner2d[running[:, idx], idx] + xOffset[idx], 
             yInner2d[running[:, idx], idx] + yOffset[idx], 'k')
    axes.plot(xMirror[idx] * xOuter2d[running[:, idx], idx] + xOffset[idx], 
             yOuter2d[running[:, idx], idx] + yOffset[idx], 'k')
    # Half circles
    lineIds = (list(range(0, spiralEndIdsActual[idx], int(segmentsPerTurn / 2))) + 
               [spiralEndIdsActual[idx] - 1])
    for lineIdx in lineIds:
        axes.plot(
            [xOuter2d[lineIdx, idx] * xMirror[idx] + xOffset[idx], 
             xInner2d[lineIdx, idx] * xMirror[idx] + xOffset[idx]],
            [yOuter2d[lineIdx, idx] + yOffset[idx], 
             yInner2d[lineIdx, idx] + yOffset[idx]],
            'k')
    # Quarter circles
    lineIds = (list(range(90, spiralEndIdsActual[idx], int(segmentsPerTurn / 2))) + 
               [spiralEndIdsActual[idx] - 1])
    for lineIdx in lineIds:
        axes.plot(
            [xOuter2d[lineIdx, idx] * xMirror[idx] + xOffset[idx], 
             xInner2d[lineIdx, idx] * xMirror[idx] + xOffset[idx]],
            [yOuter2d[lineIdx, idx] + yOffset[idx], 
             yInner2d[lineIdx, idx] + yOffset[idx]],
            'k:')


# Show the wafer circle

if showCircle:
    r = np.arange(0, 360)
    x = 100 * sin(r) + xOffsetCircle
    y = 100 * cos(r) + yOffsetCircle
    axes.plot(x, y, 'k')

axes.set_aspect('equal')

# 3d plot

#%%
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for idx in range(numSpirals):
    ax.plot(xInner3d[:spiralEndIdsActual[idx], idx], 
            yInner3d[:spiralEndIdsActual[idx], idx], 
            np.zeros((spiralEndIdsActual[idx])), 'k')
    ax.plot(xOuter3d[:spiralEndIdsActual[idx], idx], 
            yOuter3d[:spiralEndIdsActual[idx], idx], 
            zOuter3d[:spiralEndIdsActual[idx], idx], 'k')

# Create cubic bounding box to simulate equal aspect ratio
Xb = radiusOfSphere*np.mgrid[-1:2:2,-1:2:2,-1:2:2][0].flatten() #+ radiusOfSphere
Yb = radiusOfSphere*np.mgrid[-1:2:2,-1:2:2,-1:2:2][1].flatten() #+ radiusOfSphere
Zb = radiusOfSphere*np.mgrid[-1:2:2,-1:2:2,-1:2:2][2].flatten() + radiusOfSphere/2
# Comment or uncomment following both lines to test the fake bounding box:
for xb, yb, zb in zip(Xb, Yb, Zb):
   ax.plot([xb], [yb], [zb], 'w')

ax.set_aspect('equal')

plt.grid()
plt.show()
   
print('Total edge length: ', np.sum(cumDistOuter))




