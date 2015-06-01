###############
# plotMatrix.py
###############

import numpy      as np
import matplotlib as mpl

from matplotlib              import gridspec
from mpl_toolkits.axes_grid1 import make_axes_locatable
from cmap                    import colormap
from positions               import colorBarRect

def plotMatrix(ax, matrix, plotter, **kwargs):
    kwargs = fillKwargs(plotter, **kwargs)

    if plotter == 'imshow':
        return ax.imshow(matrix, **kwargs)

    elif plotter == 'contour':
        return ax.contour(matrix, **kwargs)

    elif plotter == 'contourf':
        return ax.contourf(matrix, **kwargs)

def fillKwargs(plotter, **kwargs):
    if not kwargs.has_key('origin'):
        kwargs['origin'] = 'lower'
    if not kwargs.has_key('extent'):
        kwargs['extent'] = [0.,1.,0.,1.]

    if plotter == 'imshow':
        if not kwargs.has_key('interpolation'):
            kwargs['interpolation'] = 'nearest'
    elif plotter == 'contour':
        if not kwargs.has_key('colors'):
            kwargs['colors'] = 'k'
        if not kwargs.has_key('linestyles'):
            kwargs['linestyles'] = 'solid'
        #if not kwargs.has_key('linewidths'):
        #    kwargs['linewidths'] = 1.5

    return kwargs

def addColorBar(plt, timeTextPBar, cmapName, mini, maxi, nbrTicks, ticksDecimals, label):
    rect = colorBarRect(timeTextPBar)
    gsCB = gridspec.GridSpec(1, 1, left=rect[0], bottom=rect[1], right=rect[2], top=rect[3])
    cax  = plt.subplot(gsCB[0, 0], frameon=False)
    cbar = plotColorBar(cax, cmapName, mini, maxi, nbrTicks, ticksDecimals, '')
    cbar.set_label(label, labelpad=-80)
    return (cax, cbar)

def plotColorBar(cax, cmapName, mini, maxi, nbrTicks, ticksDecimals, label):
    cmap  = colormap(cmapName)
    norm  = mpl.colors.Normalize(vmin=mini, vmax=maxi, clip=False)

    if nbrTicks < 2:
        ticks = None
    else:
        ticks = np.linspace(mini, maxi, nbrTicks).round(decimals=ticksDecimals).tolist()

    return mpl.colorbar.ColorbarBase(cax, cmap=cmap, norm=norm, ticks=ticks, label=label, orientation='vertical')
