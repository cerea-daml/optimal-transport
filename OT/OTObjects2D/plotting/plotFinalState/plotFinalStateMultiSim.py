#==================================================
#__________________________________________________

# Copyrigth 2016 A. Farchi and M. Bocquet
# CEREA, joint laboratory Ecole des Ponts ParisTech and EDF R&D

# Code for the paper: Using the Wasserstein distance to compare fields of pollutants:
# Application to the radionuclide atmospheric dispersion of the Fukushima-Daiichi accident
# by A. Farchi, M. Bocquet, Y. Roustan, A. Mathieu and A. Querel

#__________________________________________________
#==================================================

#__________________________
# plotFinalStateMultiSim.py
#__________________________
#
# util to plot the final state for multiple simulations 
#

import matplotlib.pyplot as plt

from ....utils.io.io                import fileNameSuffix
from ....utils.io.extractFinalState import extractFinalStateMultiSim
from ....utils.plotting.positions   import figureRect
from ....utils.plotting.positions   import xylims2d
from ....utils.plotting.plotting    import makeAxesGrid
from ....utils.plotting.plotting    import adaptAxesExtent
from ....utils.plotting.plot        import addTitleLabelsGrid
from ....utils.plotting.plot        import addTimeTextPBar
from ....utils.plotting.plotMatrix  import addColorBar
from ....utils.plotting.plotMatrix  import plotMatrix
from ....utils.plotting.plotMatrix  import filterKwargsMiniMaxiCmapName
from ....utils.plotting.saveFig     import saveFig

#__________________________________________________

def plotFinalStateMultiSim(outputDirList,
                           figDir,
                           prefixFigName,
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
                           extensionsList,
                           EPSILON):

    (fs, finits, ffinals, mini, maxi, Pmax) = extractFinalStateMultiSim(outputDirList)
    (xmin, xmax, ymin, ymax)                = xylims2d()
    (miniC, maxiC, cmapNameC, kwargs)       = filterKwargsMiniMaxiCmapName(mini, maxi, cmapName, **kwargs)
    (miniI, maxiI, cmapNameI, kwargsInit)   = filterKwargsMiniMaxiCmapName(mini, maxi, cmapName, **kwargsInit)
    (miniF, maxiF, cmapNameF, kwargsFinal)  = filterKwargsMiniMaxiCmapName(mini, maxi, cmapName, **kwargsFinal)

    for t in range(Pmax+2):
        kwargsInit['alpha']  = transparencyFunction(1.-float(t)/(Pmax+1.))
        kwargsFinal['alpha'] = transparencyFunction(float(t)/(Pmax+1.))

        figure     = plt.figure()
        plt.clf()

        (gs, axes) = makeAxesGrid(plt, len(outputDirList), order=order, extendDirection=extendDirection)

        for (f, finit, ffinal, label, ax) in zip(fs, finits, ffinals, labelList, axes):

            plotMatrix(ax,
                       f[:,:,t],
                       plotter=plotter,
                       xmin=xmin,
                       xmax=xmax,
                       ymin=ymin,
                       ymax=ymax,
                       cmapName=cmapNameC,
                       vmin=miniC,
                       vmax=maxiC,
                       **kwargs)
            plotMatrix(ax,
                       finit,
                       plotter='contour',
                       xmin=xmin,
                       xmax=xmax,
                       ymin=ymin,
                       ymax=ymax,
                       vmin=miniI,
                       vmax=maxiI,
                       **kwargsInit)
            plotMatrix(ax,
                       ffinal,
                       plotter='contour',
                       xmin=xmin,
                       xmax=xmax,
                       ymin=ymin,
                       ymax=ymax,
                       vmin=miniF,
                       vmax=maxiF,
                       **kwargsFinal)

            adaptAxesExtent(ax, xmin, xmax, ymin, ymax, extendX, extendY, nbrXTicks, nbrYTicks, xTicksDecimals, yTicksDecimals, EPSILON)
            addTitleLabelsGrid(ax, title=label, xLabel=xLabel, yLabel=yLabel, grid=False)

        gs.tight_layout(figure, rect=figureRect(colorBar, timeTextPBar))

        if colorBar:
            addColorBar(plt, timeTextPBar, cmapNameC, miniC, maxiC, nbrCTicks, cticksDecimals, cLabel)

        if timeTextPBar:
            addTimeTextPBar(plt, t, Pmax+1)

        figName = figDir + prefixFigName + fileNameSuffix(t,Pmax+2)
        saveFig(plt, figName, extensionsList)
        plt.close()

#__________________________________________________
