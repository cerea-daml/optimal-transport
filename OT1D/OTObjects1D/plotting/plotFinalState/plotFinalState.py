###################
# plotFinalState.py
###################
#
# util to plot the final state 
#

import numpy             as np
import cPickle           as pck
import matplotlib.pyplot as plt

from ....utils.io.io                import fileNameSuffix
from ....utils.io.extractFinalState import extractFinalState
from ....utils.plotting.plot        import plot
from ....utils.plotting.plot        import plotTimeTextPBar
from ....utils.plotting.plot        import plottingOptions
from ....utils.plotting.plot        import positions  
from ....utils.plotting.plot        import tryAddCustomLegend
from ....utils.plotting.saveFig     import saveFig

def plotFinalState(outputDir, figDir, prefixFigName, label, transpFun, extensionsList, EPSILON):

    (options, nModOptions)            = plottingOptions()
    (f, finit, ffinal, mini, maxi, P) = extractFinalState(outputDir)
    (mini, maxi, xTxt, yTxt, xPbarStart, xPbarEnd, yPbar) = positions(0.0, 1.0, mini, maxi, EPSILON)
    X = np.linspace(0.0, 1.0, finit.size)

    for t in xrange(P+2):
        alphaInit  = transpFun(1.-float(t)/(P+1.))
        alphaFinal = transpFun(float(t)/(P+1.))

        figure     = plt.figure()
        plt.clf()
        ax         = plt.subplot(111)

        plotTimeTextPBar(ax, t, P+1, xTxt, yTxt, xPbarStart, xPbarEnd, yPbar)
        plot(ax, f[:,t], X, options[np.mod(0, nModOptions)], label='$f$')
        plot(ax, finit, X, options[np.mod(1, nModOptions)], label='$f_{init}$', alpha=alphaInit)
        plot(ax, ffinal, X, options[np.mod(2, nModOptions)], label='$f_{final}$', alpha=alphaFinal)
        
        ax.set_xlabel('$x$')
        ax.set_ylim(mini, maxi)
        ax.set_xlim(0.0, 1.0)
        ax.grid()

        tryAddCustomLegend(ax)

        ax.set_title(label+'\nt = ' + fileNameSuffix(t, P+2) + ' / '+str(P+1))
        plt.tight_layout()

        figName = figDir + prefixFigName + fileNameSuffix(t, P+2)
        saveFig(plt, figName, extensionsList)
        plt.close()
