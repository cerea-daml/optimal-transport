################
# plotAnalyse.py
################
#
# plots the result of an analyse
#

import numpy as np
from matplotlib import pyplot as plt
import cPickle as pck

def plotAnalyse(outputDir, figDir, prefixFig='analyse', figSubFig=None):

    options = ['b-','g-','r-','m-','y-','c-','k-']
    nModOptions = len(options)

    fileAnalyse = outputDir + 'analyse.bin'
    f = open(fileAnalyse, 'rb')
    p = pck.Unpickler(f)
    iterationNumbers = p.load()
    iterationTimes = p.load()
    names = p.load()
    values = p.load()
    f.close()

    N  = len(names)

    if figSubFig is None:
        figSubFig = []
        for i in xrange(N):
            figSubFig.append([ ( [i] , 'iterations' , 'log' , 'log' , 'iterations' , 'operators' , 'title' , True , None ) ] )

    i = 0
    for fig in figSubFig:

        nbrSubFig = len(fig)
        Nc = int(np.floor(np.sqrt(nbrSubFig)))
        Nl = Nc
        while Nc*Nl < nbrSubFig:
            Nl += 1

        figure = plt.figure()#figsize=(10*Nl,10*Nc))            
        plt.clf()

        j = 1

        for (columns, xaxis, xscale, yscale, xlabel, ylabel, title, grid, suffix) in fig: 
            ax = plt.subplot(Nl,Nc,j)
            ax.set_xscale(xscale)
            ax.set_yscale(yscale)

            if grid:
                ax.grid()
            ax.set_title(title)
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)

            if xaxis == 'iterations':
                X = iterationNumbers
            elif xaxis == 'time':
                X = iterationTimes

            nOptions = 0
            for column in columns:
                column = min(N-1, column)
                Y = values[:,column]
                ax.plot(X,Y,options[nOptions],label=names[column])
                nOptions = np.mod(nOptions+1,nModOptions)
                
            from mpl_toolkits.axes_grid1 import make_axes_locatable
            divider = make_axes_locatable(ax)
            lax = divider.append_axes('right', '10%',frameon=False)
            lax.set_yticks([])
            lax.set_xticks([])

            try:
                ax.legend(fontsize='xx-small',loc='center right',bbox_to_anchor=(1.13, 0.5),fancybox=True,framealpha=0.40)
            except:
                ax.legend(fontsize='xx-small',loc='center right',bbox_to_anchor=(1.13, 0.5),fancybox=True)
            j += 1

        figure.tight_layout()
        if suffix is None:
            suffix = str(i)
        figName = figDir + prefixFig + suffix + '.pdf'
        print('Saving ' + figName + ' ...')
        plt.savefig(figName)
        i += 1

def plotAnalyseDefaultSubplots(outputDir, figDir, prefixFig='analyse', itOrTime='iterations'):

    figSubFig = [ [ ( [0] , itOrTime , 'log' , 'log' , itOrTime , '$div$' , 'Divergence constrain' , True , 'DivConstrain' ) ] ,
                  [ ( [1] , itOrTime , 'log' , 'log' , itOrTime , '$abs(min(.))$' , 'Positivity constrain' , True , 'PosConstrain' ) ] ,
                  [ ( [2] , itOrTime , 'log' , 'log' , itOrTime , '$J$' , 'Cost function' , True , 'J' ) ] ,
                  [ ( [2,3,4,5,6] , itOrTime , 'log' , 'log' , itOrTime , '$J$' , 'Cost function' , True , 'moreJ' ) ] ,
                  [ ( [7] , itOrTime , 'log' , 'log' , itOrTime , '' , 'Convergence' , True , 'Convergence' ) ] ]

    plotAnalyse(outputDir, figDir, prefixFig, figSubFig)

