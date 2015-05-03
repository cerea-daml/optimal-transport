################
# plotAnalyse.py
################
#
# plots the result of an analyse
#

import numpy as np
from matplotlib import pyplot as plt
import pickle as pck

def plotOneAnalyse(outputDir, figDir, prefixFig='analyse', figSubFig=None):

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
            figSubFig.append([ ( [i] , 'iterations' , 'log' , 'log' , 'iterations' , 'operators' , 'title' , True ) ] )

    i = 0
    for fig in figSubFig:

        nbrSubFig = len(fig)
        M = int(np.floor(np.sqrt(nbrSubFig)))
        P = M
        while M*P < nbrSubFig:
            P += 1

        figure = plt.figure()            
        plt.clf()

        j = 1
        for (columns, xaxis, xscale, yscale, xlabel, ylabel, title, grid) in fig: 
            ax = plt.subplot(P,M,j)
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
            ax.legend(fontsize='xx-small',loc='upper right',bbox_to_anchor=(1.1, 1.),bbox_transform=plt.gca().transAxes)
            j += 1

        figName = figDir + prefixFig + str(i) + '.pdf'
        print('Saving ' + figName + ' ...')
        plt.savefig(figName)
        i += 1

def plotAnalyseDefaultSubplots(outputDir, figDir, prefixFig='analyse', itOrTime='iterations'):

    figSubFig = [ [ ( [0] , itOrTime , 'log' , 'log' , itOrTime , '$div$' , 'Divergence constrain' , True ) ] ,
                  [ ( [1] , itOrTime , 'log' , 'log' , itOrTime , '$abs(min(.))$' , 'Positivity constrain' , True ) ] ,
                  [ ( [2,3,4,5,6] , itOrTime , 'log' , 'log' , itOrTime , '$J$' , 'Cost function' , True ) ] ,
                  [ ( [7] , itOrTime , 'log' , 'log' , itOrTime , '' , 'Convergence' , True ) ] ]

    
    plotOneAnalyse(outputDir, figDir, prefixFig, figSubFig)
