##############
# positions.py
##############

#import numpy as np

#from mpl_toolkits.axes_grid1 import make_axes_locatable
#from matplotlib              import gridspec

#from ..io.io                 import fileNameSuffix

def positionsTimeTxtPbar():
    xTxt = 0.0
    yTxt = 0.0

    xPbarStart = 0.2
    xPbarEnd   = 0.8
    yPbar      = 0.0

    return (xTxt, yTxt, xPbarStart, xPbarEnd, yPbar)

def figureRect(addColorBar=True, addTimeTextPBar=True):
    xStart = 0.0
    if addColorBar:
        xEnd = 0.85
    else:
        xEnd = 1.0
    if addTimeTextPBar:
        yStart = 0.12
    else:
        yStart = 0.0
    yEnd = 1.0

    return [xStart, yStart, xEnd, yEnd]

def colorBarRect(addTimeTextPBar=True):
    xStart = 0.87
    xEnd   = 0.93

    if addTimeTextPBar:
        yStart = 0.12
    else:
        yStart = 0.0
    yEnd = 1.0

    return [xStart, yStart, xEnd, yEnd]

def timeTextPBarRect():
    xStart = 0.07
    xEnd   = 0.93
    yStart = 0.04
    yEnd   = 0.10

    return [xStart, yStart, xEnd, yEnd]

'''
def positions1D(xmin, xmax, ymin, ymax, EPSILON):

    xExtend    = max(xmax - xmin, EPSILON)
    yExtend    = max(ymax - ymin, EPSILON)

    xPbarStart = xmin + 0.2 * xExtend
    xPbarEnd   = xmin + 0.8 * xExtend
    yPbar      = ymin - 0.05 * yExtend

    xTxt       = xmin + 0.01 * xExtend
    yTxt       = ymin - 0.05 * yExtend

    ymax      += 0.1 * yExtend
    ymin      -= 0.1 * yExtend

    return (ymin, ymax, xTxt, yTxt, xPbarStart, xPbarEnd, yPbar)
'''
