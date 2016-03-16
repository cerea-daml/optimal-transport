#==================================================
#__________________________________________________

# Copyrigth 2016 A. Farchi and M. Bocquet
# CEREA, joint laboratory Ecole des Ponts ParisTech and EDF R&D

# Code for the paper: Using the Wasserstein distance to compare fields of pollutants:
# Application to the radionuclide atmospheric dispersion of the Fukushima-Daiichi accident
# by A. Farchi, M. Bocquet, Y. Roustan, A. Mathieu and A. Querel

#__________________________________________________
#==================================================

#______________
# plotMatrix.py
#______________

import numpy      as np
import matplotlib as mpl

from matplotlib              import gridspec
from mpl_toolkits.axes_grid1 import make_axes_locatable
from .cmap                    import colormap
from .positions               import colorBarRect

#__________________________________________________

def plotMatrix(ax, matrix, plotter, xmin=0.0, xmax=1.0, ymin=0.0, ymax=1.0, cmapName='jet', **kwargs):
    kwargs = fillKwargs(plotter, xmin, xmax, ymin, ymax, cmapName, **kwargs)

    if plotter == 'imshow':
        return ax.imshow(matrix.transpose(), **kwargs)

    elif plotter == 'contour':
        return ax.contour(matrix.transpose(), **kwargs)

    elif plotter == 'contourf':
        return ax.contourf(matrix.transpose(), **kwargs)

#__________________________________________________

def fillKwargs(plotter, xmin, xmax, ymin, ymax, cmapName, **kwargs):

    if plotter == 'imshow' or plotter == 'contourf':

        cmap   = colormap(cmapName)
        if 'vmin' in kwargs and 'vmax' in kwargs:
            norm = mpl.colors.Normalize(vmin=kwargs['vmin'], vmax=kwargs['vmax'], clip=False)
            kwargs['norm'] = norm

        kwargs['cmap'] = cmap

    else:
        kwargs['cmap'] = None
        try:
            del kwargs['norm']
        except:
            pass

    if not 'origin' in kwargs:
        kwargs['origin'] = 'lower'
    if not 'extent' in kwargs:
        kwargs['extent'] = [xmin, xmax, ymin, ymax]

    if plotter == 'imshow':
        if not 'interpolation' in kwargs:
            kwargs['interpolation'] = 'nearest'
    elif plotter == 'contour':
        if not 'colors' in kwargs:
            kwargs['colors'] = 'k'
        if not 'linestyles' in kwargs:
            kwargs['linestyles'] = 'solid'

    return kwargs

#__________________________________________________

def filterKwargsMiniMaxiCmapName(mini, maxi, cmapName, **kwargs):

    if 'vmin' in kwargs:
        miniR = kwargs['vmin']
        del kwargs['vmin']
    else:
        miniR = mini


    if 'vmax' in kwargs:
        maxiR = kwargs['vmax']
        del kwargs['vmax']
    else:
        maxiR = maxi

    if 'cmap' in kwargs:
        cmapNameR = kwargs['cmap']
        del kwargs['cmap']
    else:
        cmapNameR = cmapName

    return (miniR, maxiR, cmapNameR, kwargs)

#__________________________________________________

def addColorBar(plt, timeTextPBar, cmapName, mini, maxi, nbrTicks, ticksDecimals, label):
    rect = colorBarRect(timeTextPBar)
    gsCB = gridspec.GridSpec(1, 1, left=rect[0], bottom=rect[1], right=rect[2], top=rect[3])
    cax  = plt.subplot(gsCB[0, 0], frameon=False)
    cbar = plotColorBar(cax, cmapName, mini, maxi, nbrTicks, ticksDecimals, '')
    cbar.set_label(label, labelpad=-80)
    return (cax, cbar)

#__________________________________________________

def plotColorBar(cax, cmapName, mini, maxi, nbrTicks, ticksDecimals, label, orientation='vertical'):
    cmap  = colormap(cmapName)
    norm  = mpl.colors.Normalize(vmin=mini, vmax=maxi, clip=False)

    if nbrTicks < 2:
        ticks = None
    else:
        ticks = np.linspace(mini, maxi, nbrTicks).round(decimals=ticksDecimals).tolist()

    cbar = mpl.colorbar.ColorbarBase(cax, cmap=cmap, norm=norm, ticks=ticks, label=label, orientation=orientation)
    cbar.solids.set_rasterized(True)
    cbar.solids.set_edgecolor('face')
    return cbar

#__________________________________________________
