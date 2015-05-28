###########################
# plotFinalStateMultiSim.py
###########################
#
# util to plot the final state for multiple simulations 
#

import matplotlib.pyplot as plt

from ....utils.io.io                import fileNameSuffix
from ....utils.io.extractFinalState import extractFinalStateMultiSim
from ....utils.plotting.positions   import figureRect
from ....utils.plotting.plot        import makeAxesGrid
from ....utils.plotting.plot        import adaptAxesExtent
from ....utils.plotting.plot        import addTitleLabelsGrid
from ....utils.plotting.plot        import addTimeTextPBar
from ....utils.plotting.plotMatrix  import addColorBar
from ....utils.plotting.plotMatrix  import plotMatrix
from ....utils.plotting.saveFig     import saveFig

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
                           xTicksRound,
                           yTicksRound,
                           cticksRound,
                           order,
                           extendDirection,
                           extensionsList,
                           EPSILON):

    (fs, finits, ffinals, mini, maxi, Pmax) = extractFinalStateMultiSim(outputDirList)

    xmin = 0.0
    xmax = 1.0

    ymin = 0.0
    ymax = 1.0

    for t in xrange(Pmax+2):
        kwargsInit['alpha']  = transparencyFunction(1.-float(t)/(Pmax+1.))
        kwargsFinal['alpha'] = transparencyFunction(float(t)/(Pmax+1.))

        figure     = plt.figure()
        plt.clf()

        (gs, axes) = makeAxesGrid(plt, len(outputDirList), order=order, extendDirection=extendDirection)

        for (f, finit, ffinal, label, ax) in zip(fs, finits, ffinals, labelList, axes):

            plotMatrix(ax, f[:,:,t], plotter=plotter, vmin=mini, vmax=maxi, **kwargs)
            plotMatrix(ax, finit, plotter='contour', vmin=mini, vmax=maxi, **kwargsInit)
            plotMatrix(ax, ffinal, plotter='contour', vmin=mini, vmax=maxi, **kwargsFinal)

            adaptAxesExtent(ax, xmin, xmax, ymin, ymax, extendX, extendY, nbrXTicks, nbrYTicks, xTicksRound, yTicksRound, EPSILON)
            addTitleLabelsGrid(ax, title=label, xLabel=xLabel, yLabel=yLabel, grid=False)

        gs.tight_layout(figure, rect=figureRect(colorBar, timeTextPBar))

        if colorBar:
            addColorBar(plt, timeTextPBar, cmapName, mini, maxi, nbrCTicks, cticksRound, cLabel)

        if timeTextPBar:
            addTimeTextPBar(plt, t, Pmax+1)

        figName = figDir + prefixFigName + fileNameSuffix(t,Pmax+2)
        saveFig(plt, figName, extensionsList)
        plt.close()
