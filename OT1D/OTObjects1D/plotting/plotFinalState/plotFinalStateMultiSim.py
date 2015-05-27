###########################
# plotFinalStateMultiSim.py
###########################
#
# util to plot the final state for multiple simulations 
#

import numpy             as np
import cPickle           as pck
import matplotlib.pyplot as plt

from matplotlib        import gridspec
from scipy.interpolate import interp1d

from ....utils.io.io                import fileNameSuffix
from ....utils.io.extractFinalState import extractFinalStateMultiSim
from ....utils.plotting.plot        import makeAxesGrid
from ....utils.plotting.plot        import plot
from ....utils.plotting.plot        import plottingOptions
from ....utils.plotting.plot        import addTitleLabelsGrid
from ....utils.plotting.plot        import tryAddCustomLegend
from ....utils.plotting.plot        import addTimeTextPBar
from ....utils.plotting.plot        import adaptAxesExtent
from ....utils.plotting.saveFig     import saveFig
from ....utils.plotting.positions   import figureRect

def plotFinalStateMultiSim(outputDirList,
                           figDir,
                           prefixFigName,
                           labelList,
                           transparencyFunction,
                           addLegend,
                           grid,
                           addTimeTextPbar,
                           xLabel,
                           yLabel,
                           nbrXTicks,
                           nbrYTicks,
                           xTicksRound,
                           yTicksRound,
                           extensionsList,
                           EPSILON):

    (options, nModOptions)                  = plottingOptions()
    (fs, finits, ffinals, mini, maxi, Pmax) = extractFinalStateMultiSim(outputDirList)

    xmin   = 0.0
    xmax   = 1.0

    for t in xrange(Pmax+2):
        alphaInit  = transparencyFunction(1.-float(t)/(Pmax+1))
        alphaFinal = transparencyFunction(float(t)/(Pmax+1))

        figure     = plt.figure()
        plt.clf()

        (gs, axes) = makeAxesGrid(plt, len(outputDirList), order='horizontalFirst', extendDirection='vertical')

        for (f, finit, ffinal, label, ax) in zip(fs, finits, ffinals, labelList, axes):

            X  = np.linspace(xmin, xmax, finit.size)

            plot(ax, f[:,t], X, options[np.mod(0, nModOptions)], label=label+', $f$' )
            plot(ax, finit, X, options[np.mod(1, nModOptions)], label=label+', $f_{init}$', alpha=alphaInit)
            plot(ax, ffinal, X, options[np.mod(2, nModOptions)], label=label+', $f_{final}$', alpha=alphaFinal)

            adaptAxesExtent(ax, xmin, xmax, mini, maxi, 0.0, 0.05, nbrXTicks, nbrYTicks, xTicksRound, yTicksRound, EPSILON)
            addTitleLabelsGrid(ax, title=label, xLabel=xLabel, yLabel=yLabel, grid=grid)
            if addLegend:
                tryAddCustomLegend(ax)

        gs.tight_layout(figure, rect=figureRect(addColorBar=False, addTimeTextPBar=addTimeTextPbar))
        if addTimeTextPbar:
            addTimeTextPBar(plt, t, Pmax+1)

        figName = figDir + prefixFigName + fileNameSuffix(t, Pmax+2)
        saveFig(plt, figName, extensionsList)
        plt.close()

