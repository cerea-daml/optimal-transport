###################
# animFinalState.py
###################
#
# util to animate the final state 
#

import numpy                as np
import cPickle              as pck
import matplotlib.pyplot    as plt

from matplotlib.animation    import FuncAnimation

from ....utils.io.io                import fileNameSuffix
from ....utils.io.extractFinalState import extractFinalState
from ....utils.plotting.plot        import plot
from ....utils.plotting.plot        import plottingOptions
from ....utils.plotting.plot        import positions
from ....utils.plotting.plot        import tryAddCustomLegend

def makeAnimFinalState(outputDir, label, transpFun, kwargsFuncAnim, EPSILON):

    (options, nModOptions)            = plottingOptions()
    (f, finit, ffinal, mini, maxi, P) = extractFinalState(outputDir)
    (mini, maxi, xTxt, yTxt, xPbarStart, xPbarEnd, yPbar) = positions(0.0, 1.0, mini, maxi, EPSILON):

    X          = np.linspace(0.0, 1.0, finit.size)
    figure     = plt.figure()
    plt.clf()
    ax         = plt.subplot(111)

    def animate(t):
        alphaInit    = transpFun(1.-float(t)/(P+1.))
        alphaFinal   = transpFun(float(t)/(P+1.))
        ax.cla()

        ret          = plotTimeTextPBar(ax, t, P+1, xTxt, yTxt, xPbarStart, xPbarEnd, yPbar)

        lineCurrent, = plot(ax, f[:,t], X, options[np.mod(0, nModOptions)], label='$f$')
        lineInit,    = plot(ax, finit, X, options[np.mod(1, nModOptions)], label='$f_{init}$', alpha=alphaInit)
        lineFinal,   = plot(ax, ffinal, X, options[np.mod(2, nModOptions)], label='$f_{final}$', alpha=alphaFinal)
        ret.extend([lineInit,lineFinal,lineCurrent])

        ax.set_xlabel('$x$')
        ax.set_ylim(mini,maxi)
        ax.set_xlim(0.0, 1.0)
        ax.grid()
        
        tryAddCustomLegend(ax)
        ax.set_title(label+'\nt = ' + fileNameSuffix(t, P+2) + ' / '+str(P+1))
        
        return tuple(ret)

    def init():
        return animate(0)

    init()
    plt.tight_layout()
    frames = np.arange(P+2)
    print('Making animation ...')
    return FuncAnimation(figure, animate, frames, init_func=init, **kwargsFuncAnim)

