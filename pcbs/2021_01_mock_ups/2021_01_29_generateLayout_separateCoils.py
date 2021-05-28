# -*- coding: utf-8 -*-
"""
2021_01_28

@author: sim

Now we put the base plane parallel with the hemisphere halfway level but 
above it. We choose a fixed angular fan out, which is dictated by basic
tesselation constraints - I don't yet know what that angle is -
for now I'm assuming 60 degrees.

"""

#%%
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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

# all measurements in either mm or deg
# A segment describes 1 deg around 1 turn of the spiral

# targets
diameterOfSphere = 22
pitchBetweenTurns = 0.6 # distance from edge to edge along circumference
angleOfSpread = 50 #
sensorPitch = 1

# modelling directives
numElements = 5
direction = [1] * 90
xOffset = [0, 20, 40, 60, 80]
yOffset = [0, -25, -50 , -75, -100]
xMirror = [1, 1, 1, 1, 1]
xOffsetCircle = 40
yOffsetCircle = -55

# constraints
minWidth = 4
minRadiusAtBase = 1.8 # could be as low as 1.8
minPitchBetweenTouchingLayers = 0.15 # thickness of pcb plus adhesive

# calculable from the above
radiusOfSphere = diameterOfSphere / 2
halfAngleOfSpread = angleOfSpread / 2
arcLength = angleOfSpread / 180 * np.pi * radiusOfSphere
halfArcLength = arcLength / 2
     # circumference from lowest turn up to top of sphere
numTurns = halfArcLength / pitchBetweenTurns
elevationPerTurn = halfAngleOfSpread / numTurns
elevationPerSegment = elevationPerTurn / 360

# resolve constraints
maxRadiusAtBase = minRadiusAtBase + minPitchBetweenTouchingLayers * numTurns
distFromCentreToBaseAtMaxRadius = maxRadiusAtBase / sin(halfAngleOfSpread)
minWidthFromRadiusConstraint = radiusOfSphere - distFromCentreToBaseAtMaxRadius
# maxRadiusAtBaseFromWidthConstraint = 
minWidth = minWidthFromRadiusConstraint
# Let's calculate onwards from the point of view of minWidth
distFromCentreToBaseAtMaxRadiusActual = radiusOfSphere - minWidth
heightAtBase = cos(halfAngleOfSpread) * distFromCentreToBaseAtMaxRadiusActual

startElevation = 90 - halfAngleOfSpread
planeRotation = [0]
elevationFromCentre = [startElevation]
innerRadius = [maxRadiusAtBase]
outerRadius = [cos(elevationFromCentre[-1]) * radiusOfSphere]
height = [sin(elevationFromCentre[-1]) * radiusOfSphere]
widthAtBase = [outerRadius[-1] - innerRadius[-1]]
elevationfromBase = [elevationFromCentre[-1]]
width = [minWidth]

xInner2d = [0]
yInner2d = [0]
xOuter2d = [width[-1] * cos(direction[-1] - 90)]
yOuter2d = [width[-1] * sin(direction[-1] - 90)]

xInner3d = [innerRadius[-1]]
yInner3d = [0]
#zInner3d = # will be all heightAtBase
xOuter3d = [innerRadius[-1] + widthAtBase[-1]]
yOuter3d = [0]
zOuter3d = [height[-1]]

