#__________________________________________________
#__________________________________________________

# Copyrigth 2016 A. Farchi and M. Bocquet
# CEREA, joint laboratory Ecole des Ponts ParisTech and EDF R&D

# Code for the paper: Using the Wasserstein distance to compare fields of pollutants:
# Application to the radionuclide atmospheric dispersion of the Fukushima-Daiichi accident
# by A. Farchi, M. Bocquet, Y. Roustan, A. Mathieu and A. Querel

#__________________________________________________

#__________________________________________________
#__________________________
# plotFinalStateMultiSim.py
#__________________________
#
# util to plot the final state for multiple simulations 
#

import numpy             as np
import matplotlib.pyplot as plt

from ....utils.io.io                import fileNameSuffix
from ....utils.io.extractFinalState import extractFinalStateMultiSim
from ....utils.plotting.plotting    import makeAxesGrid
from ....utils.plotting.plot        import plot
from ....utils.plotting.plotting    import plottingOptions
from ....utils.plotting.plot        import addTitleLabelsGrid
from ....utils.plotting.plot        import tryAddCustomLegend
from ....utils.plotting.plot        import addTimeTextPBar
from ....utils.plotting.plotting    import adaptAxesExtent
from ....utils.plotting.saveFig     import saveFig
from ....utils.plotting.positions   import figureRect

#__________________________________________________

def plotFinalStateMultiSim(outputDirList,
                           figDir,
                           prefixFigName,
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
                           extensionsList,
                           EPSILON):

    (options, nModOptions)                  = plottingOptions()
    (fs, finits, ffinals, mini, maxi, Pmax) = extractFinalStateMultiSim(outputDirList)

    xmin = 0.0
    xmax = 1.0

    for t in xrange(Pmax+2):
        alphaInit  = transparencyFunction(1.-float(t)/(Pmax+1))
        alphaFinal = transparencyFunction(float(t)/(Pmax+1))

        figure     = plt.figure()
        plt.clf()

        (gs, axes) = makeAxesGrid(plt, len(outputDirList), order=order, extendDirection=extendDirection)

        for (f, finit, ffinal, label, ax) in zip(fs, finits, ffinals, labelList, axes):

            X  = np.linspace(xmin, xmax, finit.size)

            plot(ax, f[:,t], X, options[np.mod(0, nModOptions)], label=label+', $f$' )
            plot(ax, finit, X, options[np.mod(1, nModOptions)], label=label+', $f_{init}$', alpha=alphaInit)
            plot(ax, ffinal, X, options[np.mod(2, nModOptions)], label=label+', $f_{final}$', alpha=alphaFinal)

            adaptAxesExtent(ax, xmin, xmax, mini, maxi, extendX, extendY, nbrXTicks, nbrYTicks, xTicksDecimals, yTicksDecimals, EPSILON)
            addTitleLabelsGrid(ax, label, xLabel, yLabel, grid)
            if legend:
                tryAddCustomLegend(ax, True)

        gs.tight_layout(figure, rect=figureRect(False, timeTextPBar))
        if timeTextPBar:
            addTimeTextPBar(plt, t, Pmax+1)

        figName = figDir + prefixFigName + fileNameSuffix(t, Pmax+2)
        saveFig(plt, figName, extensionsList)
        plt.close()

#__________________________________________________
