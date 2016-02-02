#_____________________________
# triplotFinalStateMultiSim.py
#_____________________________
#
# util to plot the final state for multiple simulations 
#

import matplotlib.pyplot as plt

from ....utils.io.io                import fileNameSuffix
from ....utils.io.extractFinalState import extractFinalStateMultiSim
from ....utils.plotting.positions   import figureRect
from ....utils.plotting.positions   import xylims2d
from ....utils.plotting.plotting    import makeAxesGridTriplot
from ....utils.plotting.plotting    import adaptAxesExtent
from ....utils.plotting.plot        import addTitleLabelsGrid
from ....utils.plotting.plot        import addTimeTextPBar
from ....utils.plotting.plotMatrix  import addColorBar
from ....utils.plotting.plotMatrix  import plotMatrix
from ....utils.plotting.plotMatrix  import filterKwargsMiniMaxiCmapName
from ....utils.plotting.saveFig     import saveFig

#__________________________________________________

def triplotFinalStateMultiSim(outputDirList,
                              figDir,
                              prefixFigName,
                              labelList,
                              plotter,
                              kwargs,
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
                              extendDirectionTriplot,
                              extensionsList,
                              EPSILON):

    (fs, finits, ffinals, mini, maxi, Pmax) = extractFinalStateMultiSim(outputDirList)
    (xmin, xmax, ymin, ymax)                = xylims2d()
    (miniC, maxiC, cmapNameC, kwargs)       = filterKwargsMiniMaxiCmapName(mini, maxi, cmapName, **kwargs)


    for t in xrange(Pmax+2):

        figure     = plt.figure()
        plt.clf()

        (gs, axes, axesInit, axesFinal) = makeAxesGridTriplot(plt, len(outputDirList), order, extendDirection, extendDirectionTriplot)

        for (f, finit, ffinal, label, ax, axInit, axFinal) in zip(fs, finits, ffinals, labelList, axes, axesInit, axesFinal):

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
            plotMatrix(axInit,
                       finit,
                       plotter=plotter,
                       xmin=xmin,
                       xmax=xmax,
                       ymin=ymin,
                       ymax=ymax,
                       cmapName=cmapNameC,
                       vmin=miniC,
                       vmax=maxiC,
                       **kwargs)
            plotMatrix(axFinal,
                       ffinal,
                       plotter=plotter,
                       xmin=xmin,
                       xmax=xmax,
                       ymin=ymin,
                       ymax=ymax,
                       cmapName=cmapNameC,
                       vmin=miniC,
                       vmax=maxiC,
                       **kwargs)

            adaptAxesExtent(ax, xmin, xmax, ymin, ymax, extendX, extendY, nbrXTicks, nbrYTicks, xTicksDecimals, yTicksDecimals, EPSILON)
            addTitleLabelsGrid(ax, title=label, xLabel=xLabel, yLabel=yLabel, grid=False)

            adaptAxesExtent(axInit, xmin, xmax, ymin, ymax, extendX, extendY, nbrXTicks, nbrYTicks, xTicksDecimals, yTicksDecimals, EPSILON)
            addTitleLabelsGrid(axInit, title=label+', init', xLabel=xLabel, yLabel=yLabel, grid=False)

            adaptAxesExtent(axFinal, xmin, xmax, ymin, ymax, extendX, extendY, nbrXTicks, nbrYTicks, xTicksDecimals, yTicksDecimals, EPSILON)
            addTitleLabelsGrid(axFinal, title=label+', final', xLabel=xLabel, yLabel=yLabel, grid=False)

        gs.tight_layout(figure, rect=figureRect(colorBar, timeTextPBar))

        if colorBar:
            addColorBar(plt, timeTextPBar, cmapNameC, miniC, maxiC, nbrCTicks, cticksDecimals, cLabel)

        if timeTextPBar:
            addTimeTextPBar(plt, t, Pmax+1)

        figName = figDir + prefixFigName + fileNameSuffix(t,Pmax+2)
        saveFig(plt, figName, extensionsList)
        plt.close()

#__________________________________________________
