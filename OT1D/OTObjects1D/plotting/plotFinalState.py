###################
# plotFinalState.py
###################
#
# util to plot the final state 
#

import numpy             as np
import cPickle           as pck
import matplotlib.pyplot as plt

from ...utils.io                  import fileNameSuffix
from ...utils.defaultTransparency import customTransparency

def plotFinalState(outputDir, figDir, prefixFigName='finalState', transpFun=None, options=None, swapInitFinal=False):

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

    yPbar = mini-0.05*extend
    xTxt  = 0.01
    yTxt  = yPbar

    maxi += 0.1*extend
    mini -= 0.1*extend


    X = np.linspace( 0.0 , 1.0 , config.N + 1 )

    for t in xrange(config.P+2):
        alphaInit  = transpFun(1.-float(t)/(finalState.P+1.))
        alphaFinal = transpFun(float(t)/(finalState.P+1.))

        plt.figure()
        plt.clf()
        ax = plt.subplot(111)

        timeText     = ax.text(xTxt, yTxt, fileNameSuffix(t,config.P+2)+' / '+str(config.P+1))
        if t < config.P + 1:
            lineBkgPbar, = ax.plot([float((0.+t)/(finalState.P+1.))*0.6+0.2,0.8],[yPbar,yPbar], 'k-', linewidth=5)
        if t > 0:
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

        ax.set_title('Final iteration\nt = ' + fileNameSuffix(t,config.P+2) + ' / '+str(config.P+1))
        plt.tight_layout()

        figName = figDir + prefixFigName + fileNameSuffix(t,finalState.P+2) + '.pdf'
        print('Writing '+figName+' ...')
        plt.savefig(figName)
