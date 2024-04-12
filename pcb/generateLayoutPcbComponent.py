# -*- coding: utf-8 -*-
"""
Created on Mon May  3 12:37:53 2021

@author: sbamford
"""

import numpy as np

def str3(num):
    return f'{num:.3f}'


def lineToPcb(file, axes, x1, y1, x2, y2, layer='Edge.Cuts', width=0.1):
    widthStr = str3(width)
    file.write('\t(gr_line (start ' + str3(x1) + ' '
            + str3(y1) + ') (end '
            + str3(x2) + ' ' + str3(y2)
            + ') (layer ' + layer + ') (width ' + widthStr + '))\n')
    axes.plot([x1, x2], [y1, y2], 'k')


def segmentToPcb(file, axes, x1, y1, x2, y2, layer='F.Cu', width=0.2, net=0):
    widthStr = str3(width)
    file.write('\t(segment (start ' + str3(x1) + ' ' + str3(y1)
               + ') (end ' + str3(x2) + ' ' + str3(y2)
               + ') (width ' + widthStr + ') (layer ' + layer + ') (net 0))\n')
    axes.plot([x1, x2], [y1, y2], 'k')


def textToPcb(file, axes, x, y, text, rotation):
    file.write('\t(gr_text ' + text + ' (at ' + str3(x) + ' ' + str3 (y) + 
               ' ' + str(int(rotation)) + ') (layer F.SilkS) ' +
               '(effects (font (size 2 2) (thickness 0.15))))\n')
    file.write('\t(gr_text ' + text + ' (at ' + str3(x) + ' ' + str3 (y) + 
               ' ' + str(int(rotation)) + ') (layer B.SilkS) ' +
               '(effects (font (size 2 2) (thickness 0.15)) (justify mirror)))\n')
    axes.text(x, y, text, rotation=rotation)
    
    
def filledPolygonToPcb(file, axes, xArray, yArray, layer='F.Adhes'):
    stringForPoints = []
    for x, y, in zip(xArray, yArray):
        stringForPoints.append('\t\t\t\t(xy ' +
                                       str3(x) + ' ' +
                                       str3(y) + ')\n')
    xArray = np.append(xArray, xArray[0])
    yArray = np.append(yArray, yArray[0])
    axes.plot(xArray, yArray, 'k')
    
    stringForPoints = ''.join(stringForPoints)
    file.write('\t(zone (net 0) (net_name "") (layer ' + layer + ') (tstamp 0) (hatch edge 0.0)')
    file.write('\t\t(connect_pads (clearance 0.0))\n')
    file.write('\t\t(min_thickness 0.0)\n')
    file.write('\t\t(fill yes (arc_segments 32) (thermal_gap 0.0) (thermal_bridge_width 0.0))\n')
    file.write('\t\t(polygon\n')
    file.write('\t\t\t(pts\n')
    file.write(stringForPoints)
    file.write('\t\t\t)\n')
    file.write('\t\t)\n')
    file.write('\t\t(filled_polygon\n')
    file.write('\t\t\t(pts\n')
    file.write(stringForPoints)
    file.write('\t\t\t)\n')
    file.write('\t\t)\n')
    file.write('\t)')
    file.write('\n')
    
    
