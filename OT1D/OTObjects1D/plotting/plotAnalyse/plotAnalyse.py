################
# plotAnalyse.py
################
#
# plots the result of an analyse
#

import cPickle           as pck
import numpy             as np
import matplotlib.pyplot as plt

from matplotlib                  import gridspec

from ....utils.plotting.plot     import plot
from ....utils.plotting.plot     import plottingOptions
from ....utils.plotting.plot     import tryAddCustomLegend
from ....utils.plotting.plot     import makeAxesGrid
from ....utils.plotting.plot     import addTitleLabelsGrid
from ....utils.plotting.plot     import trySetScale
from ....utils.plotting.saveFig  import saveFig
from ....utils.io.extractAnalyse import extractAnalyse

def plotAnalyse(outputDir, figDir, prefixFigName, figSubFig, extensionsList):

    (options, nModOptions)                            = plottingOptions()
    (iterationNumbers, iterationTimes, names, values) = extractAnalyse(outputDir)

    N  = len(names)

    for (columnsList, xAxisList, xScaleList, yScaleList, xLabelList, yLabelList, titleList, gridList, fileNameSuffix) in figSubFig:

        nbrSubFig          = len(columnsList)
        figure             = plt.figure()
        plt.clf()

        (gs, axes)         = makeAxesGrid(plt, nbrSubFig, order='horizontalFirst', extendDirection='vertical')

        for (columns, xAxis, xScale, yScale, 
             xLabel, yLabel, title, grid, ax) in zip(columnsList, xAxisList, xScaleList, yScaleList, 
                                                     xLabelList, yLabelList, titleList, gridList, axes):

            addTitleLabelsGrid(ax, title, xLabel, yLabel, grid)

            if xAxis == 'iterations':
                X = iterationNumbers
            elif xAxis == 'time':
                X = iterationTimes

            nOptions = -1
            for column in columns:
                nOptions = np.mod(nOptions+1, nModOptions)
                column   = min(N-1, column)
                Y        = values[:, column]
                plot(ax, Y, X, options[nOptions], label=names[column])

            trySetScale(ax, xScale, yScale)
            tryAddCustomLegend(ax)

        gs.tight_layout(figure)
        figName = figDir + prefixFigName + fileNameSuffix
        saveFig(plt, figName, extensionsList)
        plt.close()


