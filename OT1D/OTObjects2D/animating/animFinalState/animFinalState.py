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

from ....utils.io                   import fileNameSuffix
from ....utils.io.extractFinalState import extractFinalState

from ....utils.plotting.plot        import plot
from ....utils.plotting.plotMatrix  import plotMatrix
from ....utils.plotting.plotMatrix  import positions2d
from ....utils.plotting.plotMatrix  import addColorBar
from ....utils.plotting.saveFig     import saveFig

def makeAnimFinalState(outputDir, label, transpFun, kwargsFuncAnim, plotter,
                       kwargs, kwargsInit, kwargsFinal, EPSILON):

    (f, finit, ffinal, mini, maxi, P)    = extractFinalState(outputDir)
    (xmin, xmax, ymin, ymax, xTxt, yTxt,
     xPbarStart, xPbarEnd, yPbar)        = positions2d(0.0, 1.0, 0.0, 1.0, EPSILON)

    figure = plt.figure()
    plt.clf()
    ax     = plt.subplot(111)

    addColorBar(ax, mini, maxi)    
    
    def animate(t):
        ax.cla()
        kwargsInit['alpha']  = transpFun(1.-float(t)/(P+1.))
        kwargsFinal['alpha'] = transpFun(float(t)/(P+1.))
        ret                  = plotTimeTextPBar(ax, t, P+1, xTxt, yTxt, xPbarStart, xPbarEnd, yPbar)

        imC = plotMatrix(ax, f[:,:,t], plotter=plotter, vmin=mini, vmax=maxi, **kwargs)
        imI = plotMatrix(ax, finit, plotter='contour', vmin=mini, vmax=maxi, **kwargsInit)
        imF = plotMatrix(ax, ffinal, plotter='contour', vmin=mini, vmax=maxi, **kwargsFinal)
        
        ret.extend([imC,imI,imF])

        ax.set_xlabel('$x$')
        ax.set_ylabel('$y$')
        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)
        ax.set_title(label+'\nt = ' + fileNameSuffix(t,P+2) + ' / '+str(P+1))

        return tuple(ret)

    def init():
        return animate(0)

    init()
    plt.tight_layout()
    frames = np.arange(P+2)
    print('Making animation ...')
    return FuncAnimation(figure, animate, frames, init_func=init, **kwargsFuncAnim)
