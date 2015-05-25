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

from ....utils.io            import fileNameSuffix
from ....utils.plotting.plot import plot
from ....utils.plotting.plot import plottingOptions
from ....utils.plotting.plot import positions
from ....utils.plotting.plot import tryAddCustomLegend

def makeAnimFinalState(outputDir, label, transpFun, kwargsFuncAnim, EPSILON):

    (options, nModOptions) = plottingOptions()

    fileFinalState = outputDir + 'finalState.bin'
    f              = open(fileFinalState,'rb')
    p              = pck.Unpickler(f)
    finalState     = p.load()
    f.close()

    fileConfig     = outputDir + 'config.bin'
    f              = open(fileConfig,'rb')
    p              = pck.Unpickler(f)
    try:
        while True:
            config = p.load()
    except:
        f.close()

    if config.swappedInitFinal:
        finit  = config.boundaries.temporalBoundaries.bt1
        ffinal = config.boundaries.temporalBoundaries.bt0
        f      = np.zeros(shape=(config.N+1,config.P+2))
        for t in xrange(config.P+2):
            f[:,t] = finalState.f[:,config.P+1-t]
    else:
        finit  = config.boundaries.temporalBoundaries.bt0
        ffinal = config.boundaries.temporalBoundaries.bt1
        f      = finalState.f

    
    mini       = np.min( [ finit.min() , ffinal.min() , f.min() ] )
    maxi       = np.max( [ finit.max() , ffinal.max() , f.max() ] )

    (mini, maxi, xTxt, yTxt, xPbarStart, xPbarEnd, yPbar) = positions(0.0, 1.0, mini, maxi, EPSILON):

    X          = np.linspace( 0.0 , 1.0 , config.N + 1 )
    figure     = plt.figure()
    plt.clf()
    ax         = plt.subplot(111)

    def animate(t):
        alphaInit    = transpFun(1.-float(t)/(config.P+1.))
        alphaFinal   = transpFun(float(t)/(config.P+1.))
        ax.cla()

        ret          = plotTimeTextPBar(ax, t, config.P+1, xTxt, yTxt, xPbarStart, xPbarEnd, yPbar)

        lineCurrent, = plot(ax, finalState.f[:,t], X, options[np.mod(0, nModOptions)], label='$f$')
        lineInit,    = plot(ax, finit, X, options[np.mod(1, nModOptions)], label='$f_{init}$', alpha=alphaInit)
        lineFinal,   = plot(ax, ffinal, X, options[np.mod(2, nModOptions)], label='$f_{final}$', alpha=alphaFinal)
        ret.extend([lineInit,lineFinal,lineCurrent])

        ax.set_xlabel('$x$')
        ax.set_ylim(mini,maxi)
        ax.set_xlim(0.0, 1.0)
        ax.grid()
        
        tryAddCustomLegend(ax)
        ax.set_title(label+'\nt = ' + fileNameSuffix(t,config.P+2) + ' / '+str(config.P+1))
        
        return tuple(ret)

    def init():
        return animate(0)

    init()
    plt.tight_layout()
    frames = np.arange(config.P+2)    
    print('Making animation ...')
    return FuncAnimation(figure, animate, frames, init_func=init, **kwargsFuncAnim)

