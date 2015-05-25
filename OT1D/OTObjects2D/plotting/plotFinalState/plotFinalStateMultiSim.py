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

from ....utils.io                   import fileNameSuffix
from ....utils.io.extractFinalState import extractFinalStateMultiSim
from ....utils.plotting.plot        import makeGrid
from ....utils.plotting.plot        import plot
from ....utils.plotting.plotMatrix  import plotMatrix
from ....utils.plotting.plotMatrix  import positions2d
from ....utils.plotting.plotMatrix  import addColorBarMultiSim
from ....utils.plotting.saveFig     import saveFig

def plotFinalStateMultiSim(outputDirList, figDir, prefixFigName, labelsList, transpFun, extensionsList, plotter, 
                           kwargs, kwargsInit, kwargsFinal, EPSILON):

    (fs,finits,ffinals, mini, maxi, Pmax) = extractFinalStateMultiSim(outputDirList)
    (xmin, xmax, ymin, ymax, xTxt, yTxt, 
     xPbarStart, xPbarEnd, yPbar)         = positions2d(0.0, 1.0, 0.0, 1.0, EPSILON)
    (nLines, nColumns)                    = makeGrid(len(outputDirList), extendDirection='vertical')


    for t in xrange(Pmax+2):
        kwargsInit['alpha']  = transpFun(1.-float(t)/(Pmax+1.))
        kwargsFinal['alpha'] = transpFun(float(t)/(Pmax+1.))

        figure     = plt.figure()
        plt.clf()

        gs         = gridspec.GridSpec(nLines, nColumns)
        j          = -1

        for (f, finit, ffinal, title) in zip(fs, finits, ffinals, labelsList):
            j += 1
            nc = int(np.mod(j,nColumns))
            nl = int((j-nColumns)/nColumns)
            ax = plt.subplot(gs[nl,nc])

            plotMatrix(ax, f[:,:,t], plotter=plotter, vmin=mini, vmax=maxi, **kwargs)
            plotMatrix(ax, finit, plotter='contour', vmin=mini, vmax=maxi, **kwargsInit)
            plotMatrix(ax, ffinal, plotter='contour', vmin=mini, vmax=maxi, **kwargsFinal)

            ax.set_yticks([])
            ax.set_xticks([])
            ax.set_xlim(xmin, xmax)
            ax.set_ylim(ymin, ymax)

            ax.set_title(title+'\nt = ' + fileNameSuffix(t,Pmax+2) + ' / '+str(Pmax+1))

        gs.tight_layout(figure, rect=[0.,0.,0.85,1.])
        gs2 = gridspec.GridSpec(1,1)
        gs2.update(left=0.87, right=0.93)
        cax = plt.subplot(gs2[0,0], frameon=False)
        addColorBarMultiSim(cax, mini, maxi)

        figName = figDir + prefixFigName + fileNameSuffix(t,Pmax+2)
        saveFig(plt, figName, extensionsList)
        plt.close()
