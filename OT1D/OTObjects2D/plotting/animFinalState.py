###################
# animFinalState.py
###################
#
# util to animate the final state 
#

import numpy                as np
import cPickle              as pck
import matplotlib           as mpl
import matplotlib.pyplot    as plt
import matplotlib.animation as anim

from mpl_toolkits.axes_grid1 import make_axes_locatable

from ...utils.io                  import fileNameSuffix
from ...utils.defaultTransparency import customTransparency
from ...utils.plotMatrix          import plotMatrix
from ...utils.plot                import plot

def animFinalState(outputDir, figDir, figName='finalState.mp4', writer='ffmpeg', interval=100., transpFun=None, plotter='imshow', swapInitFinal=False,
                   kwargsCurrent={}, kwargsInit={}, kwargsFinal={}):

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
            f[:,:,t] = finalState.f[:,:,config.P+1-t]
    else:
        finit  = config.boundaries.temporalBoundaries.bt0
        ffinal = config.boundaries.temporalBoundaries.bt1
        f      = finalState.f

    mini = np.min( [ finit.min() , ffinal.min() , f.min() ] ) 
    maxi = np.max( [ finit.max() , ffinal.max() , f.max() ] ) 

    xTxt  = 0.01
    yTxt  = -0.05
    yPbar = -0.05

    if not kwargsCurrent.has_key('origin'):
        kwargsCurrent['origin'] = 'lower'
    if not kwargsCurrent.has_key('extent'):
        kwargsCurrent['extent'] = [0.,1.,0.,1.]
    if not kwargsCurrent.has_key('vmin'):
        kwargsCurrent['vmin'] = mini
    if not kwargsCurrent.has_key('vmax'):
        kwargsCurrent['vmax'] = maxi
    if not kwargsCurrent.has_key('interpolation'):
        kwargsCurrent['interpolation'] = 'nearest'

    if not kwargsInit.has_key('origin'):
        kwargsInit['origin'] = 'lower'
    if not kwargsInit.has_key('extent'):
        kwargsInit['extent'] = [0.,1.,0.,1.]
    if not kwargsInit.has_key('vmin'):
        kwargsInit['vmin'] = mini
    if not kwargsInit.has_key('vmax'):
        kwargsInit['vmax'] = maxi
    if not kwargsInit.has_key('colors'):
        kwargsInit['colors'] = 'k'
    if not kwargsInit.has_key('linestyles'):
        kwargsInit['linestyles'] = 'solid'
    if not kwargsInit.has_key('linewidths'):
        kwargsInit['linewidths'] = 1.5
    
    if not kwargsFinal.has_key('origin'):
        kwargsFinal['origin'] = 'lower'
    if not kwargsFinal.has_key('extent'):
        kwargsFinal['extent'] = [0.,1.,0.,1.]
    if not kwargsFinal.has_key('vmin'):
        kwargsFinal['vmin'] = mini
    if not kwargsFinal.has_key('vmax'):
        kwargsFinal['vmax'] = maxi
    if not kwargsFinal.has_key('colors'):
        kwargsFinal['colors'] = 'k'
    if not kwargsFinal.has_key('linestyles'):
        kwargsFinal['linestyles'] = 'dashed'
    if not kwargsFinal.has_key('linewidths'):
        kwargsFinal['linewidths'] = 1.5

    figure = plt.figure()
    plt.clf()
    ax = plt.subplot(111)
    
    kwargsInit['alpha']  = transpFun(1.)
    kwargsFinal['alpha'] = transpFun(0.)

    lineBkgPbar, = plot(ax, [yPbar,yPbar], [0.2,0.8], 'k-', linewidth=5)
    linePbar,    = plot(ax, [yPbar,yPbar], [0.2,0.2], 'g-', linewidth=5)
    timeText     = ax.text(xTxt, yTxt, fileNameSuffix(0.,config.P+2)+' / '+str(config.P+1))
    imC          = plotMatrix(ax, f[:,:,0], plotter, **kwargsCurrent)
    imI          = plotMatrix(ax, finit, 'contour', **kwargsInit)
    imF          = plotMatrix(ax, ffinal, 'contour', **kwargsFinal)

    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$')

    ax.set_xlim(-0.1,1.1)
    ax.set_ylim(-0.1,1.1)

    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', '10%', pad='5%')

    cmap = mpl.cm.jet
    norm = mpl.colors.Normalize(vmin=mini, vmax=maxi)
    cb1 = mpl.colorbar.ColorbarBase(cax, cmap=cmap, norm=norm, orientation='vertical')

    ax.set_title('Final iteration\nt = ' + fileNameSuffix(0,config.P+2) + ' / '+str(config.P+1))
    
    def animate(t):
        ret = []
        kwargsInit['alpha']  = transpFun(1.-float(t)/(config.P+1.))
        kwargsFinal['alpha'] = transpFun(float(t)/(config.P+1.))
        ax.cla()

        timeText     = ax.text(xTxt, yTxt, fileNameSuffix(t,config.P+2)+' / '+str(config.P+1))
        lineBkgPbar, = plot(ax, [yPbar,yPbar], [float(t)/(config.P+1.)*0.6+0.2,0.8], 'k-', linewidth=5)
        linePbar,    = plot(ax, [yPbar,yPbar], [0.2,float(t)/(config.P+1.)*0.6+0.2], 'g-', linewidth=5)

        ret.extend([timeText,lineBkgPbar,linePbar])

        imC = plotMatrix(ax, f[:,:,t], plotter, **kwargsCurrent)
        imI = plotMatrix(ax, finit, 'contour', **kwargsInit)
        imF = plotMatrix(ax, ffinal, 'contour', **kwargsFinal)

        ret.extend([imC,imI,imF])

        ax.set_xlabel('$x$')
        ax.set_ylabel('$y$')

        ax.set_xlim(-0.1,1.1)
        ax.set_ylim(-0.1,1.1)

        ax.set_title('Final iteration\nt = ' + fileNameSuffix(t,config.P+2) + ' / '+str(config.P+1))

        return tuple(ret)

    def init():
        return animate(0)

    frames = np.arange(finalState.P+2)

    print('Making animation ...')
    ani = anim.FuncAnimation(figure, animate, frames, init_func=init, interval=interval, blit=True)
    print('Writing '+figDir+figName+' ...')
    ani.save(figDir+figName,writer)
