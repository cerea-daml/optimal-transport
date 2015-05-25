###################
# plotFinalState.py
###################
#
# util to plot the final state 
#

import numpy             as np
import cPickle           as pck
import matplotlib.pyplot as plt

from ....utils.io                   import fileNameSuffix
from ....utils.io.extractFinalState import extractFinalState

from ....utils.plotting.plot        import plot
from ....utils.plotting.plotMatrix  import plotMatrix 
from ....utils.plotting.plotMatrix  import positions2d
from ....utils.plotting.plotMatrix  import addColorBar
from ....utils.plotting.saveFig     import saveFig

def plotFinalState(outputDir, figDir, prefixFigName, label, transpFun, extensionsList, plotter, 
                   kwargs, kwargsInit, kwargsFinal, EPSILON):

    (f, finit, ffinal, mini, maxi, P)    = extractFinalState(outputDir)
    (xmin, xmax, ymin, ymax, xTxt, yTxt,
     xPbarStart, xPbarEnd, yPbar)        = positions2d(0.0, 1.0, 0.0, 1.0, EPSILON)

    for t in xrange(P+2):
        kwargsInit['alpha']  = transpFun(1.-float(t)/(P+1.))
        kwargsFinal['alpha'] = transpFun(float(t)/(P+1.))

        figure     = plt.figure()
        plt.clf()
        ax         = plt.subplot(111)

        plotTimeTextPBar(ax, t, P+1, xTxt, yTxt, xPbarStart, xPbarEnd, yPbar)

        plotMatrix(ax, f[:,:,t], plotter=plotter, vmin=mini, vmax=maxi, **kwargs)
        plotMatrix(ax, finit, plotter='contour', vmin=mini, vmax=maxi, **kwargsInit)
        plotMatrix(ax, ffinal, plotter='contour', vmin=mini, vmax=maxi, **kwargsFinal)
        
        ax.set_xlabel('$x$')
        ax.set_ylabel('$y$')

        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)

        addColorBar(ax, mini, maxi)

        ax.set_title(label+'\nt = ' + fileNameSuffix(t,P+2) + ' / '+str(P+1))
        plt.tight_layout()

        figName = figDir + prefixFigName + fileNameSuffix(t,P+2)
        saveFig(plt, figName, extensionsList)
        plt.close()
