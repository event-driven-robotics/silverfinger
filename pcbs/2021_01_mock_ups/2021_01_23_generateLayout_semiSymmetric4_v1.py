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
diameterOfSphere = 20
pitchBetweenTurns = 1 # distance from edge to edge along circumference
startElevation = 15 # up from horizontal, out from centre
sensorPitch = 1
numSpirals = 4

# modelling directives
spiralEndIds = np.array([90, 110, 278, 500])
spiralEndIdsActual = np.array([10000, 10000, 10000, 10000])
direction = np.array([25, 40, -40, 10])[np.newaxis, :] + 90
xOffset = np.array([-13, -13, -8, -8])
yOffset = np.array([0, 0, 2, 2])
anglePerSegment = 5

# constraints
minRadiusAtBase = 3 # could be as low as 1.8
minPitchBetweenTouchingLayers = 0.2 # thickness of pcb plus adhesive
deelevationPerSegment = 1 # degrees by which outer spiral should twist outwards to restore the ideal space filling

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
    [startElevation, 
     startElevation + elevationPerTurn, 
     startElevation + elevationPerTurn * 2, 
     startElevation + elevationPerTurn * 3])[np.newaxis, :]
innerRadius = np.array(
    [maxRadiusAtBase,
     maxRadiusAtBase - minPitchBetweenTouchingLayers,
     maxRadiusAtBase - minPitchBetweenTouchingLayers * 2,
     maxRadiusAtBase - minPitchBetweenTouchingLayers * 3])[np.newaxis, :]

outerRadius = cos(elevationFromCentre) * radiusOfSphere
height = sin(elevationFromCentre) * radiusOfSphere
widthAtBase = outerRadius - innerRadius
elevationfromBase = arctan(height / widthAtBase)
width = height / sin(elevationfromBase)

xInner2d = np.array([0, 0, 0, 0])[np.newaxis, :]
yInner2d = np.array([0, 0, 0, 0])[np.newaxis, :]
xOuter2d = width * cos(direction - 90)
yOuter2d = width * sin(direction - 90)

xInner3d = innerRadius
yInner3d = np.array([0, 0, 0, 0])[np.newaxis, :]
#zInner3d = np.array([0, 0, 0, 0])[np.newaxis, :] # will be all zeros
xOuter3d = innerRadius + widthAtBase
yOuter3d = np.array([0, 0, 0, 0])[np.newaxis, :]
zOuter3d = height

segIdx = 0
# We use the direction when we calculate the step from the previous segment
# to the next.
# Therefore we initialise it halfway through that step
running = np.ones((1, 4), dtype=np.bool) 
while np.any(running[-1, :]):
    segIdx += 1
    planeRotation = np.append(planeRotation, planeRotation[-1] + anglePerSegment)
    if planeRotation[-1] < 360:        
        elevationFromCentre = np.append(elevationFromCentre,
            elevationFromCentre[-1, np.newaxis, :] + 
            elevationPerTurn * turnsPerSegment * numSpirals,
            axis=0)
        innerRadius = np.append(innerRadius,
            innerRadius[-1, np.newaxis, :] - 
            minPitchBetweenTouchingLayers * turnsPerSegment * numSpirals,
            axis=0)    
    else:
        # After making one complete rotation, we follow existing elevations
        # find previous max elevationFromCentre
        maxElevationFromCentre = np.max(elevationFromCentre[1-segmentsPerTurn])
        newElevationsFromCentre = []
        newInnerRadii = []
        minInnerRadius = np.min(innerRadius[1-segmentsPerTurn])
        for spiralIdx in range(4):
            if running[-1, spiralIdx]:
                newElevationFromCentre = max(
                    maxElevationFromCentre + elevationPerTurn,
                    elevationFromCentre[-1, spiralIdx] - outerRadius[-1, spiralIdx] / radiusOfSphere) # wind out by some angle - base the ngle on outerRadius - if further in, wind out more slowly.
                maxElevationFromCentre = newElevationFromCentre
                newElevationsFromCentre.append(newElevationFromCentre)
                newInnerRadius = min(
                    minInnerRadius - minPitchBetweenTouchingLayers,
                    innerRadius[-1, spiralIdx] + 0.2 * minPitchBetweenTouchingLayers * innerRadius[-1, spiralIdx] / maxRadiusAtBase) # wind out by some angle - base the ngle on outerRadius - if further in, wind out more slowly.
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
            segIdx < spiralEndIds,
            outerRadius[-1, :] > pitchBetweenTurns / 2)[np.newaxis, :],
        axis=0)
    numSpirals = np.sum(running[-1, :])
    for idx in range(4):
        if not running[-1, idx]:
            if spiralEndIdsActual[idx] > segIdx:
                spiralEndIdsActual[idx] = segIdx + 1
    
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

