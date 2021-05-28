# -*- coding: utf-8 -*-
"""
Created on Thu Dec 31 16:58:23 2020

@author: sim
"""

#%%
import numpy as np
import matplotlib.pyplot as plt

'''
mapping by each turn of the spiral.
For each turn we have:
    height
    distance of base from centre
    angular position of top out from centre
    diameters for top and centre
    from these we calculate the curvature
'''


#%%

a = 1
b = 1
t = np.arange(2000)
x = (a + b*t) * cos(t)
y = (a + b*t) * sin(t)

fig, axes = plt.subplots(1, 1)

plt.plot(x, y)
axes.set_aspect('equal')

#%% First calculate reference values for each radius

desiredDiameter = 22
desiredTurnPitch = 1
numTurns = int(desiredDiameter * np.pi / 4 / desiredTurnPitch)
minRadiusAtBase = 3.6
minPitchBetweenTouchingLayers = 0.15
spacingPiezo = 4
diameterPiezo = 1.5
depthPiezo = diameterPiezo / 2
spacingCap = 6
diameterCap = 2
depthCap = diameterCap / 2 + diameterPiezo
minWirePitch = 0.2


#%%

sectionEndIds = [900]
sectionEndIds.append(sectionEndIds[-1] + 160)
sectionEndIds.append(sectionEndIds[-1] + 125)
sectionEndIds.append(sectionEndIds[-1] + 110)
sectionEndIds.append(sectionEndIds[-1] + 95)
sectionEndIds.append(sectionEndIds[-1] + 85)
sectionEndIds.append(sectionEndIds[-1] + 78)
sectionEndIds.append(sectionEndIds[-1] + 65)

firstSectionAngleOffset = - np.pi
sectionDist = 40

idx = np.arange(numTurns)
radiusAtBase = minRadiusAtBase + idx * minPitchBetweenTouchingLayers
xBase = radiusAtBase
zBase = np.zeros_like(radiusAtBase)
angleOfTopFromCentre = (idx + 0.5) / (numTurns - 0.5) * np.pi / 2 # rad
angleOfTopFromCentreDeg = angleOfTopFromCentre / np.pi * 180
xTop = desiredDiameter / 2 * np.sin(angleOfTopFromCentre)
zTop = desiredDiameter / 2 * np.cos(angleOfTopFromCentre)
angleOfTopFromBase = np.arctan((xTop-xBase) / (zTop - zBase))
angleOfTopFromBaseDeg = angleOfTopFromBase / np.pi * 180
distBaseToTop = np.sqrt((xTop-xBase) **2 + (zTop - zBase)**2)
circumferenceAtBase = radiusAtBase * np.pi * 2
circumferenceAtTop = xTop * np.pi * 2
circumferenceAtPiezo = (
    circumferenceAtTop / distBaseToTop * (distBaseToTop - depthPiezo) +
    circumferenceAtBase / distBaseToTop * depthPiezo
    )
circumferenceAtCap = (
    circumferenceAtTop / distBaseToTop * (distBaseToTop - depthCap) +
    circumferenceAtBase / distBaseToTop * depthCap
    )
depthLeftForWiring = distBaseToTop - depthCap - diameterCap / 2

# Then interpolate linearly for each radius

def expandArray(array, numElements):
    innerArrays = []
    for prv, nxt in zip(array[:-1], array[1:]):
        innerArray = np.arange(prv, nxt - 0.00000001, (nxt - prv) / numElements)
        innerArray = innerArray[:numElements]
        innerArrays.append(innerArray)
    expandedArray = np.concatenate(innerArrays)
    return expandedArray

numSectionsPerTurn = 100
distBaseToTop = expandArray(distBaseToTop, numSectionsPerTurn)
circumferenceAtBase =  expandArray(circumferenceAtBase, numSectionsPerTurn)
circumferenceAtTop = expandArray(circumferenceAtTop, numSectionsPerTurn)
circumferenceAtPiezo = expandArray(circumferenceAtPiezo, numSectionsPerTurn)
circumferenceAtCap = expandArray(circumferenceAtCap, numSectionsPerTurn)
depthLeftForWiring = expandArray(depthLeftForWiring, numSectionsPerTurn)
numPoints = len(distBaseToTop)

