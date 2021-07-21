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

