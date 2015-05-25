##########################
# plotFinalStateMuliSim.py
##########################
#
# util to plot the final state for multiple simulations 
#

import numpy                as np
import cPickle              as pck
import matplotlib.pyplot    as plt

from matplotlib              import gridspec
from matplotlib.animation    import FuncAnimation

from ....utils.io                   import fileNameSuffix
from ....utils.io.extractFinalState import extractFinalState

from ....utils.plotting.plot        import plot
from ....utils.plotting.plotMatrix  import plotMatrix
from ....utils.plotting.plotMatrix  import positions2d
from ....utils.plotting.plotMatrix  import addColorBarMultiSim
from ....utils.plotting.saveFig     import saveFig

def makeAnimFinalStateMultiSim(outputDirList, labelsList, transpFun, kwargsFuncAnim, plotter,
                               kwargs, kwargsInit, kwargsFinal, EPSILON):

    (fs, finits, ffinals, mini, maxi, Pmax) = extractFinalStateMultiSim(outputDirList)
    (xmin, xmax, ymin, ymax, xTxt, yTxt,
     xPbarStart, xPbarEnd, yPbar)           = positions2d(0.0, 1.0, 0.0, 1.0, EPSILON)
    (nLines, nColumns)                      = makeGrid(len(outputDirList), extendDirection='vertical')

    figure = plt.figure()
    plt.clf()

    gs     = gridspec.GridSpec(Nl, Nc)
    j      = -1
    axes   = []

    for j in xrange(len(fs)):
        nc = int(np.mod(j,nColumns))
        nl = int((j-nColumns)/nColumns)
        axes.append(plt.subplot(gs[nl,nc]))

    def animate(t):
        ret = []
        kwargsInit['alpha']  = transpFun(1.-float(t)/(Pmax+1.))
        kwargsFinal['alpha'] = transpFun(float(t)/(Pmax+1.))

        for (f, finit, ffinal, label, ax) in zip(fs, finits, ffinals, labelsList, axes):
            ax.cla()

            imC = plotMatrix(ax, f[:,:,t], plotter=plotter, vmin=mini, vmax=maxi, **kwargs)
            imI = plotMatrix(ax, finit, plotter='contour', vmin=mini, vmax=maxi, **kwargsInit)
            imF = plotMatrix(ax, ffinal, plotter='contour', vmin=mini, vmax=maxi, **kwargsFinal)
            ret.extend([imC,imI,imF])

            ax.set_yticks([])
            ax.set_xticks([])
            ax.set_xlim(xmin, xmax)
            ax.set_ylim(ymin, ymax)

            ax.set_title(title+'\nt = ' + fileNameSuffix(t,Pmax+2) + ' / '+str(Pmax+1))

            ax.set_title(title)
        return tuple(ret)

    def init():
        return animate(0)

    init()

    gs.tight_layout(figure, rect=[0.,0.,0.85,1.])
    gs2 = gridspec.GridSpec(1,1)
    gs2.update(left=0.87, right=0.93)
    cax = plt.subplot(gs2[0,0], frameon=False)
    addColorBarMultiSim(cax, mini, maxi)

    frames = np.arange(Pmax+2)

    print('Making animation ...')
    return FuncAnimation(figure, animate, frames, init_func=init, **kwargsFuncAnim)
