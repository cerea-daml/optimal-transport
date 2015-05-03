##################
# plotFinalStep.py
##################
#
# util to plot the final step 
#

import numpy as np
import pickle as pck
from matplotlib import pyplot as plt

def suffixFor(i,iMaxP1):
    nDigit = np.ceil(np.log10(iMaxP1))
    s = str(int(i))
    while len(s) < nDigit:
        s = '0'+s
    return s

def makeFrames(max_f, DT, dt_min=50.):
    EPS = 1.e-6
    frames = np.arange(max_f+1)
    dt = DT/(max_f+1.)

    if dt < dt_min-EPS:
        print 'Warning : dt < dt_min'
        dt = dt_min
        Nf = np.floor(DT/dt)
        frames = np.floor(np.linspace(0,max_f,Nf)).astype(int)
    return frames, dt

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
        plt.figure()
        plt.clf()
        plt.plot(X,finit,options[0],label='$f_{init}$')
        plt.plot(X,ffinal,options[1],label='$f_{final}$')
        plt.plot(X,finalState.f[:,t],options[2],label='$f$')
        plt.xlabel('$x$')
        plt.ylim(mini,maxi)
        plt.legend(fontsize='xx-small',loc='upper right',bbox_to_anchor=(1.1, 1.),bbox_transform=plt.gca().transAxes)
        plt.grid()

        plt.title('Final iteration\nt = ' + suffixFor(t,finalState.P+1) + ' / '+str(finalState.P+1))

        figName = figDir + prefixFigName + suffixFor(t,finalState.P+1) + '.pdf'
        print('Writing '+figName+' ...')
        plt.savefig(figName)