def writeConnector(file, axes, orientation, x, y, refNo):
    connectorStr = '''
  (module Connector_PinHeader_2.54mm:PinHeader_2x03_P2.54mm_Vertical (layer F.Cu) (tedit 59FED5CC) (tstamp 608FD40F)
    (at #xxx# #yyy##orientation#)
    (descr "Through hole straight pin header, 2x03, 2.54mm pitch, double rows")
    (tags "Through hole pin header THT 2x03 2.54mm double row")
    (fp_text reference J#jRef# (at 1.27 -3.33) (layer F.SilkS)
      (effects (font (size 1 1) (thickness 0.15)))
    )
    (fp_text value PinHeader_2x03_P2.54mm_Vertical (at 1.27 7.41) (layer F.Fab)
      (effects (font (size 1 1) (thickness 0.15)))
    )
    (fp_line (start 4.35 -1.8) (end -1.8 -1.8) (layer F.CrtYd) (width 0.05))
    (fp_line (start 4.35 6.85) (end 4.35 -1.8) (layer F.CrtYd) (width 0.05))
    (fp_line (start -1.8 6.85) (end 4.35 6.85) (layer F.CrtYd) (width 0.05))
    (fp_line (start -1.8 -1.8) (end -1.8 6.85) (layer F.CrtYd) (width 0.05))
    (fp_line (start -1.33 -1.33) (end 0 -1.33) (layer F.SilkS) (width 0.12))
    (fp_line (start -1.33 0) (end -1.33 -1.33) (layer F.SilkS) (width 0.12))
    (fp_line (start 1.27 -1.33) (end 3.87 -1.33) (layer F.SilkS) (width 0.12))
    (fp_line (start 1.27 1.27) (end 1.27 -1.33) (layer F.SilkS) (width 0.12))
    (fp_line (start -1.33 1.27) (end 1.27 1.27) (layer F.SilkS) (width 0.12))
    (fp_line (start 3.87 -1.33) (end 3.87 6.41) (layer F.SilkS) (width 0.12))
    (fp_line (start -1.33 1.27) (end -1.33 6.41) (layer F.SilkS) (width 0.12))
    (fp_line (start -1.33 6.41) (end 3.87 6.41) (layer F.SilkS) (width 0.12))
    (fp_line (start -1.27 0) (end 0 -1.27) (layer F.Fab) (width 0.1))
    (fp_line (start -1.27 6.35) (end -1.27 0) (layer F.Fab) (width 0.1))
    (fp_line (start 3.81 6.35) (end -1.27 6.35) (layer F.Fab) (width 0.1))
    (fp_line (start 3.81 -1.27) (end 3.81 6.35) (layer F.Fab) (width 0.1))
    (fp_line (start 0 -1.27) (end 3.81 -1.27) (layer F.Fab) (width 0.1))
    (fp_text user %R (at 1.27 2.54 90) (layer F.Fab)
      (effects (font (size 1 1) (thickness 0.15)))
    )
    (pad 6 thru_hole oval (at 2.54 5.08) (size 1.7 1.7) (drill 1) (layers *.Cu *.Mask))
    (pad 5 thru_hole oval (at 0 5.08) (size 1.7 1.7) (drill 1) (layers *.Cu *.Mask))
    (pad 4 thru_hole oval (at 2.54 2.54) (size 1.7 1.7) (drill 1) (layers *.Cu *.Mask))
    (pad 3 thru_hole oval (at 0 2.54) (size 1.7 1.7) (drill 1) (layers *.Cu *.Mask))
    (pad 2 thru_hole oval (at 2.54 0) (size 1.7 1.7) (drill 1) (layers *.Cu *.Mask))
    (pad 1 thru_hole rect (at 0 0) (size 1.7 1.7) (drill 1) (layers *.Cu *.Mask))
    

     (model ${KISYS3DMOD}/Connector_PinHeader_2.54mm.3dshapes/PinHeader_2x03_P2.54mm_Vertical.wrl
      (at (xyz 0 0 0))
      (scale (xyz 1 1 1))
      (rotate (xyz 0 0 0))
    )
  )
    '''
    # x and y are xinnerext
    # connector component is defined wrt connector hole 1
    xl = x - orientation * 4.7
    xr = xl + orientation * 6.15
    yt = y
    yb = yt + orientation * 8.65
    #lineToPcb(file, axes, xl, yt, xr, yt)
    lineToPcb(file, axes, xl, yb, xr, yb)
    lineToPcb(file, axes, xl, yt, xl, yb)
    lineToPcb(file, axes, xr, yt, xr, yb)
    
    xHole = x + orientation * -2.95
    yHole = y + orientation * 1.8
    connectorStr = connectorStr.replace('#xxx#', str3(xHole))
    connectorStr = connectorStr.replace('#yyy#', str3(yHole))
    connectorStr = connectorStr.replace('#jRef#', str(refNo))
    if orientation == -1:
        connectorStr = connectorStr.replace('#orientation#', ' 180')
    else:
        connectorStr = connectorStr.replace('#orientation#', '')
    file.write(connectorStr)
    
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
        segmentToPcb(file, axes, x1, y1, x2, y2)
    # final edge cuts
    lineToPcb(file, axes, xr, yt, x, yt)
    lineToPcb(file, axes, xl, yt, xl + orientation * 1.2, yt)
    # drawing rigid area
    xArray = np.array([xl, xr, xr, xl])
    yArray = np.array([yt, yt, yb, yb])
    filledPolygonToPcb(file, axes, xArray, yArray, layer='Dwgs.User')
    