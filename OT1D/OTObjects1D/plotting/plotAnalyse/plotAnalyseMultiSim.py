################
# plotAnalyse.py
################
#
# plots the result of multiple analyses
#

import numpy as np
from matplotlib import pyplot as plt
import cPickle as pck

def plotAnalyseMultiSim(outputDirList, figDir, prefixFig='analyse', labelsList=None, figSubFig=None):

    options = ['b-', 'g-', 'r-', 'm-', 'y-', 'c-', 'k-',
               'b--','g--','r--','m--','y--','c--','k--',
               'b:', 'g:', 'r:', 'm:', 'y:', 'c:', 'k:' ]

    nModOptions = len(options)

    numbers = []
    times   = []
    values  = []
    for outputDir in outputDirList:
        fileAnalyse = outputDir + 'analyse.bin'
        f = open(fileAnalyse, 'rb')
        p = pck.Unpickler(f)
        numbers.append(p.load())
        times.append(p.load())
        names = p.load()
        values.append(p.load())
        f.close()

    N  = len(names)

    if labelsList is None:
        labelsList = []
        for i in xrange(len(outputDirList)):
            labelsList.append('sim '+str(i))

    if figSubFig is None:
        figSubFig = []
        for i in xrange(N):
            figSubFig.append([ ( [i] , 'iterations' , 'log' , 'log' , 'iterations' , 'operators' , 'title' , True , None ) ] )

    i = 0
    for fig in figSubFig:

        nbrSubFig = len(fig)
        Nc = int(np.floor(np.sqrt(nbrSubFig)))
        Nl = Nc
        while Nl*Nc < nbrSubFig:
            Nl += 1

        figure = plt.figure()            
        plt.clf()

        j = 1
        suffix = None
        for (columns, xaxis, xscale, yscale, xlabel, ylabel, title, grid, suffix) in fig: 
            ax = plt.subplot(Nl,Nc,j)
            ax.set_xscale(xscale)
            ax.set_yscale(yscale)

            if grid:
                ax.grid()
            ax.set_title(title)
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)

            nOptions = 0
            for value,it,t,label in zip(values,numbers,times,labelsList):
                if xaxis == 'iterations':
                    X = it
                elif xaxis == 'time':
                    X = t

                for column in columns:
                    column = min(N-1, column)
                    Y = value[:,column]
                    ax.plot(X,Y,options[nOptions],label=label+', '+names[column])
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

def plotAnalyseMultiSimDefaultSubplots(outputDirList, figDir, prefixFig='analyse', itOrTime='iterations', labelsList=None):

    figSubFig = [ [ ( [0] , itOrTime , 'log' , 'log' , itOrTime , '$div$' , 'Divergence constrain' , True , 'DivConstrain' ) ] ,
                  [ ( [1] , itOrTime , 'log' , 'log' , itOrTime , '$abs(min(.))$' , 'Positivity constrain' , True , 'PosConstrain' ) ] ,
                  [ ( [2] , itOrTime , 'log' , 'log' , itOrTime , '$J$' , 'Cost function' , True , 'J' ) ] ,
                  [ ( [2,3,4,5,6] , itOrTime , 'log' , 'log' , itOrTime , '$J$' , 'Cost function' , True , 'moreJ' ) ] ,
                  [ ( [7] , itOrTime , 'log' , 'log' , itOrTime , '' , 'Convergence' , True , 'Convergence' ) ] ]
    
    plotAnalyseMultiSim(outputDirList, figDir, prefixFig, labelsList, figSubFig)

def plotAnalyseMultiSimDefaultSubplots2(outputDirList, figDir, prefixFig='analyse', itOrTime='iterations', labelsList=None):

    figSubFig = [ [ ( [0] , itOrTime , 'log' , 'log' , itOrTime , '$div$' , 'Divergence constrain' , True , 'DivConstrain' ) ,
                    ( [1] , itOrTime , 'log' , 'log' , itOrTime , '$abs(min(.))$' , 'Positivity constrain' , True , 'PosConstrain' ) ] ,
                  [ ( [2] , itOrTime , 'log' , 'log' , itOrTime , '$J$' , 'Cost function' , True , 'J' ) ] ,
                  [ ( [2] , itOrTime , 'log' , 'log' , itOrTime , '$J$' , 'Cost function' , True , 'moreJ' ) ,
                    ( [2,3,4,5,6] , itOrTime , 'log' , 'log' , itOrTime , '$J$' , 'Cost function' , True , 'moreJ' ) ] ,
                  [ ( [7] , itOrTime , 'log' , 'log' , itOrTime , '' , 'Convergence' , True , 'Convergence' ) ] ]
    
    plotAnalyseMultiSim(outputDirList, figDir, prefixFig, labelsList, figSubFig)
