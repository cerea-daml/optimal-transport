###########################
# animFinalStateMultiSim.py
###########################
#
# util to animate the final state for multiple simulations 
#

import numpy                as np
import cPickle              as pck
import matplotlib.pyplot    as plt

from matplotlib           import gridspec
from matplotlib.animation import FuncAnimation
from scipy.interpolate    import interp1d

from ....utils.io.io                import fileNameSuffix
from ....utils.io.extractFinalState import extractFinalStateMultiSim
from ....utils.plotting.plot        import plot
from ....utils.plotting.plot        import plottingOptions
from ....utils.plotting.plot        import positions
from ....utils.plotting.plot        import tryAddCustomLegend

def makeAnimFinalStateMultiSim(outputDirList, labelsList, transpFun, kwargsFuncAnim, EPSILON):

    (options, n)                            = plottingOptions()
    (fs, finits, ffinals, mini, maxi, Pmax) = extractFinalStateMultiSim(outputDirList)
    (mini, maxi, xTxt, yTxt, xPbarStart, xPbarEnd, yPbar) = positions(0.0, 1.0, mini, maxi, EPSILON)
    (nLines, nColumns) = makeGrid(len(outputDirList), extendDirection='vertical')

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
        alphaInit  = transpFun(1.-float(t)/(Pmax+1.))
        alphaFinal = transpFun(float(t)/(Pmax+1.))

        for (f,finit,ffinal,title,ax) in zip(fs,finits,ffinals,labelsList,axes):
            ax.cla()

            X  = np.linspace(0.0, 1.0, finit.size)

            lineCurrent, = plot(ax, f[:,t], X, options[np.mod(0, nModOptions)], label='$f$')
            lineInit,    = plot(ax, finit, X, options[np.mod(1, nModOptions)], label='$f_{init}$', alpha=alphaInit)
            lineFinal,   = plot(ax, ffinal, X, options[np.mod(2, nModOptions)], label='$f_{final}$', alpha=alphaFinal)
            ret.extend([lineInit,lineFinal,lineCurrent])

            ax.set_ylim(mini,maxi)
            ax.set_xlim(0.0, 1.0)
            ax.grid()

            tryAddCustomLegend(ax)
            ax.set_title(title+'\nt = ' + fileNameSuffix(t,Pmax+2) + ' / '+str(Pmax+1))

        return tuple(ret)

    def init():
        return animate(0)

    init()
    gs.tight_layout(figure)
    frames = np.arange(Pmax+2)    
    print('Making animation ...')
    return FuncAnimation(figure, animate, frames, init_func=init, **kwargsFuncAnim)


