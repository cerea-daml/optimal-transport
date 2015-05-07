###################
# plotFinalState.py
###################
#
# util to plot the final state 
#

import numpy as np
import cPickle as pck
from matplotlib import pyplot as plt
from matplotlib import animation as anim

def suffixFor(i,iMaxP1):
    nDigit = np.ceil(np.log10(iMaxP1))
    s = str(int(i))
    while len(s) < nDigit:
        s = '0'+s
    return s

def defaultTransparency(t):
    return t

def fastVanishingTransparency(t):
    if t < 0.6:
        return 0.
    else:
        return 1. + (1./0.4)*(t-1.)

def customTransparency(t):
    return max(t,0.25)

def plotFinalState(outputDir, figDir, prefixFigName='finalState', transpFun=None, options=None, swapInitFinal=False,):

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

    mini = np.min( [ finit.min() , ffinal.min() , f.min() ] ) 
    maxi = np.max( [ finit.max() , ffinal.max() , f.max() ] ) 

    extend = maxi - mini + 1.e-6
    maxi += 0.05*extend
    mini -= 0.05*extend

    yPbar = mini-0.05*extend
    xTxt  = 0.01
    yTxt  = yPbar

    X = np.linspace( 0.0 , 1.0 , config.N + 1 )

    for t in xrange(config.P+2):
        alphaInit  = transpFun(1.-float(t)/(finalState.P+1.))
        alphaFinal = transpFun(float(t)/(finalState.P+1.))

        plt.figure()
        plt.clf()
        ax = plt.subplot(111)

        timeText     = ax.text(xTxt, yTxt, suffixFor(t,config.P+1)+' / '+str(config.P+1))
        lineBkgPbar, = ax.plot([float((0.+t)/(finalState.P+1.))*0.6+0.2,0.8],[yPbar,yPbar], 'k-', linewidth=5)
        linePbar,    = ax.plot([0.2,float((0.+t)/(finalState.P+1.))*0.6+0.2],[yPbar,yPbar], 'g-', linewidth=5)

        ax.plot(X,finit,options[0],label='$f_{init}$',alpha=alphaInit)
        ax.plot(X,ffinal,options[1],label='$f_{final}$',alpha=alphaFinal)
        ax.plot(X,finalState.f[:,t],options[2],label='$f$')
        
        ax.set_xlabel('$x$')
        ax.set_ylim(mini,maxi)
        ax.grid()

        try:
            ax.legend(fontsize='xx-small',loc='center right',bbox_to_anchor=(1.13, 0.5),fancybox=True,framealpha=0.40)
        except:
            ax.legend(fontsize='xx-small',loc='center right',bbox_to_anchor=(1.13, 0.5),fancybox=True)            

        ax.set_title('Final iteration\nt = ' + suffixFor(t,config.P+1) + ' / '+str(config.P+1))
        plt.tight_layout()

        figName = figDir + prefixFigName + suffixFor(t,finalState.P+1) + '.pdf'
        print('Writing '+figName+' ...')
        plt.savefig(figName)

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

    mini = np.min( [ finit.min() , ffinal.min() , f.min() ] )
    maxi = np.max( [ finit.max() , ffinal.max() , f.max() ] )

    extend = maxi - mini + 1.e-6
    maxi += 0.05*extend
    mini -= 0.05*extend

    yPbar = mini-0.05*extend
    xTxt  = 0.01
    yTxt  = yPbar

    X = np.linspace( 0.0 , 1.0 , config.N + 1 )

    figure = plt.figure()
    plt.clf()
    ax = plt.subplot(111)

    alphaInit  = transpFun(1.)
    alphaFinal = transpFun(0.)

    lineBkgPbar, = ax.plot([0.2,0.8], [yPbar,yPbar], 'k-', linewidth=5)
    linePbar,    = ax.plot([0.2,0.2], [yPbar,yPbar], 'g-', linewidth=5)
    timeText     = ax.text(xTxt, yTxt, suffixFor(0.,config.P+1)+' / '+str(config.P+1))

    lineInit,    = ax.plot(X,finit,options[0],label='$f_{init}$',alpha=alphaInit)
    lineFinal,   = ax.plot(X,ffinal,options[1],label='$f_{final}$',alpha=alphaFinal)
    lineCurrent, = ax.plot(X,finalState.f[:,0],options[2],label='$f$')

    ax.set_xlabel('$x$')
    ax.set_ylim(mini-0.15*extend,maxi)
    ax.grid()

    try:
        ax.legend(fontsize='xx-small',loc='center right',bbox_to_anchor=(1.13, 0.5),fancybox=True,framealpha=0.40)
    except:
        ax.legend(fontsize='xx-small',loc='center right',bbox_to_anchor=(1.13, 0.5),fancybox=True)            

    ax.set_title('Final iteration\nt = ' + suffixFor(0,config.P+1) + ' / '+str(config.P+1))

    def animate(i):
        ret = []
        alphaInit  = transpFun(1.-float(t)/(config.P+1.))
        alphaFinal = transpFun(float(t)/(config.P+1.))
        ax.cla()

        timeText     = ax.text(xTxt, yTxt, suffixFor(t,config.P+1)+' / '+str(config.P+1))
        lineBkgPbar, = ax.plot([float((0.+t)/(finalState.P+1.))*0.6+0.2,0.8],[yPbar,yPbar], 'k-', linewidth=5)
        linePbar,    = ax.plot([0.2,float((0.+t)/(finalState.P+1.))*0.6+0.2],[yPbar,yPbar], 'g-', linewidth=5)

        ret.extend([timeText,lineBkgPbar,linePbar])


        lineInit,    = ax.plot(X,finit,options[0],label='$f_{init}$',alpha=alphaInit)
        lineFinal,   = ax.plot(X,ffinal,options[1],label='$f_{final}$',alpha=alphaFinal)
        lineCurrent, = ax.plot(X,finalState.f[:,i],options[2],label='$f$')

        ret.extend([lineInit,lineFinal,lineCurrent])

        ax.set_xlabel('$x$')
        ax.set_ylim(mini-0.15*extend,maxi)
        ax.set_title('Final iteration\nt = ' + suffixFor(t,config.P+1) + ' / '+str(config.P+1))
        ax.grid()
        try:
            ax.legend(fontsize='xx-small',loc='center right',bbox_to_anchor=(1.13, 0.5),fancybox=True,framealpha=0.40)
        except:
            ax.legend(fontsize='xx-small',loc='center right',bbox_to_anchor=(1.13, 0.5),fancybox=True)
        return tuple(ret)

    def init():
        return animate(0)

    frames = np.arange(finalState.P+2)
    
    print('Making animation ...')
    ani = anim.FuncAnimation(figure, animate, frames, init_func=init, interval=interval, blit=True)
    print('Writing '+figDir+figName+' ...')
    ani.save(figDir+figName,writer)

