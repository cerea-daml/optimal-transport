#==================================================
#__________________________________________________

# Copyrigth 2016 A. Farchi and M. Bocquet
# CEREA, joint laboratory Ecole des Ponts ParisTech and EDF R&D

# Code for the paper: Using the Wasserstein distance to compare fields of pollutants:
# Application to the radionuclide atmospheric dispersion of the Fukushima-Daiichi accident
# by A. Farchi, M. Bocquet, Y. Roustan, A. Mathieu and A. Querel

#__________________________________________________
#==================================================

#____________
# plotting.py
#____________

import numpy as np

from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib              import gridspec

from ..io.io                 import fileNameSuffix
from positions               import timeTextPBarRect
from positions               import positionsTimeTxtPbar

#__________________________________________________

def plottingOptions():
    options = np.array(['b-', 'g-', 'r-', 'm-', 'y-', 'c-', 'k-',
                        'b--','g--','r--','m--','y--','c--','k--',
                        'b:', 'g:', 'r:', 'm:', 'y:', 'c:', 'k:',
                        'b-.','g-.','r-.','m-.','y-.','c-.','k-.'])
    n       = len(options)
    return (options, n)

#__________________________________________________

def plottingOptionsMultiSim():
    options = np.array([['b-', 'g-', 'r-', 'm-', 'y-', 'c-', 'k-'],
                        ['b--','g--','r--','m--','y--','c--','k--'],
                        ['b:', 'g:', 'r:', 'm:', 'y:', 'c:', 'k:' ],
                        ['b-.','g-.','r-.','m-.','y-.','c-.','k-.']])

    (m, n) = options.shape
    return (options, m, n)

#__________________________________________________

def makeGrid(nbrOfItems, extendDirection):
    nColumns = int(np.floor(np.sqrt(nbrOfItems)))
    nLines   = nColumns

    while nColumns*nLines < nbrOfItems:
        if extendDirection == 'vertical':
            nLines += 1
        elif extendDirection == 'horizontal':
            nColumns += 1
        else:
            nLines += 1
            nColumns += 1

    return (nLines, nColumns)

#__________________________________________________

def makeAxesGrid(plt, nbrOfItems, order, extendDirection):
    (nLines, nColumns) = makeGrid(nbrOfItems, extendDirection)
    gs                 = gridspec.GridSpec(nLines, nColumns)
    axes               = []

    for j in xrange(nbrOfItems):
        if order == 'horizontalFirst':
            modulo = nColumns
        elif order == 'verticalFirst':
            modulo = nLines

        nc = int(np.mod(j, modulo))
        nl = int((j-nc)/modulo)
        axes.append(plt.subplot(gs[nl,nc]))

    return (gs, axes)

#__________________________________________________

def makeAxesGridTriplot(plt, nbrOfItems, order, extendDirection, extendDirectionTriplot):
    axes               = []
    axesInit           = []
    axesFinal          = []
    (nLines, nColumns) = makeGrid(nbrOfItems, extendDirection)
    if order == 'horizontalFirst':
        modulo = nColumns
    elif order == 'verticalFirst':
        modulo = nLines

    if extendDirectionTriplot == 'horizontal':
        gs = gridspec.GridSpec(nLines, 3*nColumns)

        for j in xrange(nbrOfItems):
            nc = int(np.mod(j, modulo))
            nl = int((j-nc)/modulo)
            axesInit.append(plt.subplot(gs[nl,3*nc]))
            axes.append(plt.subplot(gs[nl,3*nc+1]))
            axesFinal.append(plt.subplot(gs[nl,3*nc+2]))

    elif extendDirectionTriplot == 'vertical':
        gs = gridspec.GridSpec(3*nLines, nColumns)

        for j in xrange(nbrOfItems):
            nc = int(np.mod(j, modulo))
            nl = int((j-nc)/modulo)
            axesInit.append(plt.subplot(gs[3*nl,nc]))
            axes.append(plt.subplot(gs[3*nl+1,nc]))
            axesFinal.append(plt.subplot(gs[3*nl+2,nc]))

    return (gs, axes, axesInit, axesFinal)

#__________________________________________________

def adaptAxesExtent(ax, xmin, xmax, ymin, ymax, extendX, extendY, nbrXTicks, nbrYTicks, xTicksDecimals, yTicksDecimals, EPSILON):    
    xExtend = max(xmax - xmin, EPSILON)
    yExtend = max(ymax - ymin, EPSILON)

    ax.set_xlim(xmin-xExtend*extendX, xmax+xExtend*extendX)
    ax.set_ylim(ymin-yExtend*extendY, ymax+yExtend*extendY)

    xTicks = np.linspace(xmin, xmax, nbrXTicks).round(decimals=xTicksDecimals).tolist()
    yTicks = np.linspace(ymin, ymax, nbrYTicks).round(decimals=yTicksDecimals).tolist()

    ax.set_xticks(xTicks)
    ax.set_yticks(yTicks)

#__________________________________________________

def makeOutputDirLabelPrefixFigNameList(singleOrMulti, outputDirList, labelList, prefixFigName):

    if singleOrMulti == 'multi':
        outputDirListList = [outputDirList]
        labelListList     = [labelList]
        prefixFigNameList = [prefixFigName]
    
    elif singleOrMulti == 'single':
        outputDirListList = []
        labelListList     = []
        prefixFigNameList = []

        for (outputDir, label) in zip(outputDirList, labelList):
            outputDirListList.append([outputDir])
            labelListList.append([label])
            prefixFigNameList.append(prefixFigName+label+'_')

    return (outputDirListList, labelListList, prefixFigNameList)

#__________________________________________________
