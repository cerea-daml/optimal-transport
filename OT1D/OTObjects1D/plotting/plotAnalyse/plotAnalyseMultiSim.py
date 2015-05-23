################
# plotAnalyse.py
################
#
# plots the result of multiple analyses
#

import cPickle           as pck
import numpy             as np
import matplotlib.pyplot as plt

from matplotlib              import gridspec

from ....utils.plotting.plot import plot
from ....utils.plotting.plot import plottingOptionsMultiSim
from ....utils.plotting.plot import tryAddCustomLegend
from ....utils.io            import makeGrid

def plotAnalyseMultiSim(outputDirList, figDir, prefixFigName, labelsList, figSubFig, extensionsList):

    (options, mModOptions, nModOptions) = plottingOptionsMultiSim()
    
    iterNumbers = []
    iterTimes   = []
    names       = []
    values      = []

    for outputDir in outputDirList:
        fileAnalyse = outputDir + 'analyse.bin'
        f           = open(fileAnalyse, 'rb')
        p           = pck.Unpickler(f)
        iterNumbers.append(p.load())
        iterTimes.append(p.load())
        names.append(p.load())
        values.append(p.load())
        f.close()

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
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)

            mOptions = -1

            for (iter, times, name, values, label) in zip(iterNumbers, iterTimes, names, values, labelsList):
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
                    Y        = values[:, column]
                    plot(ax, Y, X, options[mOptions, nOptions], label=label+', '+names[column])

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


