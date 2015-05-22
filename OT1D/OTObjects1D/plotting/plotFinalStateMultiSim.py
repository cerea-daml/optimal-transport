###########################
# plotFinalStateMultiSim.py
###########################
#
# util to plot the final state for multiple simulations 
#

import numpy             as np
import cPickle           as pck
import matplotlib.pyplot as plt

from matplotlib        import gridspec
from scipy.interpolate import interp1d

from ...utils.io                  import fileNameSuffix
from ...utils.defaultTransparency import customTransparency
from ...utils.extent              import xExtentPP
from ...utils.extent              import extendY1d
from ...utils.extent              import extendY2d

def plotFinalStateMultiSim(outputDirList, figDir, prefixFigName='finalState', transpFun=None, swapInitFinal=None,
                           titlesList=None, options=None):
    
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
    Xs      = []
    finits  = []
    ffinals = []
    Plist   = []

    minis = []
    maxis = []

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

        Xs.append(xExtentPP, fstate.N)
        fs.append(extendY2d(f, axis=0, copy=False))

        minis.append(f.min())
        maxis.append(f.max())

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

            finits.append(extendY1d(finit, copy=False))
            ffinals.append(extendY1d(ffinal, copy=False))
            minis.append(finit.min())
            minis.append(ffinal.min())
            maxis.append(finit.max())
            maxis.append(ffinal.max())
            Plist.append(config.P)

    minis.append(0.0)
    maxis.append(0.0)
    Pmax = np.max(Plist)
    mini = np.min(minis)
    maxi = np.max(maxis)

    extend = maxi - mini + 1.e-6
    maxi += 0.05*extend
    mini -= 0.05*extend

    yPbar = mini-0.05*extend
    xTxt  = 0.01
    yTxt  = yPbar

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

    for t in xrange(Pmax+2):
        alphaInit  = transpFun(1.-float(t)/(Pmax+1))
        alphaFinal = transpFun(float(t)/(Pmax+1))

        figure = plt.figure()
        plt.clf()

        gs = gridspec.GridSpec(Nl, Nc)
        j = 0

        for (f,X,finit,ffinal,title) in zip(fs,Xs,finits,ffinals,titlesList):
            nc = int(np.mod(j,Nc))
            nl = int((j-nc)/Nc)
            ax = plt.subplot(gs[nl,nc])

            ax.plot( X,    finit,  options[0], label=lbl+'$f_{init}$',  alpha=alphaInit  )
            ax.plot( X,   ffinal, options[1], label=lbl+'$f_{final}$', alpha=alphaFinal )
            ax.plot( X, f[:,t], options[2], label=lbl+'$f$' )
            ax.set_ylim(mini,maxi)
            ax.set_xlim(0.0, 1.0)
            try:
                ax.legend(fontsize='xx-small',loc='center right',bbox_to_anchor=(1.13, 0.5),fancybox=True,framealpha=0.40)
            except:
                ax.legend(fontsize='xx-small',loc='center right',bbox_to_anchor=(1.13, 0.5),fancybox=True)

            ax.grid()
            ax.set_title(title)
            j += 1        

        gs.tight_layout(figure)
        figName = figDir + prefixFigName + fileNameSuffix(t,Pmax+2) + '.pdf'
        print('Writing '+figName+' ...')
        plt.savefig(figName)
        plt.close()

