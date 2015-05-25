###########################
# animFinalStateMultiSim.py
###########################
#
# util to animate the final state for multiple simulations 
#

import numpy                as np
import cPickle              as pck
import matplotlib.pyplot    as plt

from matplotlib           import gridspec
from matplotlib.animation import FuncAnimation
from scipy.interpolate    import interp1d

from ....utils.io            import fileNameSuffix
from ....utils.plotting.plot import plot
from ....utils.plotting.plot import plottingOptions
from ....utils.plotting.plot import positions
from ....utils.plotting.plot import tryAddCustomLegend

def makeAnimFinalStateMultiSim(outputDirList, labelsList, transpFun, kwargsFuncAnim, EPSILON):

    (options, n) = plottingOptions()

    fs           = []
    finits       = []
    ffinals      = []
    Plist        = []

    minis        = []
    maxis        = []

    for outputDir in outputDirList:
        fileConfig = outputDir + 'config.bin'
        f          = open(fileConfig,'rb')
        p          = pck.Unpickler(f)
        try:
            while True:
                config = p.load()
        except:
            f.close()

        fileFinalState = outputDir + 'finalState.bin'
        f              = open(fileFinalState,'rb')
        p              = pck.Unpickler(f)
        fstate         = p.load()
        f.close()

        if config.swappedInitFinal:
            finit  = config.boundaries.temporalBoundaries.bt1
            ffinal = config.boundaries.temporalBoundaries.bt0
            f      = np.zeros(shape=(config.N+1, config.P+2))
            for t in xrange(config.P+2):
                f[:, t] = fstate.f[:, config.P+1-t]
            else:
            finit  = config.boundaries.temporalBoundaries.bt0
            ffinal = config.boundaries.temporalBoundaries.bt1
            f      = fstate.f

        fs.append(f )
        finits.append(finit)
        ffinals.append(ffinal)

        minis.append(f.min())
        minis.append(finit.min())
        minis.append(ffinal.min())

        maxis.append(f.max())
        maxis.append(finit.max())
        maxis.append(ffinal.max())

        Plist.append(config.P)

    Pmax = np.max(Plist)
    mini = np.min(minis)
    maxi = np.max(maxis)

    (mini, maxi, xTxt, yTxt, xPbarStart, xPbarEnd, yPbar) = positions(0.0, 1.0, mini, maxi, EPSILON)
    (nLines, nColumns) = makeGrid(len(outputDirList), extendDirection='vertical')

    fsCorrected = []
    for (f,P) in zip(fs,Plist):
        if P < Pmax:
            interpF = interp1d(np.linspace(0.0, 1.0, P+2), f, axis = 1, copy=False, bounds_error=False, fill_value=0.0)
            fsCorrected.append(interpF(np.linspace(0.0, 1.0, Pmax+2)))
        else:
            fsCorrected.append(f)

    fs = fsCorrected

    figure = plt.figure()
    plt.clf()



    gs     = gridspec.GridSpec(Nl, Nc)
    j      = -1
    axes   = []

    for j in xrange(len(fs)):
        nc = int(np.mod(j,nColumns))
        nl = int((j-nColumns)/nColumns)
        axes.append(plt.subplot(gs[nl,nc]))

    def animate(t):
        ret = []
        alphaInit  = transpFun(1.-float(t)/(Pmax+1.))
        alphaFinal = transpFun(float(t)/(Pmax+1.))

        for (f,finit,ffinal,title,ax) in zip(fs,finits,ffinals,labelsList,axes):
            ax.cla()

            X  = np.linspace(0.0, 1.0, finit.size)

            lineCurrent, = plot(ax, f[:,t], X, options[np.mod(0, nModOptions)], label='$f$')
            lineInit,    = plot(ax, finit, X, options[np.mod(1, nModOptions)], label='$f_{init}$', alpha=alphaInit)
            lineFinal,   = plot(ax, ffinal, X, options[np.mod(2, nModOptions)], label='$f_{final}$', alpha=alphaFinal)
            ret.extend([lineInit,lineFinal,lineCurrent])

            ax.set_ylim(mini,maxi)
            ax.set_xlim(0.0, 1.0)
            ax.grid()

            tryAddCustomLegend(ax)
            ax.set_title(label+'\nt = ' + fileNameSuffix(t,config.P+2) + ' / '+str(config.P+1))

            ax.set_ylim(mini-0.15*extend,maxi)
            ax.set_title(title+'\nt = ' + fileNameSuffix(t,Pmax+2) + ' / '+str(Pmax+1))

        return tuple(ret)

    def init():
        return animate(0)

    init()
    gs.tight_layout(figure)
    frames = np.arange(Pmax+2)    
    print('Making animation ...')
    return FuncAnimation(figure, animate, frames, init_func=init, **kwargsFuncAnim)


