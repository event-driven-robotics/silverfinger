# -*- coding: utf-8 -*-
"""
Plot output from capacitance measurements
"""

#%% Single measurements


#%% example of what comes out of serial port of arduino

# format is: ts(ms), measurement (16 bit),
rawData = [
[23459, 41625],
[23477, 41628],
[23495, 41622],
[23512, 41677],
]

#%%
import numpy as np

data = np.array(rawData)

ts = (data[:, 0] - data[0, 0]) / 1000
cap = data[:, 1]
cap = cap - np.mean(cap)

import matplotlib.pyplot as plt

ax = plt.plot(ts, cap)
plt.xlabel('Time (s)')
plt.ylabel('Single-sided capacitance, 16 bit, relative to mean')


#%% Multiple measurements


#%% example of what comes out of serial port of arduino

# format is: ts(ms), measurement (16 bit) x 11,
rawData = [
[11932, 41793, 35548, 35174, 34085, 34773, 35101, 35917, 37358, 45230, 44542, 43892, ],
[12025, 41818, 35547, 35230, 34090, 34759, 34965, 35749, 37327, 45240, 44543, 43904, ],
[12117, 41902, 35546, 35271, 34092, 34742, 34932, 35756, 37316, 45271, 44534, 43957, ],

#%%
import numpy as np

data = np.array(rawData)

ts = (data[:, 0] - data[0, 0]) / 1000

import matplotlib.pyplot as plt

plt.close('all')

for capIdx in range(1, 12):
    cap = data[:, capIdx]
    cap = cap - np.mean(cap)
    ax = plt.plot(ts, cap)
plt.xlabel('Time (s)')
plt.ylabel('Single-sided capacitance, 16 bit, relative to mean')

#%% Cap Network

#%% Example of what the data looks like:


rawData = [
[36590, 1, 0, 881],
[36612, 2, 0, 374],
[36634, 3, 0, 54],
[36654, 4, 0, 56],
[36675, 5, 0, 48],
]
# Each sweep goes through 0-11 for each of sender and receiver

#%%

import numpy as np

data = np.array(rawData)

ts = (data[:, 0] - data[0, 0]) / 1000
sender = data[:, 1]
receiver = data[:, 2]
cap = data[:, 3] / 4096 * 3.3

import matplotlib.pyplot as plt

plt.close('all')

for senderIdx in range(12):
    for receiverIdx in range(12):
        keep = np.logical_and(sender == senderIdx, 
                              receiver == receiverIdx)
            
        ax = plt.plot(ts[keep], cap[keep])
plt.xlabel('Time (s)')
plt.ylabel('inter_node transmission of 3.3V pulse (V)')
#plt.legend([0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11])

#%% Or choose a single cap

plt.close('all')

senderIdx = 8
for receiverIdx in range(12):
    keep = np.logical_and(sender == senderIdx, 
                          receiver == receiverIdx)
        
    ax = plt.plot(ts[keep], cap[keep])
plt.xlabel('Time (s)')
plt.ylabel('inter_node transmission of 3.3V pulse (V)')
plt.legend([0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11])

#%% One sweep per line

# Example data

rawData = [
[2, 709, 275, 339, 253, 143, 107, 150, 52, 119, 37, 39, 671, 857, 128, 206, 208, 48, 57, 67, 65, 63, 171, 478, 865, 395, 196, 304, 47, 37, 31, 93, 50, 88, 493, 131, 377, 1036, 257, 104, 79, 60, 69, 53, 71, 387, 196, 161, 953, 569, 206, 133, 72, 68, 53, 54, 350, 217, 262, 255, 620, 440, 89, 72, 129, 164, 138, 266, 48, 51, 85, 198, 383, 921, 506, 84, 181, 100, 333, 48, 47, 66, 154, 70, 966, 500, 142, 132, 82, 255, 69, 39, 59, 64, 83, 518, 473, 508, 155, 273, 273, 76, 63, 76, 66, 104, 86, 143, 498, 713, 452, 240, 53, 50, 40, 71, 155, 187, 131, 142, 701, 814, 291, 165, 83, 55, 55, 123, 91, 81, 255, 431, 813, ],
[524, 769, 314, 329, 227, 184, 123, 134, 42, 117, 53, 52, 658, 861, 146, 204, 193, 53, 68, 73, 60, 63, 178, 495, 862, 381, 200, 302, 48, 41, 44, 93, 32, 88, 501, 137, 375, 1032, 266, 107, 72, 58, 74, 57, 73, 385, 195, 167, 954, 562, 206, 137, 70, 66, 51, 58, 351, 213, 261, 259, 620, 437, 88, 73, 135, 158, 133, 270, 54, 46, 84, 200, 392, 920, 497, 86, 187, 95, 330, 47, 39, 83, 132, 69, 967, 491, 143, 139, 85, 253, 70, 34, 62, 79, 78, 526, 471, 500, 163, 276, 279, 74, 79, 62, 66, 112, 101, 145, 492, 713, 460, 232, 49, 44, 49, 72, 141, 183, 147, 150, 692, 813, 298, 170, 73, 54, 57, 130, 82, 78, 255, 441, 811, ],
[1167, 761, 296, 330, 248, 175, 113, 144, 78, 134, 58, 28, 676, 855, 131, 207, 208, 54, 72, 53, 71, 73, 174, 474, 866, 419, 197, 262, 36, 50, 75, 59, 41, 75, 520, 128, 365, 1038, 282, 109, 61, 69, 72, 65, 60, 387, 194, 169, 955, 561, 205, 137, 71, 56, 59, 59, 353, 199, 264, 278, 615, 422, 89, 78, 136, 158, 131, 278, 52, 32, 89, 201, 399, 919, 494, 86, 196, 84, 321, 71, 59, 65, 137, 79, 980, 507, 137, 126, 95, 257, 52, 37, 65, 83, 80, 503, 469, 524, 160, 252, 283, 92, 63, 67, 54, 132, 92, 139, 486, 721, 456, 221, 49, 51, 52, 64, 134, 186, 155, 149, 684, 814, 299, 167, 66, 61, 61, 128, 71, 80, 258, 440, 808, ],
]

#%% import one-sweep-per-line data

import numpy as np

data = np.array(rawData)

ts = (data[:, 0] - data[0, 0]) / 1000
cap = data[:, 1:] / 4096 * 3.3

#%% Plot

import numpy as np
import matplotlib.pyplot as plt

plt.close('all')

capIdx = 0
for senderIdx in range(12):
    for receiverIdx in range(12):
        if senderIdx != receiverIdx:
            capCurrent = cap[:, capIdx]
            
            # General
            #ax = plt.plot(ts, capCurrent)
            
            # Selective
            pair = [2, 4]
            if senderIdx in pair and receiverIdx in pair:
                ax = plt.plot(ts, capCurrent)
            
            capIdx += 1
plt.xlabel('Time (s)')
plt.ylabel('inter_node transmission of 3.3V pulse (V)')
#plt.legend([0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11])

#%% correlation of mean

meanMatrix = np.zeros([12, 12])

capIdx = 0
for senderIdx in range(12):
    for receiverIdx in range(12):
        if senderIdx != receiverIdx:
            capCurrent = cap[:, capIdx]
            meanCapCurrent = np.mean(capCurrent)
            meanMatrix[senderIdx, receiverIdx] = meanCapCurrent
            capIdx += 1

plt.close('all')

plt.imshow(meanMatrix)

#%% sums of means both ways

meanMatrix = np.zeros([12, 12])

capIdx = 0
for senderIdx in range(12):
    for receiverIdx in range(12):
        if senderIdx != receiverIdx:
            capCurrent = cap[:, capIdx]
            meanCapCurrent = np.mean(capCurrent)
            if senderIdx > receiverIdx:
                meanMatrix[senderIdx, receiverIdx] = \
                    meanMatrix[senderIdx, receiverIdx] + meanCapCurrent
            else:
                meanMatrix[receiverIdx, senderIdx] = \
                    meanMatrix[receiverIdx, senderIdx] + meanCapCurrent
                
            capIdx += 1

plt.close('all')

plt.imshow(meanMatrix)

#%% remove means then plot

import numpy as np
import matplotlib.pyplot as plt

plt.close('all')

capIdx = 0
for senderIdx in range(12):
    for receiverIdx in range(12):
        if senderIdx != receiverIdx:
            capCurrent = cap[:, capIdx]
            ax = plt.plot(ts, capCurrent - np.mean(capCurrent))
            capIdx += 1
plt.xlabel('Time (s)')
plt.ylabel('inter_node transmission of 3.3V pulse (V)')

#%% Create video of mean-adjusted value matrix

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import Normalize
# First calculate means

capMinusMean = cap - np.mean(cap, axis=0)[np.newaxis, :]

fig, ax = plt.subplots()


# ims is a list of lists, each row is a list of artists to draw in the
# current frame; here we are just animating one artist, the image, in
# each frame
ims = []
theMin = np.min(capMinusMean)
theMax = np.max(capMinusMean)

norm = Normalize(vmin=theMin, vmax=theMax, clip=False)
for i, capAtCurrentTime in enumerate(capMinusMean):
    capIdx = 0
    matrix = np.zeros([12, 12])
    for senderIdx in range(12):
        for receiverIdx in range(12):
            if senderIdx != receiverIdx:
                capCurrent = capAtCurrentTime[capIdx]
                matrix[senderIdx, receiverIdx] = capCurrent
                capIdx += 1
    im = ax.imshow(matrix, animated=True, norm=norm)
    title = ax.text(0.5,1.05,"Title {}".format(ts[i]), 
                    size=plt.rcParams["axes.titlesize"],
                    ha="center", transform=ax.transAxes, )
    if i == 0:
        ax.imshow(matrix)  # show an initial one first
    ims.append([im, title])

ani = animation.ArtistAnimation(fig, ims, interval=50, blit=False,
                                repeat_delay=1000)

# To save the animation, use e.g.
#
# ani.save("movie.mp4")
#
# or
#
# writer = animation.FFMpegWriter(
#     fps=15, metadata=dict(artist='Me'), bitrate=1800)
# ani.save("movie.mp4", writer=writer)

plt.show()

#%% Try positioning coords over photo

photoSource = "C:/repos/silverfinger/arduino/plates.png"
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
photo = mpimg.imread(photoSource)
imgplot = plt.imshow(photo)
plt.show()

#%%

photoSource = "C:/repos/silverfinger/arduino/plates.png"
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
photo = mpimg.imread(photoSource)

coords = [
    [324, 495],
    [717, 389],
    [527, 468],
    [146, 498],
    [557, 378],
    [347, 444],
    [289, 395],
    [652, 248],
    [480, 310],
    [343, 264],
    [720, 102],
    [539, 174],
    ]

plt.close('all')
imgplot = plt.imshow(photo)
for coord in coords:
    plt.scatter(coord[0], coord[1], s=500, c='red', marker='o')
plt.show()


#%% Create a video of jostled points

photoSource = "C:/repos/silverfinger/arduino/plates.png"

coords = np.array([
    [324, 495],
    [717, 389],
    [527, 468],
    [146, 498],
    [557, 378],
    [347, 444],
    [289, 395],
    [652, 248],
    [480, 310],
    [343, 264],
    [720, 102],
    [539, 174],
    ])


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.image as mpimg
photo = mpimg.imread(photoSource)

# First calculate means

capMinusMean = cap - np.mean(cap, axis=0)[np.newaxis, :]



# ims is a list of lists, each row is a list of artists to draw in the
# current frame; here we are just animating one artist, the image, in
# each frame
ims = []
theMin = np.min(capMinusMean)
theMax = np.max(capMinusMean)

scaleFactor = 1
for i, capAtCurrentTime in enumerate(capMinusMean):

    plt.close('all')
    fig, ax = plt.subplots()

    capIdx = 0
    matrix = np.zeros([12, 12])
    currentCoords = coords.copy()
    for senderIdx in range(12):
        for receiverIdx in range(12):
            if senderIdx != receiverIdx:
                capCurrent = capAtCurrentTime[capIdx]
                currentCoords[senderIdx] = currentCoords[senderIdx] - (
                    currentCoords[senderIdx] - currentCoords[receiverIdx]
                    ) * capCurrent * scaleFactor
                capIdx += 1
    im = ax.imshow(photo, animated=True)
    im = ax.scatter(currentCoords[:, 0], currentCoords[:, 1], s=50, c='red', marker='o')
    
    #
    #title = ax.text(0.5,1.05,"Time: {} s".format(ts[i]), 
    #                size=plt.rcParams["axes.titlesize"],
    #                ha="center", transform=ax.transAxes, )
    im = ax.set_title("Time: {} s".format(ts[i]))
    fileName = str(i) + '.png'
    plt.savefig(fileName)
    ims.append(fileName)
    
#%% Create video file
    
import os
import moviepy.video.io.ImageSequenceClip
fps=10

clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(ims, fps=fps)
clip.write_videofile('my_video.mp4')


#%% Same thing, but consider only selective pairings

pairings = [
    [0, 3],
    [0, 5],
    [1, 4],
    [2, 4],
    [2, 5],
    [3, 6],
    [4, 7],
    [4, 8],
    [5, 6],
    [5, 8],
    [6, 9],
    [7, 10],
    [7, 11],
    [8, 9],
    [8, 11],
    ]

photoSource = "C:/repos/silverfinger/arduino/plates.png"

import numpy as np
coords = np.array([
    [324, 495],
    [717, 389],
    [527, 468],
    [146, 498],
    [557, 378],
    [347, 444],
    [289, 395],
    [652, 248],
    [480, 310],
    [343, 264],
    [720, 102],
    [539, 174],
    ])

scaleFactor = 2

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.image as mpimg
import os
import moviepy.video.io.ImageSequenceClip
photo = mpimg.imread(photoSource)
capMinusMean = cap - np.mean(cap, axis=0)[np.newaxis, :]
ims = []
theMin = np.min(capMinusMean)
theMax = np.max(capMinusMean)
for i, capAtCurrentTime in enumerate(capMinusMean):
    plt.close('all')
    fig, ax = plt.subplots()
    capIdx = 0
    matrix = np.zeros([12, 12])
    currentCoords = coords.copy()
    for senderIdx in range(12):
        for receiverIdx in range(12):
            if senderIdx != receiverIdx:
                for pair in pairings:
                    if senderIdx in pair and receiverIdx in pair:
                        capCurrent = capAtCurrentTime[capIdx]
                        currentCoords[senderIdx] = currentCoords[senderIdx] - (
                            currentCoords[senderIdx] - currentCoords[receiverIdx]
                            ) * capCurrent * scaleFactor
                capIdx += 1
    im = ax.imshow(photo, animated=True)
    im = ax.scatter(currentCoords[:, 0], currentCoords[:, 1], s=50, c='red', marker='o')
    
    #
    #title = ax.text(0.5,1.05,"Time: {} s".format(ts[i]), 
    #                size=plt.rcParams["axes.titlesize"],
    #                ha="center", transform=ax.transAxes, )
    im = ax.set_title("Time: {} s".format(ts[i]))
    fileName = str(i) + '.png'
    plt.savefig(fileName)
    ims.append(fileName)
fps=10
clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(ims, fps=fps)
clip.write_videofile('my_video.mp4')
