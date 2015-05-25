###############
# plotMatrix.py
###############

import matplotlib as mpl

from mpl_toolkits.axes_grid1 import make_axes_locatable

def positions2d(xmin, xmax, ymin, ymax, EPSILON):
    yExtend    = min(ymax - ymin, EPSILON)
    xExtend    = min(xmax - xmin, EPSILON)

    xPbarStart = xmin + 0.2 * xExtend
    xPbarEnd   = xmin + 0.8 * xExtend
    yPbar      = ymin - 0.05 * yExtend

    xTxt       = xmin + 0.01 * xExtend
    yTxt       = ymin - 0.05 * yExtend

    ymax      += 0.1 * yExtend
    ymin      -= 0.1 * yExtend
    xmax      += 0.1 * xExtend
    xmin      -= 0.1 * xExtend

    return (xmin, xmax, ymin, ymax, xTxt, yTxt, xPbarStart, xPbarEnd, yPbar)

def plotMatrix(ax, matrix, plotter='imshow', **kwargs):

    if not kwargs.has_key('origin'):
        kwargs['origin'] = 'lower'
    if not kwargs.has_key('extent'):
        kwargs['extent'] = [0.,1.,0.,1.]

    if plotter == 'imshow':

        if not kwargs.has_key('interpolation'):
            kwargs['interpolation'] = 'nearest'
        return ax.imshow(matrix, **kwargs)

    elif plotter == 'contour':

        if not kwargs.has_key('colors'):
            kwargs['colors'] = 'k'
        if not kwargs.has_key('linestyles'):
            kwargs['linestyles'] = 'solid'
        if not kwargs.has_key('linewidths'):
            kwargs['linewidths'] = 1.5

        return ax.contour(matrix, **kwargs)

    elif plotter == 'contourf':

        return ax.contourf(matrix, **kwargs)

def addColorBar(ax, mini, maxi):
    divider = make_axes_locatable(ax)
    cax     = divider.append_axes('right', '10%', pad='5%')

    cmap    = mpl.cm.jet
    norm    = mpl.colors.Normalize(vmin=mini, vmax=maxi)
    return mpl.colorbar.ColorbarBase(cax, cmap=cmap, norm=norm, orientation='vertical')

def addColorBarMultiSim(cax, mini, maxi):
    cmap = mpl.cm.jet
    norm = mpl.colors.Normalize(vmin=mini, vmax=maxi)
    return mpl.colorbar.ColorbarBase(cax, cmap=cmap, norm=norm, orientation='vertical')