# Main loop

import matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 1)

allPiezos = []
allCaps = []


initialise = True

while sectionEndIds[-1] >= numPoints:
    sectionEndIds.pop()

numSections = len(sectionEndIds)
numTurnsActual = sectionEndIds[-1] / numSectionsPerTurn

startAngles = np.arange(0, np.pi * 2, np.pi * 2 / numSections)
startCoords = [[sectionDist * np.sin(startAngle), sectionDist * np.cos(startAngle)]
               for startAngle in startAngles]
startAngleOffset = np.pi / 2 
# exception
startAngles[0] = startAngles[0] + firstSectionAngleOffset

sectionIdx = -1
sensorsPerSection = []
cableWidths = []
wirePitches = []
for idx in range(sectionEndIds[-1] + 1):
    dbt = distBaseToTop[idx]
    cab = circumferenceAtBase[idx]
    cat = circumferenceAtTop[idx]
    cap = circumferenceAtPiezo[idx]
    cac = circumferenceAtCap[idx]
    dlfw = depthLeftForWiring[idx]
        
    # Initialise a section
    if initialise:
        sectionIdx += 1
        distToNextPiezo = spacingPiezo / 2
        distToNextCap = spacingCap / 2
        angle = startAngles[sectionIdx] + startAngleOffset
        xInner, yInner = startCoords[sectionIdx]
        xOuter = xInner + dbt * np.cos(-angle)
        yOuter = yInner + dbt * np.sin(-angle)
        allInner = []
        allOuter = []
        allInner.append([xInner, yInner])
        allOuter.append([xInner, yInner])
        allInner.append([xInner, yInner])
        allOuter.append([xOuter, yOuter])
        initialise = False
    
    xInner = xInner + (cab / numSectionsPerTurn) * np.sin(angle)
    yInner = yInner + (cab / numSectionsPerTurn) * np.cos(angle)

    xOuter = xInner + dbt * np.cos(-angle)
    yOuter = yInner + dbt * np.sin(-angle)

    angle = angle - np.arctan((cat - cab) / numSectionsPerTurn / dbt)
    allInner.append([xInner, yInner])
    allOuter.append([xOuter, yOuter])

    # put a line at each complete circle
    if idx % numSectionsPerTurn == 0:
        allInner.append([xInner, yInner])
        allOuter.append([xInner, yInner])
        allInner.append([xInner, yInner])
        allOuter.append([xOuter, yOuter])

    distToNextPiezo = distToNextPiezo - cap / numSectionsPerTurn
    if distToNextPiezo <= 0:
        allPiezos.append([
            xInner + (dbt - depthPiezo) * np.cos(-angle),
            yInner + (dbt - depthPiezo) * np.sin(-angle)
            ])
        distToNextPiezo = spacingPiezo                

    distToNextCap = distToNextCap - cac / numSectionsPerTurn
    if distToNextCap <= 0:
        allCaps.append([
            xInner + (dbt - depthCap) * np.cos(-angle),
            yInner + (dbt - depthCap) * np.sin(-angle)
            ])
        distToNextCap = spacingCap

    allInner.append([xInner, yInner])
    allOuter.append([xOuter, yOuter])

    if idx == sectionEndIds[sectionIdx]:
        if distToNextPiezo > spacingPiezo / 2:
            allPiezos.pop()
        if distToNextCap > spacingCap / 2:
            allCaps.pop()
        totalSensors = len(allPiezos) + len(allCaps)
        numSensors = totalSensors - sum(sensorsPerSection)
        sensorsPerSection.append(numSensors)
        wirePitches.append(dlfw - (numSensors * minWirePitch / 2)) # divided by 2 because the cable can come off at the centre.
        cableWidths.append(numSensors * minWirePitch)
        allInner.append([xInner, yInner])
        allOuter.append([xInner, yInner])
        allInner = np.array(allInner)
        allOuter = np.array(allOuter)
        plt.plot(allInner[:, 0], allInner[:, 1], 'k')
        plt.plot(allOuter[:, 0], allOuter[:, 1], 'k')
        initialise = True


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

