################
# plotAnalyse.py
################
#
# plots the result of an analyse
#

import cPickle           as pck
import numpy             as np
import matplotlib.pyplot as plt

from matplotlib              import gridspec

from ....utils.plotting.plot import plot
from ....utils.plotting.plot import plottingOptions
from ....utils.plotting.plot import tryAddCustomLegend
from ....utils.io            import makeGrid

def plotAnalyse(outputDir, figDir, prefixFigName, figSubFig, extensionsList):

    (options, nModOptions) = plottingOptions()

    fileAnalyse      = outputDir + 'analyse.bin'
    f                = open(fileAnalyse, 'rb')
    p                = pck.Unpickler(f)
    iterationNumbers = p.load()
    iterationTimes   = p.load()
    names            = p.load()
    values           = p.load()
    f.close()

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
        for ext in extensionsList:
            try:
                plt.savefig(figName+ext)
                print('Writing '+figName+ext+' ...')
            except:
                print('Could not write '+figName+ext+' ...')

        plt.close()