#plt.close('all')
fig, axes = plt.subplots(1, 1)

for idx in range(4):
    xMirror = (idx % 2) * 2 - 1
    axes.plot(xMirror * (xInner2d[running[:, idx], idx] + xOffset[idx]), 
             yInner2d[running[:, idx], idx] + yOffset[idx], 'k')
    axes.plot(xMirror * (xOuter2d[running[:, idx], idx] + xOffset[idx]), 
             yOuter2d[running[:, idx], idx] + yOffset[idx], 'k')
    axes.plot(
        [(xOuter2d[0, idx] + xOffset[idx]) * xMirror, 
         (xInner2d[0, idx] + xOffset[idx]) * xMirror],
        [yOuter2d[0, idx] + yOffset[idx], 
         yInner2d[0, idx] + yOffset[idx]],
        'k')
    axes.plot(
        [(xOuter2d[spiralEndIdsActual[idx]-1, idx] + xOffset[idx]) * xMirror, 
         (xInner2d[spiralEndIdsActual[idx]-1, idx] + xOffset[idx]) * xMirror],
        [yOuter2d[spiralEndIdsActual[idx]-1, idx] + yOffset[idx], 
         yInner2d[spiralEndIdsActual[idx]-1, idx] + yOffset[idx]],
        'k')


# Show the wafer circle

r = np.arange(0, 360)
x = 100 * sin(r)
y = 100 * cos(r)
axes.plot(x, y, 'k')

axes.set_aspect('equal')

# 3d plot

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for idx in range(4):
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

plt.grid()
plt.show()
   
#%%


# plot piezos
for piezo in allPiezos:
    circle = plt.Circle(piezo, diameterPiezo / 2, color='g', clip_on=False)
    axes.add_artist(circle)
    
# plot caps    
for cap in allCaps:
    circle = plt.Circle(cap, diameterCap / 2, color='b', clip_on=False)
    axes.add_artist(circle)

   
# Plot cables    
for cableWidth, startCoordPair, startAngle in zip(cableWidths, startCoords, startAngles):
    plt.plot([0, startCoordPair[0]], [0, startCoordPair[1]], 'k')
    offsetX = cableWidth * np.sin(startAngle-np.pi/2)
    offsetY = cableWidth * np.cos(startAngle-np.pi/2)
    plt.plot([0, startCoordPair[0]] + offsetX, [0, startCoordPair[1]] + offsetY, 'k')
   
axes.set_aspect('equal')

from math import log10, floor
def sf3(x):
    if x and isinstance(x, (int, float, complex)) and not isinstance(x, bool):
        return round(x, -int(floor(log10(abs(x)))) + 2)
    else:
        return x
    
print('target num turns = ' + str(numTurns - 1))
print('num turns = ' + str(numTurnsActual))
print('num caps = ' + str(len(allCaps)))
print('num piezos = ' + str(len(allPiezos)))
print('num sensors = ' + str(len(allPiezos) + len(allCaps)))
print('sensors per section: ')
print([sf3(x) for x in sensorsPerSection])
print('wire pitch: ')
print([sf3(x) for x in wirePitches])
print('cable width: ')
print([sf3(x) for x in cableWidths])


