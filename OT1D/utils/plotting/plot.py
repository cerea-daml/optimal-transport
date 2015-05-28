#########
# plot.py
#########

import numpy as np

from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib              import gridspec

from ..io.io                 import fileNameSuffix

from positions               import timeTextPBarRect
from positions               import positionsTimeTxtPbar

def plottingOptions():
    options = np.array(['b-', 'g-', 'r-', 'm-', 'y-', 'c-', 'k-',
                        'b--','g--','r--','m--','y--','c--','k--',
                        'b:', 'g:', 'r:', 'm:', 'y:', 'c:', 'k:',
                        'b-.','g-.','r-.','m-.','y-.','c-.','k-.'])
    n       = len(options)
    return (options, n)

def plottingOptionsMultiSim():
    options = np.array([['b-', 'g-', 'r-', 'm-', 'y-', 'c-', 'k-'],
                        ['b--','g--','r--','m--','y--','c--','k--'],
                        ['b:', 'g:', 'r:', 'm:', 'y:', 'c:', 'k:' ],
                        ['b-.','g-.','r-.','m-.','y-.','c-.','k-.']])

    (m, n) = options.shape
    return (options, m, n)

def tryAddCustomLegend(ax, makeRoom):
    if makeRoom:
        divider = make_axes_locatable(ax)
        lax     = divider.append_axes('right', '10%',frameon=False)
        lax.set_yticks([])
        lax.set_xticks([])

    try:
        ax.legend(fontsize='xx-small', loc='center right', bbox_to_anchor=(1.13, 0.5), fancybox=True, framealpha=0.40)
    except:
        ax.legend(fontsize='xx-small', loc='center right', bbox_to_anchor=(1.13, 0.5), fancybox=True)

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

def addTitleLabelsGrid(ax, title, xLabel, yLabel, grid):
    if bool(title):
        ax.set_title(title)
    if bool(xLabel):
        ax.set_xlabel(xLabel)
    if bool(yLabel):
        ax.set_ylabel(yLabel)
    if grid:
        ax.grid()

def trySetScale(ax, xScale, yScale):
    if xScale is not None:
        try:
            ax.set_xscale(xScale)
        except:
            pass

    if yScale is not None:
        try:
            ax.set_yscale(yScale)
        except:
            pass

def plot(ax, Y, X=None, opt=None, **kwargs):
    args = []
    if X is not None:
        args.append(X)
    args.append(Y)
    if opt is not None:
        args.append(opt)

    return ax.plot(*tuple(args), **kwargs)

def addTimeTextPBar(plt, t, tMax):
    rect     = timeTextPBarRect()
    gsTTPB   = gridspec.GridSpec(1, 1, left=rect[0], bottom=rect[1], right=rect[2], top=rect[3])
    ax       = plt.subplot(gsTTPB[0, 0], frameon=False)
    return (ax, plotTimeTextPBar(ax, t, tMax))

def plotTimeTextPBar(ax, t, tMax):
    (xTxt, yTxt, xPbarStart, xPbarEnd, yPbar) = positionsTimeTxtPbar()
    ret = [ax.text(xTxt, yTxt, fileNameSuffix(t, tMax+1)+' / '+str(tMax))]

    if t < tMax:
        lineBkgPbar, = plot(ax, [yPbar,yPbar], [xPbarStart+float(t)/(tMax)*(xPbarEnd-xPbarStart),xPbarEnd], 'k-', linewidth=5)
        ret.append(lineBkgPbar)

    if t > 0:
        linePbar,    = plot(ax, [yPbar,yPbar], [xPbarStart,xPbarStart+float(t)/(tMax)*(xPbarEnd-xPbarStart)], 'g-', linewidth=5)
        ret.append(linePbar)

    adaptAxesExtent(ax, 0.0, 1.0, -0.5, 0.5, 0.0, 0.0, 0, 0, 1, 1, 0.0)
    return ret

def adaptAxesExtent(ax, xmin, xmax, ymin, ymax, extendX, extendY, nbrXTicks, nbrYTicks, xTicksDecimals, yTicksDecimals, EPSILON):    
    xExtend = max(xmax - xmin, EPSILON)
    yExtend = max(ymax - ymin, EPSILON)

    ax.set_xlim(xmin-xExtend*extendX, xmax+xExtend*extendX)
    ax.set_ylim(ymin-yExtend*extendY, ymax+yExtend*extendY)

    xTicks = np.linspace(xmin, xmax, nbrXTicks).round(decimals=xTicksDecimals).tolist()
    yTicks = np.linspace(ymin, ymax, nbrYTicks).round(decimals=yTicksDecimals).tolist()

    ax.set_xticks(xTicks)
    ax.set_yticks(yTicks)
