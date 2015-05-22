#########
# plot.py
#########

from extent import xExtentPP
from extent import extendY1d

def plot(ax, Y, X=None, opt=None, **kwargs):
    args = []
    if X is not None:
        args.append(X)
    args.append(Y)
    if opt is not None:
        args.append(opt)

    return ax.plot(*tuple(args), **kwargs)

def extandAndPlot(ax, Y, opt=None, **kwargs):
    N   = Y.size - 1
    X   = xExtentPP(N)
    YPP = extendY1d(Y, copy=False)

    args = [X, Y]
    if opt is not None:
        args.append(opt)

    return ax.plot(*tuple(args), **kwargs)
    
