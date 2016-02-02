################
# plotAnalyse.py
################
#
# plots the result of multiple analyses
#

import numpy             as np
import matplotlib.pyplot as plt

from ....utils.plotting.plot     import plot
from ....utils.plotting.plotting import plottingOptionsMultiSim
from ....utils.plotting.plot     import tryAddCustomLegend
from ....utils.plotting.plotting import makeAxesGrid
from ....utils.plotting.plot     import addTitleLabelsGrid
from ....utils.plotting.plot     import trySetScale
from ....utils.plotting.saveFig  import saveFig
from ....utils.io.extractAnalyse import extractAnalyseMultiSim

def plotAnalyseMultiSim(outputDirList, figDir, prefixFigName, labelList, figSubFig, extensionsList):

    (options, mModOptions, nModOptions)     = plottingOptionsMultiSim()
    (iterNumbers, iterTimes, names, values) = extractAnalyseMultiSim(outputDirList)

    for (columnsList, xAxisList, xScaleList, yScaleList, xLabelList, yLabelList, titleList, gridList, fileNameSuffix) in figSubFig:

        nbrSubFig          = len(columnsList)
        figure             = plt.figure()
        plt.clf()
        (gs, axes)         = makeAxesGrid(plt, nbrSubFig, order='horizontalFirst', extendDirection='vertical')

        for (columns, xAxis, xScale, yScale, 
             xLabel, yLabel, title, grid, ax) in zip(columnsList, xAxisList, xScaleList, yScaleList, xLabelList, 
                                                     yLabelList, titleList, gridList, axes):

            addTitleLabelsGrid(ax, title, xLabel, yLabel, grid)

            mOptions = -1
            for (iter, times, name, value, label) in zip(iterNumbers, iterTimes, names, values, labelList):
                mOptions = np.mod(mOptions+1, mModOptions)
                if xAxis == 'iterations':
                    X = iter
                elif xAxis == 'time':
                    X = times

                N = len(name)
                nOptions = -1
                for column in columns:
                    nOptions = np.mod(nOptions+1, nModOptions)
                    column   = min(N-1, column)
                    Y        = value[:, column]
                    plot(ax, Y, X, options[mOptions, nOptions], label=label+', '+name[column])

            trySetScale(ax, xScale, yScale)
            tryAddCustomLegend(ax, True)

        gs.tight_layout(figure)
        figName = figDir + prefixFigName + fileNameSuffix
        saveFig(plt, figName, extensionsList)
        plt.close()
