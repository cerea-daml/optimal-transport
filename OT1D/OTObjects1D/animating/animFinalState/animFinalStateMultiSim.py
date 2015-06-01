###########################
# animFinalStateMultiSim.py
###########################
#
# util to animate the final state for multiple simulations 
#

import numpy                as np
import matplotlib.pyplot    as plt

from matplotlib.animation import FuncAnimation

from ....utils.io.extractFinalState import extractFinalStateMultiSim
from ....utils.plotting.plot        import makeAxesGrid
from ....utils.plotting.plot        import plot
from ....utils.plotting.plot        import plottingOptions
from ....utils.plotting.plot        import addTitleLabelsGrid
from ....utils.plotting.plot        import tryAddCustomLegend
from ....utils.plotting.plot        import addTimeTextPBar
from ....utils.plotting.plot        import plotTimeTextPBar
from ....utils.plotting.plot        import adaptAxesExtent
from ....utils.plotting.positions   import figureRect

def makeAnimFinalStateMultiSim(outputDirList,
                               labelList,
                               transparencyFunction,
                               legend,
                               grid,
                               timeTextPBar,
                               xLabel,
                               yLabel,
                               extendX,
                               extendY,
                               nbrXTicks,
                               nbrYTicks,
                               xTicksDecimals,
                               yTicksDecimals,
                               order,
                               extendDirection,
                               kwargsFuncAnim,
                               EPSILON):

    (options, nModOptions)                  = plottingOptions()
    (fs, finits, ffinals, mini, maxi, Pmax) = extractFinalStateMultiSim(outputDirList)
 
    xmin = 0.0
    xmax = 1.0

    figure     = plt.figure()
    plt.clf()
    (gs, axes) = makeAxesGrid(plt, len(outputDirList), order=order, extendDirection=extendDirection)

    alphaInit  = transparencyFunction(1.-float(0)/(Pmax+1.))
    alphaFinal = transparencyFunction(float(0)/(Pmax+1.))
    
    for (f, finit, ffinal, label, ax) in zip(fs, finits, ffinals, labelList, axes):
        X            = np.linspace(0.0, 1.0, finit.size)
        lineCurrent, = plot(ax, f[:,0], X, options[np.mod(0, nModOptions)], label='$f$')
        lineInit,    = plot(ax, finit, X, options[np.mod(1, nModOptions)], label='$f_{init}$', alpha=alphaInit)
        lineFinal,   = plot(ax, ffinal, X, options[np.mod(2, nModOptions)], label='$f_{final}$', alpha=alphaFinal)
        
        adaptAxesExtent(ax, xmin, xmax, mini, maxi, extendX, extendY, nbrXTicks, nbrYTicks, xTicksDecimals, yTicksDecimals, EPSILON)
        addTitleLabelsGrid(ax, label, xLabel, yLabel, grid)
        if legend:
            tryAddCustomLegend(ax, True)

    gs.tight_layout(figure, rect=figureRect(False, timeTextPBar))
    if timeTextPBar:
        (TTPBax, ret) = addTimeTextPBar(plt, 0, Pmax+1)

    def animate(t):
        ret = []
        alphaInit  = transparencyFunction(1.-float(t)/(Pmax+1.))
        alphaFinal = transparencyFunction(float(t)/(Pmax+1.))

        for (f, finit, ffinal, label, ax) in zip(fs, finits, ffinals, labelList, axes):
            ax.cla()
            X            = np.linspace(0.0, 1.0, finit.size)

            lineCurrent, = plot(ax, f[:,t], X, options[np.mod(0, nModOptions)], label='$f$')
            lineInit,    = plot(ax, finit, X, options[np.mod(1, nModOptions)], label='$f_{init}$', alpha=alphaInit)
            lineFinal,   = plot(ax, ffinal, X, options[np.mod(2, nModOptions)], label='$f_{final}$', alpha=alphaFinal)
            ret.extend([lineInit,lineFinal,lineCurrent])

            adaptAxesExtent(ax, xmin, xmax, mini, maxi, extendX, extendY, nbrXTicks, nbrYTicks, xTicksDecimals, yTicksDecimals, EPSILON)
            addTitleLabelsGrid(ax, label, xLabel, yLabel, grid)
            if legend:
                tryAddCustomLegend(ax, False)

        if timeTextPBar:
            TTPBax.cla()
            ret.extend(plotTimeTextPBar(TTPBax, t, Pmax+1))

        return tuple(ret)

    def init():
        return animate(0)

    frames = np.arange(Pmax+2)    
    print('Making animation ...')
    return FuncAnimation(figure, animate, frames, init_func=init, **kwargsFuncAnim)
