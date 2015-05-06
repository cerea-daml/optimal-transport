##########################
# plotFinalStepMultiSim.py
##########################
#
# util to plot the final step for multiple simulations 
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

def plotFinalStateMultiSim(outputDirList, figDir, prefixFigName='finalState', transpFun=None, labelsList=None, options=None):
    
    if labelsList is None:
        labelsList = []
        for i in xrange(len(outputDirList)):
            labelsList.append('sim '+str(i)+', ')

    if options is None:
        options = ['b-','r-','g-']

    if transpFun is None:
        transpFun = customTransparency

    finalStates = []
    finits = []
    ffinals = []

    minis = []
    maxis = []

    for outputDir in outputDirList:
        fileFinalState = outputDir + 'finalState.bin'
        f = open(fileFinalState,'rb')
        p = pck.Unpickler(f)
        fstate = p.load()
        finalStates.append( fstate )
        minis.append( fstate.f.min() )
        maxis.append( fstate.f.max() )
        f.close()

        fileConfig = outputDir + 'config.bin'
        f = open(fileConfig,'rb')
        p = pck.Unpickler(f)
        try:
            while True:
                config = p.load()
        except:
            f.close()
            finit = config.boundaries.temporalBoundaries.bt0
            ffinal = config.boundaries.temporalBoundaries.bt1
            finits.append( finit )
            ffinals.append( ffinal )
            minis.append( finit.min() )
            minis.append( ffinal.min() )
            maxis.append( finit.max() )
            maxis.append( ffinal.max() )


    mini = np.min( minis )
    maxi = np.max( maxis )

    extend = maxi - mini + 1.e-6
    maxi += 0.05*extend
    mini -= 0.05*extend

    nbrSubFig = len(outputDirList)
    M = int(np.floor(np.sqrt(nbrSubFig)))
    P = M
    while M*P < nbrSubFig:
        P += 1

    Tmax = finalStates[0].P + 1
    for finalState in finalStates:
        Tmax = max( Tmax , finalState.P + 1 ) 

    for t in xrange(Tmax+1):
        alphaInit  = transpFun(1.-float(t)/(Tmax))
        alphaFinal = transpFun(float(t)/(Tmax))

        plt.figure()
        plt.clf()

        j = 1
        for (finit,ffinal,finalState,lbl) in zip(finits,ffinals,finalStates,labelsList):
            if finalState.P + 2 > t:
                X = np.linspace(0.0,1.0,finalState.N+1)

                ax = plt.subplot(P,M,j)
                ax.plot(X,finit,options[0],label=lbl+'$f_{init}$',alpha=alphaInit)
                ax.plot(X,ffinal,options[1],label=lbl+'$f_{final}$',alpha=alphaFinal)
                ax.plot(X,finalState.f[:,t],options[2],label=lbl+'$f$')
                ax.set_ylim(mini,maxi)
                ax.legend(fontsize='xx-small',loc='upper right',bbox_to_anchor=(1.1, 1.),bbox_transform=plt.gca().transAxes)
                ax.grid()
                j += 1        

        plt.suptitle('Final iteration\nt = ' + suffixFor(t,Tmax) + ' / '+str(Tmax))
        figName = figDir + prefixFigName + suffixFor(t,Tmax) + '.pdf'
        print('Writing '+figName+' ...')
        plt.savefig(figName)
        plt.close()


def animFinalStateMultiSim(outputDirList, figDir, figName='finalState.mp4', writer='ffmpeg', interval=100., transpFun=None, labelsList=None, options=None):

    if labelsList is None:
        labelsList = []
        for i in xrange(len(outputDirList)):
            labelsList.append('sim '+str(i)+', ')

    if options is None:
        options = ['b-','r-','g-']

    if transpFun is None:
        transpFun = customTransparency

    finalStates = []
    finits = []
    ffinals = []

    minis = []
    maxis = []

    for outputDir in outputDirList:
        fileFinalState = outputDir + 'finalState.bin'
        f = open(fileFinalState,'rb')
        p = pck.Unpickler(f)
        fstate = p.load()
        finalStates.append( fstate )
        minis.append( fstate.f.min() )
        maxis.append( fstate.f.max() )
        f.close()

        fileConfig = outputDir + 'config.bin'
        f = open(fileConfig,'rb')
        p = pck.Unpickler(f)
        try:
            while True:
                config = p.load()
        except:
            f.close()
            finit = config.boundaries.temporalBoundaries.bt0
            ffinal = config.boundaries.temporalBoundaries.bt1
            finits.append( finit )
            ffinals.append( ffinal )
            minis.append( finit.min() )
            minis.append( ffinal.min() )
            maxis.append( finit.max() )
            maxis.append( ffinal.max() )


    mini = np.min( minis )
    maxi = np.max( maxis )

    extend = maxi - mini + 1.e-6
    maxi += 0.05*extend
    mini -= 0.05*extend

    nbrSubFig = len(outputDirList)
    M = int(np.floor(np.sqrt(nbrSubFig)))
    P = M
    while M*P < nbrSubFig:
        P += 1

    Tmax = finalStates[0].P + 1
    for finalState in finalStates:
        Tmax = max( Tmax , finalState.P + 1 ) 

    figure = plt.figure()
    plt.clf()

    yPbar = mini-0.05*extend

    xTxt = 0.01
    yTxt = mini-0.1*extend

    plt.title('Final iteration')

    def animate(t):
        ret = []
        plt.clf()

        alphaInit  = transpFun(1.-float(t)/(Tmax))
        alphaFinal = transpFun(float(t)/(Tmax))


        j = 1
        for (finit,ffinal,finalState,lbl) in zip(finits,ffinals,finalStates,labelsList):
            if finalState.P + 2 > t:
                X = np.linspace(0.0,1.0,finalState.N+1)

                ax = plt.subplot(P,M,j)
                lineInit, = ax.plot(X,finit,options[0],label=lbl+'$f_{init}$',alpha=alphaInit)
                lineFinal, = ax.plot(X,ffinal,options[1],label=lbl+'$f_{final}$',alpha=alphaFinal)
                lineCurrent, = ax.plot(X,finalState.f[:,t],options[2],label=lbl+'$f$')

                ret.append(lineInit)
                ret.append(lineFinal)
                ret.append(lineCurrent)

                ax.set_ylim(mini-0.15*extend,maxi)
                ax.legend(fontsize='xx-small',loc='upper right',bbox_to_anchor=(1.1, 1.),bbox_transform=plt.gca().transAxes)
                ax.grid()

                timeText = ax.text(xTxt, yTxt, suffixFor(t,finalState.P+1)+' / '+str(finalState.P+1))
                ret.append(timeText)
                lineBkgPbar, = ax.plot([float((0.+t)/(finalState.P+1.))*0.6+0.2,0.8],[yPbar,yPbar], 'k-', linewidth=5)
                linePbar, = ax.plot([0.2,float((0.+t)/(finalState.P+1.))*0.6+0.2],[yPbar,yPbar], 'g-', linewidth=5)
                ret.append(lineBkgPbar)
                ret.append(linePbar)
                j += 1        

        plt.suptitle('Final iteration')
        return tuple(ret)

    def init():
        return animate(0)

    frames = np.arange(Tmax+1)
    
    print('Making animation ...')
    ani = anim.FuncAnimation(figure, animate, frames, init_func=init, interval=interval, blit=True)
    print('Writing '+figDir+figName+' ...')
    ani.save(figDir+figName,writer)

