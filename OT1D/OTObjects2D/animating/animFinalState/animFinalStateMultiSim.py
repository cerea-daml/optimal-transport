##########################
# plotFinalStateMuliSim.py
##########################
#
# util to plot the final state for multiple simulations 
#

import numpy                as np
import matplotlib.pyplot    as plt

from matplotlib.animation           import FuncAnimation

from ....utils.io.io                import fileNameSuffix
from ....utils.io.extractFinalState import extractFinalStateMultiSim
from ....utils.plotting.positions   import figureRect
from ....utils.plotting.plot        import makeAxesGrid
from ....utils.plotting.plot        import adaptAxesExtent
from ....utils.plotting.plot        import addTitleLabelsGrid
from ....utils.plotting.plot        import addTimeTextPBar
from ....utils.plotting.plot        import plotTimeTextPBar
from ....utils.plotting.plotMatrix  import addColorBar
from ....utils.plotting.plotMatrix  import plotMatrix
from ....utils.plotting.saveFig     import saveFig

def makeAnimFinalStateMultiSim(kwargsFuncAnim,
                               outputDirList,
                               figDir,
                               labelList,
                               transparencyFunction,
                               plotter,
                               kwargs,
                               kwargsInit,
                               kwargsFinal,
                               colorBar,
                               cmapName,
                               timeTextPBar,
                               xLabel,
                               yLabel,
                               cLabel,
                               extendX,
                               extendY,
                               nbrXTicks,
                               nbrYTicks,
                               nbrCTicks,
                               xTicksDecimals,
                               yTicksDecimals,
                               cticksDecimals,
                               order,
                               extendDirection,
                               EPSILON):

    (fs, finits, ffinals, mini, maxi, Pmax) = extractFinalStateMultiSim(outputDirList)

    xmin = 0.0
    xmax = 1.0

    ymin = 0.0
    ymax = 1.0

    figure = plt.figure()
    plt.clf()

    (gs, axes) = makeAxesGrid(plt, len(outputDirList), order=order, extendDirection=extendDirection)

    alphaInit  = transparencyFunction(1.-float(0)/(Pmax+1.))
    alphaFinal = transparencyFunction(float(0)/(Pmax+1.))

    for (f, finit, ffinal, label, ax) in zip(fs, finits, ffinals, labelList, axes):
        imC = plotMatrix(ax, f[:,:,0], plotter=plotter, vmin=mini, vmax=maxi, **kwargs)
        imI = plotMatrix(ax, finit, plotter='contour', vmin=mini, vmax=maxi, **kwargsInit)
        imF = plotMatrix(ax, ffinal, plotter='contour', vmin=mini, vmax=maxi, **kwargsFinal)

        adaptAxesExtent(ax, xmin, xmax, ymin, ymax, extendX, extendY, nbrXTicks, nbrYTicks, xTicksDecimals, yTicksDecimals, EPSILON)
        addTitleLabelsGrid(ax, title=label, xLabel=xLabel, yLabel=yLabel, grid=False)

    gs.tight_layout(figure, rect=figureRect(colorBar, timeTextPBar))
    if colorBar:
        (cax, cbar)   = addColorBar(plt, timeTextPBar, cmapName, mini, maxi, nbrCTicks, cticksDecimals, cLabel)

    if timeTextPBar:
        (TTPBax, ret) = addTimeTextPBar(plt, 0, Pmax+1)

    def animate(t):
        ret = []
        kwargsInit['alpha']  = transparencyFunction(1.-float(t)/(Pmax+1.))
        kwargsFinal['alpha'] = transparencyFunction(float(t)/(Pmax+1.))

        for (f, finit, ffinal, label, ax) in zip(fs, finits, ffinals, labelList, axes):
            ax.cla()

            imC = plotMatrix(ax, f[:,:,t], plotter=plotter, vmin=mini, vmax=maxi, **kwargs)
            imI = plotMatrix(ax, finit, plotter='contour', vmin=mini, vmax=maxi, **kwargsInit)
            imF = plotMatrix(ax, ffinal, plotter='contour', vmin=mini, vmax=maxi, **kwargsFinal)
            ret.extend([imC,imI,imF])

            adaptAxesExtent(ax, xmin, xmax, ymin, ymax, extendX, extendY, nbrXTicks, nbrYTicks, xTicksDecimals, yTicksDecimals, EPSILON)
            addTitleLabelsGrid(ax, title=label, xLabel=xLabel, yLabel=yLabel, grid=False)

        if timeTextPBar:
            TTPBax.cla()
            ret.extend(plotTimeTextPBar(TTPBax, t, Pmax+1))

        return tuple(ret)

    def init():
        return animate(0)

    frames = np.arange(Pmax+2)
    print('Making animation ...')
    return FuncAnimation(figure, animate, frames, init_func=init, **kwargsFuncAnim)
