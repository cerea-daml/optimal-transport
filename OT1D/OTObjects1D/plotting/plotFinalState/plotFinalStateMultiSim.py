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
from ....utils.plotting.plot        import makeGrid
from ....utils.plotting.plot        import plot
from ....utils.plotting.plot        import plottingOptions
from ....utils.plotting.plot        import positions
from ....utils.plotting.plot        import tryAddCustomLegend

def plotFinalStateMultiSim(outputDirList, figDir, prefixFigName, labelsList, transpFun, extensionsList, EPSILON):

    (options, n)                            = plottingOptions()
    (fs, finits, ffinals, mini, maxi, Pmax) = extractFinalStateMultiSim(outputDirList)
    (mini, maxi, xTxt, yTxt, xPbarStart, xPbarEnd, yPbar) = positions(0.0, 1.0, mini, maxi, EPSILON)
    (nLines, nColumns) = makeGrid(len(outputDirList), extendDirection='vertical')

    for t in xrange(Pmax+2):
        alphaInit  = transpFun(1.-float(t)/(Pmax+1))
        alphaFinal = transpFun(float(t)/(Pmax+1))

        figure     = plt.figure()
        plt.clf()

        gs         = gridspec.GridSpec(nLines, nColumns)
        j          = -1

        for (f, finit, ffinal, title) in zip(fs, finits, ffinals, labelsList):
            j += 1
            nc = int(np.mod(j,nColumns))
            nl = int((j-nColumns)/nColumns)
            ax = plt.subplot(gs[nl,nc])

            X  = np.linspace(0.0, 1.0, finit.size)

            plot(ax, f[:,t], X, options[np.mod(0, nModOptions)], label=lbl+'$f$' )
            plot(ax, finit, X, options[np.mod(1, nModOptions)], label=lbl+'$f_{init}$', alpha=alphaInit)
            plot(ax, ffinal, X, options[np.mod(2, nModOptions)], label=lbl+'$f_{final}$', alpha=alphaFinal)

            ax.set_ylim(mini,maxi)
            ax.set_xlim(0.0, 1.0)
            ax.grid()
            ax.set_title(title+'\nt = ' + fileNameSuffix(t,Pmax+2) + ' / '+str(Pmax+1))
            tryAddCustomLegend(ax)

        gs.tight_layout(figure)

        figName = figDir + prefixFigName + fileNameSuffix(t, Pmax+2)
        saveFig(plt, figName, extensionsList)
        plt.close()