segIdx = 0
# We use the direction when we calculate the step from the previous segment
# to the next.
# Therefore we initialise it halfway through that step
cumDistOuter = [0]
while outerRadius[-1] > pitchBetweenTurns / 2:
    segIdx += 1
    planeRotation.append(planeRotation[-1] + 1)
    elevationFromCentre.append(elevationFromCentre[-1] + elevationPerTurn / 360)
    innerRadius.append(innerRadius[-1] - minPitchBetweenTouchingLayers / 360)    
    outerRadius.append(cos(elevationFromCentre[-1]) * radiusOfSphere)
    height.append(sin(elevationFromCentre[-1]) * radiusOfSphere)
    widthAtBase.append(outerRadius[-1] - innerRadius[-1])
    elevationfromBase.append(arctan((height[-1] - heightAtBase)
                                    / np.abs(widthAtBase[-1])))
    width.append((height[-1] - heightAtBase) / sin(elevationfromBase[-1]))
    
    # how long are the inner and outer edges of this segment    
    distanceInner = innerRadius[-1] * np.pi / 180
    distanceOuter = outerRadius[-1] * np.pi / 180
    # distanceOuter is a slight underestimate, because it also rose slightly
    # away from the plane, twisting the segment - we'll ignore this for now
    cumDistOuter += distanceOuter

    xInner2d.append(xInner2d[-1] + distanceInner * cos(direction[-1]))
    yInner2d.append(yInner2d[-1] + distanceInner * sin(direction[-1]))
    # We plot outer wrt inner using the width
    xOuter2d.append(xInner2d[-1] + width[-1] * cos(direction[-1] - 90))
    yOuter2d.append(yInner2d[-1] + width[-1] * sin(direction[-1] - 90))

    # update direction
    direction.append(direction[-1] + 
                     arctan((distanceOuter - distanceInner) / width[-1]))
    
    xInner3d.append(innerRadius[-1] * cos(planeRotation[-1]))
    yInner3d.append(innerRadius[-1] * sin(planeRotation[-1]))
    #zInner3d will be all heightAtBase
    xOuter3d.append(outerRadius[-1] * cos(planeRotation[-1]))
    yOuter3d.append(outerRadius[-1] * sin(planeRotation[-1]))
    zOuter3d.append(height[-1])

# Plot 2d    

plt.close('all')
fig, axes = plt.subplots(1, 1)

for idx in range(numElements):
    axes.plot(xMirror[idx] * [x + xOffset[idx] for x in xInner2d], 
              [y + yOffset[idx] for y in yInner2d], 'k')
    axes.plot(xMirror[idx] * [x + xOffset[idx] for x in xOuter2d], 
              [y + yOffset[idx] for y in yOuter2d], 'k')

    numSegActual = len(width)
    # Half circles
    lineIds = (list(range(0, numSegActual, int(180))) + 
               [numSegActual - 1])
    for lineIdx in lineIds:
        axes.plot(
            [xOuter2d[lineIdx] * xMirror[idx] + xOffset[idx], 
             xInner2d[lineIdx] * xMirror[idx] + xOffset[idx]],
            [yOuter2d[lineIdx] + yOffset[idx], 
             yInner2d[lineIdx] + yOffset[idx]],
            'k')
    # Quarter circles
    lineIds = (list(range(90, numSegActual, int(180))) + 
               [numSegActual - 1])
    for lineIdx in lineIds:
        axes.plot(
            [xOuter2d[lineIdx] * xMirror[idx] + xOffset[idx], 
             xInner2d[lineIdx] * xMirror[idx] + xOffset[idx]],
            [yOuter2d[lineIdx] + yOffset[idx], 
             yInner2d[lineIdx] + yOffset[idx]],
            'k:')


# Show the wafer circle

r = np.arange(0, 360)
x = 100 * sin(r) + xOffsetCircle
y = 100 * cos(r) + yOffsetCircle
axes.plot(x, y, 'k')

axes.set_aspect('equal')

# 3d plot

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.plot(xInner3d,
        yInner3d, 
        heightAtBase, 'k')


ax.plot(xOuter3d, 
        yOuter3d, 
        zOuter3d, 'k')

  
# Create cubic bounding box to simulate equal aspect ratio
Xb = radiusOfSphere*np.mgrid[-1:2:2,-1:2:2,-1:2:2][0].flatten() #+ radiusOfSphere
Yb = radiusOfSphere*np.mgrid[-1:2:2,-1:2:2,-1:2:2][1].flatten() #+ radiusOfSphere
Zb = radiusOfSphere*np.mgrid[-1:2:2,-1:2:2,-1:2:2][2].flatten() + radiusOfSphere/2
# Comment or uncomment following both lines to test the fake bounding box:
for xb, yb, zb in zip(Xb, Yb, Zb):
   ax.plot([xb], [yb], [zb], 'w')

plt.grid()
plt.show()
   
print('Total edge length: ', np.sum(cumDistOuter) * 5)





