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
from ....utils.plotting.plot     import makeGrid
from ....utils.plotting.saveFig  import saveFig
from ....utils.io.extractAnalyse import extractAnalyse

def plotAnalyse(outputDir, figDir, prefixFigName, figSubFig, extensionsList):

    (options, nModOptions)                            = plottingOptions()
    (iterationNumbers, iterationTimes, names, values) = extractAnalyse(outputDir)

    N  = len(names)

    for (columnsList, xAxisList, xScaleList, yScaleList, xLabelList, yLabelList, titleList, gridList, fileNameSuffix) in figSubFig:

        nbrSubFig          = len(columnsList)
        (nLines, nColumns) = makeGrid(nbrSubFig, extendDirection='vertical') 
        figure             = plt.figure()
        plt.clf()
        gs                 = gridspec.GridSpec(nLines, nColumns)
        j                  = -1

        for ( (columns, xAxis, xScale, yScale, xLabel, yLabel, title, grid) in 
              zip(columnsList, xAxisList, xScaleList, yScaleList, xLabelList, yLabelList, titleList, gridList) ):

            j += 1
            nc = int(np.mod(j,nColumns))
            nl = int((j-nColumns)/nColumns)
            ax = plt.subplot(gs[nl,nc])

            if grid:
                ax.grid()
            ax.set_title(title)
            ax.set_xlabel(xLabel)
            ax.set_ylabel(yLabel)

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

            try:
                ax.set_xscale(xScale)
                ax.set_yscale(yScale)
            except:
                pass

            tryAddCustomLegend(ax)

        gs.tight_layout(figure)
        figName = figDir + prefixFigName + fileNameSuffix
        saveFig(plt, figName, extensionsList)
        plt.close()


