###########################
# animFinalStateMultiSim.py
###########################
#
# util to animate the final state for multiple simulations 
#

import numpy as np
import cPickle as pck
from matplotlib import pyplot as plt
from matplotlib import animation as anim
from scipy.interpolate import interp1d

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

def animFinalStateMultiSim(outputDirList, figDir, figName='finalState.mp4', writer='ffmpeg', interval=100., transpFun=None,
                           swapInitFinal=None, titlesList=None, options=None):
    
    if swapInitFinal is None:
        swapInitFinal = []
        for i in xrange(len(outputDirList)):
            swapInitFinal.append(False)

    if titlesList is None:
        titlesList = []
        for i in xrange(len(outputDirList)):
            titlesList.append('sim '+str(i))

    if options is None:
        options = ['b-','r-','g-']

    if transpFun is None:
        transpFun = customTransparency

    fs      = []
    finits  = []
    ffinals = []
    Plist   = []

    minis   = []
    maxis   = []

    for (outputDir,swap) in zip(outputDirList,swapInitFinal):
        fileFinalState = outputDir + 'finalState.bin'
        f = open(fileFinalState,'rb')
        p = pck.Unpickler(f)
        fstate = p.load()
        f.close()

        if swap:
            f = fstate.f.copy()
            for t in xrange(fstate.P+2):
                f[:,t] = fstate.f[:,fstate.P+1-t]
        else:
            f = fstate.f

        fs.append( f )
        minis.append( f.min() )
        maxis.append( f.max() )
        fileConfig = outputDir + 'config.bin'
        f = open(fileConfig,'rb')
        p = pck.Unpickler(f)
        try:
            while True:
                config = p.load()
        except:
            f.close()

            if swap:
                finit = config.boundaries.temporalBoundaries.bt1
                ffinal = config.boundaries.temporalBoundaries.bt0
            else:
                finit = config.boundaries.temporalBoundaries.bt0
                ffinal = config.boundaries.temporalBoundaries.bt1
            finits.append( finit )
            ffinals.append( ffinal )
            minis.append( finit.min() )
            minis.append( ffinal.min() )
            maxis.append( finit.max() )
            maxis.append( ffinal.max() )
            Plist.append( config.P )

    mini  = np.min( minis )
    maxi  = np.max( maxis )
    Pmax  = np.max( Plist )

    extend = maxi - mini + 1.e-6
    maxi += 0.05*extend
    mini -= 0.05*extend

    nbrSubFig = len(outputDirList)
    Nc = int(np.floor(np.sqrt(nbrSubFig)))
    Nl = Nc
    while Nc*Nl < nbrSubFig:
        Nl += 1

    fsCorrected = []
    for (f,P) in zip(fs,Plist):
        if P < Pmax:
            interpF = interp1d( np.linspace( 0.0 , 1.0 , P+2 ) , f , axis = 1 )
            fsCorrected.append( interpF( np.linspace( 0.0 , 1.0 , Pmax+2 ) ) )
        else:
            fsCorrected.append( f )

    fs = fsCorrected

    alphaInit  = transpFun(1.)
    alphaFinal = transpFun(0.)

    figure = plt.figure()
    plt.clf()

    gs = gridspec.GridSpec(Nl, Nc)
    j = 0
    axes = []

    for (f,finit,ffinal,title) in zip(fs,finits,ffinals,titlesList):
        nc = int(np.mod(j,Nc))
        nl = int((j-nc)/Nc)

        ax = plt.subplot(gs[nl,nc])
        axes.append(ax)

        XInit    = np.linspace( 0.0 , 1.0 , finit.size  )
        XFinal   = np.linspace( 0.0 , 1.0 , ffinal.size )
        XCurrent = np.linspace( 0.0 , 1.0 , f[:,0].size ) 
        lineInit,    = ax.plot(XInit,finit,options[0],label='$f_{init}$',alpha=alphaInit)
        lineFinal,   = ax.plot(XFinal,ffinal,options[1],label='$f_{final}$',alpha=alphaFinal)
        lineCurrent, = ax.plot(XCurrent,f[:,0],options[2],label='$f$')

        try:
            ax.legend(fontsize='xx-small',loc='center right',bbox_to_anchor=(1.13, 0.5),fancybox=True,framealpha=0.40)
        except:
            ax.legend(fontsize='xx-small',loc='center right',bbox_to_anchor=(1.13, 0.5),fancybox=True)
        ax.set_ylim(mini-0.15*extend,maxi)
        ax.grid()

        ax.set_title(title)
        j += 1

    gs.tight_layout(figure)

    def animate(t):
        ret = []
        alphaInit  = transpFun(1.-float(t)/(Pmax+1.))
        alphaFinal = transpFun(float(t)/(Pmax+1.))

        for (f,finit,ffinal,title,ax) in zip(fs,finits,ffinals,titlesList,axes):
            ax.cla()

            XInit    = np.linspace( 0.0 , 1.0 , finit.size  )
            XFinal   = np.linspace( 0.0 , 1.0 , ffinal.size )
            XCurrent = np.linspace( 0.0 , 1.0 , f[:,t].size )

            lineInit,    = ax.plot(XInit,finit,options[0],label='$f_{init}$',alpha=alphaInit)
            lineFinal,   = ax.plot(XFinal,ffinal,options[1],label='$f_{final}$',alpha=alphaFinal)
            lineCurrent, = ax.plot(XCurrent,f[:,t],options[2],label='$f$')

            ret.extend([lineInit,lineFinal,lineCurrent])

            ax.set_ylim(mini-0.15*extend,maxi)
            ax.set_title(title)
            ax.grid()
            try:
                ax.legend(fontsize='xx-small',loc='center right',bbox_to_anchor=(1.13, 0.5),fancybox=True,framealpha=0.40)
            except:
                ax.legend(fontsize='xx-small',loc='center right',bbox_to_anchor=(1.13, 0.5),fancybox=True)

        return tuple(ret)

    def init():
        return animate(0)

    frames = np.arange(Pmax+2)
    
    print('Making animation ...')
    ani = anim.FuncAnimation(figure, animate, frames, init_func=init, interval=interval, blit=True)
    print('Writing '+figDir+figName+' ...')
    ani.save(figDir+figName,writer)

