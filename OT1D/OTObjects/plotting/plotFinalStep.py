##################
# plotFinalStep.py
##################
#
# util to plot the final step 
#

import numpy as np
import pickle as pck
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

def plotFinalState(outputDir, figDir, prefixFigName='finalState', transpFun=None, options=None):

    if options is None:
        options = ['b-','r-','g-']

    if transpFun is None:
        transpFun = customTransparency

    fileFinalState = outputDir + 'finalState.bin'
    f = open(fileFinalState,'rb')
    p = pck.Unpickler(f)
    finalState = p.load().convergingStaggeredField()
    f.close()

    fileConfig = outputDir + 'config.bin'
    f = open(fileConfig,'rb')
    p = pck.Unpickler(f)
    try:
        while True:
            config = p.load()
    except:
        pass

    finit  = config.boundaries.temporalBoundaries.bt0
    ffinal = config.boundaries.temporalBoundaries.bt1

    mini = np.min( [ finit.min() , ffinal.min() , finalState.f.min() ] ) 
    maxi = np.max( [ finit.max() , ffinal.max() , finalState.f.max() ] ) 

    extend = maxi - mini + 1.e-6
    maxi += 0.05*extend
    mini -= 0.05*extend

    X = np.linspace( 0.0 , 1.0 , finalState.N + 1 )
    for t in xrange(finalState.P+2):
        alphaInit  = transpFun(1.-float(t)/(finalState.P+1.))
        alphaFinal = transpFun(float(t)/(finalState.P+1.))

        plt.figure()
        plt.clf()
        plt.plot(X,finit,options[0],label='$f_{init}$',alpha=alphaInit)
        plt.plot(X,ffinal,options[1],label='$f_{final}$',alpha=alphaFinal)
        plt.plot(X,finalState.f[:,t],options[2],label='$f$')
        plt.xlabel('$x$')
        plt.ylim(mini,maxi)
        plt.legend(fontsize='xx-small',loc='upper right',bbox_to_anchor=(1.1, 1.),bbox_transform=plt.gca().transAxes)
        plt.grid()

        plt.title('Final iteration\nt = ' + suffixFor(t,finalState.P+1) + ' / '+str(finalState.P+1))

        figName = figDir + prefixFigName + suffixFor(t,finalState.P+1) + '.pdf'
        print('Writing '+figName+' ...')
        plt.savefig(figName)

def animFinalState(outputDir, figDir, figName='finalState.mp4', writer='ffmpeg', interval=100., transpFun=None, options=None):
    if options is None:
        options = ['b-','r-','g-']

    if transpFun is None:
        transpFun = customTransparency

    fileFinalState = outputDir + 'finalState.bin'
    f = open(fileFinalState,'rb')
    p = pck.Unpickler(f)
    finalState = p.load().convergingStaggeredField()
    f.close()

    fileConfig = outputDir + 'config.bin'
    f = open(fileConfig,'rb')
    p = pck.Unpickler(f)
    try:
        while True:
            config = p.load()
    except:
        pass

    finit  = config.boundaries.temporalBoundaries.bt0
    ffinal = config.boundaries.temporalBoundaries.bt1

    mini = np.min( [ finit.min() , ffinal.min() , finalState.f.min() ] )
    maxi = np.max( [ finit.max() , ffinal.max() , finalState.f.max() ] )

    extend = maxi - mini + 1.e-6
    maxi += 0.05*extend
    mini -= 0.05*extend

    X = np.linspace( 0.0 , 1.0 , finalState.N + 1 )

    figure = plt.figure()
    plt.clf()

    yPbar = mini-0.05*extend
    lineBkgPbar, = plt.plot([0.,1.], [yPbar,yPbar], 'k-', linewidth=5)
    linePbar, = plt.plot([0.,0.], [yPbar,yPbar], 'g-', linewidth=5)

    xTxt = 0.01
    yTxt = mini-0.1*extend
    timeText = plt.text(xTxt, yTxt, suffixFor(0.,finalState.P+1)+' / '+str(finalState.P+1))

    lineInit, = plt.plot(X,finit,options[0],label='$f_{init}$',alpha=transpFun(1.))
    lineFinal, = plt.plot(X,ffinal,options[1],label='$f_{final}$',alpha=transpFun(0.))
    lineCurrent, = plt.plot(X,finalState.f[:,0],options[2],label='$f$')

    plt.xlabel('$x$')
    plt.ylim(mini-0.15*extend,maxi)
    plt.legend(fontsize='xx-small',loc='upper right',bbox_to_anchor=(1.1, 1.),bbox_transform=plt.gca().transAxes)
    plt.grid()

    plt.title('Final iteration')

    def animate(i):
        ret = []
        plt.clf()

        timeText = plt.text(xTxt, yTxt, suffixFor(i,finalState.P+1)+' / '+str(finalState.P+1))
        ret.append(timeText)

        lineBkgPbar, = plt.plot([float((0.+i)/(finalState.P+1.))*0.6+0.2,0.8],[yPbar,yPbar], 'k-', linewidth=5)
        linePbar, = plt.plot([0.2,float((0.+i)/(finalState.P+1.))*0.6+0.2],[yPbar,yPbar], 'g-', linewidth=5)
        ret.append(lineBkgPbar)
        ret.append(linePbar)

        lineInit, = plt.plot(X,finit,options[0],label='$f_{init}$',alpha=transpFun(1.-float(i)/(finalState.P+1.)))
        lineFinal, = plt.plot(X,ffinal,options[1],label='$f_{final}$',alpha=transpFun(float(i)/(finalState.P+1.)))
        lineCurrent, = plt.plot(X,finalState.f[:,i],options[2],label='$f$')
        ret.append(lineInit)
        ret.append(lineFinal)
        ret.append(lineCurrent)

        plt.xlabel('$x$')
        plt.ylim(mini-0.15*extend,maxi)
        plt.grid()
        plt.legend(fontsize='xx-small',loc='upper right',bbox_to_anchor=(1.1, 1.),bbox_transform=plt.gca().transAxes)
        plt.title('Final iteration')
        return tuple(ret)

    def init():
        return animate(0)

    frames = np.arange(finalState.P+2)
    
    print('Making animation ...')
    ani = anim.FuncAnimation(figure, animate, frames, init_func=init, interval=interval, blit=True)
    print('Writing '+figDir+figName+' ...')
    ani.save(figDir+figName,writer)

