#########
# plot.py
#########

import numpy as np

from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib              import gridspec

from ..io.io                 import fileNameSuffix

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

def tryAddCustomLegend(ax):
    divider = make_axes_locatable(ax)
    lax     = divider.append_axes('right', '10%',frameon=False)
    lax.set_yticks([])
    lax.set_xticks([])

    try:
        ax.legend(fontsize='xx-small', loc='center right', bbox_to_anchor=(1.13, 0.5), fancybox=True, framealpha=0.40)
    except:
        ax.legend(fontsize='xx-small', loc='center right', bbox_to_anchor=(1.13, 0.5), fancybox=True)

def plotTimeTextPBar(ax, t, tMax, xTxt, yTxt, xPbarStart, xPbarEnd, yPbar):
    timeText = ax.text(xTxt, yTxt, fileNameSuffix(t, tMax+1)+' / '+str(tMax))
    ret      = [timeText]
    if t < tMax:
        lineBkgPbar, = plot(ax, [yPbar,yPbar], [xPbarStart+float(t)/(tMax)*(xPbarEnd-xPbarStart),xPbarEnd], 'k-', linewidth=5)
        ret.append(lineBkgPbar)
    if t > 0:
        linePbar,    = plot(ax, [yPbar,yPbar], [xPbarStart,xPbarStart+float(t)/(tMax)*(xPbarEnd-xPbarStart)], 'g-', linewidth=5)
        ret.append(linePbar)
    return ret

def makeGrid(nbrOfItems, extendDirection='vertical'):
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

def makeAxesGrid(plt, nbrOfItems, order='horizontalFirst', extendDirection='vertical'):
    (nLines, nColumns) = makeGrid(nbrOfItems, extendDirection='vertical')
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

def addTitleLabelsGrid(ax, title=None, xLabel=None, yLabel=None, grid=False):
    if title is not None:
        ax.set_title(title)
    if xLabel is not None:
        ax.set_xlabel(xLabel)
    if yLabel is not None:
        ax.set_ylabel(yLabel)
    if grid:
        ax.grid()

def trySetScale(ax, xScale=None, yScale=None):
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

def positions(xmin, xmax, ymin, ymax, EPSILON):
    yExtend    = min(ymax - ymin, EPSILON)
    xExtend    = min(xmax - xmin, EPSILON)

    xPbarStart = xmin + 0.2 * xExtend
    xPbarEnd   = xmin + 0.8 * xExtend
    yPbar      = ymin - 0.05 * yExtend

    xTxt       = xmin + 0.01 * xExtend
    yTxt       = ymin - 0.05 * yExtend

    ymax      += 0.1 * yExtend
    ymin      -= 0.1 * yExtend

    return (ymin, ymax, xTxt, yTxt, xPbarStart, xPbarEnd, yPbar)
