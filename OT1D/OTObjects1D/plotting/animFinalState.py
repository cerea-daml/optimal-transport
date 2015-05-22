###################
# animFinalState.py
###################
#
# util to animate the final state 
#

import numpy                as np
import cPickle              as pck
import matplotlib.pyplot    as plt
import matplotlib.animation as anim

from ...utils.io                  import fileNameSuffix
from ...utils.defaultTransparency import customTransparency
from ...utils.extent              import xExtentPP
from ...utils.extent              import extendY1d
from ...utils.extent              import extendY2d
from ...utils.plot                import plot

def animFinalState(outputDir, figDir, figName='finalState.mp4', writer='ffmpeg', interval=100., transpFun=None, options=None, swapInitFinal=False):

    if options is None:
        options = ['b-','r-','g-']

    if transpFun is None:
        transpFun = customTransparency

    fileFinalState = outputDir + 'finalState.bin'
    f = open(fileFinalState,'rb')
    p = pck.Unpickler(f)
    finalState = p.load()
    f.close()

    fileConfig = outputDir + 'config.bin'
    f = open(fileConfig,'rb')
    p = pck.Unpickler(f)
    try:
        while True:
            config = p.load()
    except:
        f.close()

    if swapInitFinal:
        finit  = config.boundaries.temporalBoundaries.bt1
        ffinal = config.boundaries.temporalBoundaries.bt0
        f      = finalState.f.copy()
        for t in xrange(config.P+2):
            f[:,t] = finalState.f[:,config.P+1-t]
    else:
        finit  = config.boundaries.temporalBoundaries.bt0
        ffinal = config.boundaries.temporalBoundaries.bt1
        f      = finalState.f

    finit  = extendY1d(finit, copy=False)
    ffinal = extendY1d(ffinal, copy=False)
    f      = extendY2d(f, axis=0, copy=False)
    X      = xExtentPP(config.N)

    mini   = np.min( [ finit.min() , ffinal.min() , f.min() ] )
    maxi   = np.max( [ finit.max() , ffinal.max() , f.max() ] )
    extend = maxi - mini + 1.e-6

    yPbar  = mini-0.05*extend
    xTxt   = 0.01
    yTxt   = yPbar

    maxi  += 0.1*extend
    mini  -= 0.1*extend

    figure = plt.figure()
    plt.clf()
    ax = plt.subplot(111)

    alphaInit  = transpFun(1.)
    alphaFinal = transpFun(0.)

    lineBkgPbar, = plot(ax, [yPbar,yPbar], [0.2,0.8], 'k-', linewidth=5)
    timeText     = ax.text(xTxt, yTxt, fileNameSuffix(0.,config.P+2)+' / '+str(config.P+1))

    lineInit,    = plot(ax, finit, X, options[0], label='$f_{init}$', alpha=alphaInit)
    lineFinal,   = plot(ax, ffinal, X, options[1], label='$f_{final}$', alpha=alphaFinal)
    lineCurrent, = plot(ax, finalState.f[:,0], X, options[2], label='$f$')

    ax.set_xlabel('$x$')
    ax.set_ylim(mini-0.15*extend,maxi)
    ax.set_xlim(0.0,1.0)
    ax.grid()

    try:
        ax.legend(fontsize='xx-small',loc='center right',bbox_to_anchor=(1.13, 0.5),fancybox=True,framealpha=0.40)
    except:
        ax.legend(fontsize='xx-small',loc='center right',bbox_to_anchor=(1.13, 0.5),fancybox=True)            

    ax.set_title('Final iteration\nt = ' + fileNameSuffix(0,config.P+2) + ' / '+str(config.P+1))

    def animate(t):
        ret = []
        alphaInit  = transpFun(1.-float(t)/(config.P+1.))
        alphaFinal = transpFun(float(t)/(config.P+1.))
        ax.cla()

        timeText     = ax.text(xTxt, yTxt, fileNameSuffix(t,config.P+2)+' / '+str(config.P+1))
        ret.append(timeText)
        if t < config.P + 1:
            lineBkgPbar, = plot(ax, [yPbar,yPbar], [float(t)/(config.P+1.)*0.6+0.2,0.8], 'k-', linewidth=5)
            ret.append(lineBkgPbar)
        if t > 0:
            linePbar,    = plot(ax, [yPbar,yPbar], [0.2,float(t)/(config.P+1.)*0.6+0.2], 'g-', linewidth=5)
            ret.append(linePbar)

        lineInit,    = plot(ax, finit, X, options[0], label='$f_{init}$', alpha=alphaInit)
        lineFinal,   = plot(ax, ffinal, X, options[1], label='$f_{final}$', alpha=alphaFinal)
        lineCurrent, = plot(ax, finalState.f[:,t], X, options[2], label='$f$')

        ret.extend([lineInit,lineFinal,lineCurrent])

        ax.set_xlabel('$x$')
        ax.set_ylim(mini,maxi)
        ax.set_xlim(0.0,1.0)
        ax.set_title('Final iteration\nt = ' + fileNameSuffix(t,config.P+2) + ' / '+str(config.P+1))
        ax.grid()
        try:
            ax.legend(fontsize='xx-small',loc='center right',bbox_to_anchor=(1.13, 0.5),fancybox=True,framealpha=0.40)
        except:
            ax.legend(fontsize='xx-small',loc='center right',bbox_to_anchor=(1.13, 0.5),fancybox=True)
        return tuple(ret)

    def init():
        return animate(0)

    frames = np.arange(config.P+2)
    
    print('Making animation ...')
    ani = anim.FuncAnimation(figure, animate, frames, init_func=init, interval=interval, blit=True)
    print('Writing '+figDir+figName+' ...')
    ani.save(figDir+figName,writer)

