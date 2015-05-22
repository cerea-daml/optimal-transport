###############
# plotMatrix.py
###############

from scipy.interpolate import interp2d

from extent import xyExtentPP
from extent import extendY2d

def plotMatrix(ax, matrix, plotter='imshow', copy=True, **kwargs):

    M            = matrix.shape[0] - 1
    N            = matrix.shape[1] - 1

    X,Y          = xyExtentPP(M,N)

    matrixPP     = extendY2d(matrix, axis=0, copy=copy)
    matrixPP     = extendY2d(matrixPP, axis=1, copy=False)

    interpMatrix = interp2d(X, Y, matrixPP, copy=False, bounds_error=False, fill_value=0.0)

    XNew         = np.linspace(0.0, 1.0, 2*(M+1)+1)
    YNew         = np.linspace(0.0, 1.0, 2*(N+1)+1)

    Xmini        = 0.0 - 0.5 / ( 2. * (M+1) )
    Xmaxi        = 1.0 + 0.5 / ( 2. * (M+1) )

    Ymini        = 0.0 - 0.5 / ( 2. * (N+1) )
    Ymaxi        = 1.0 + 0.5 / ( 2. * (N+1) )

    matrixToPlot = interpMatrix(XNew, YNew).transpose()

    if not kwargs.has_key('origin'):
        kwargs['origin'] = 'lower'

    if not kwargs.has_key('extent'):
        kwargs['extent'] = [Xmini, Xmaxi, Ymini, Ymaxi]
 
    if plotter == 'imshow':
        return ax.imshow(matrixToPlot, **kwargs)
    elif plotter == 'contour':
        return ax.contour(matrixToPlot, **kwargs)
    elif plotter == 'contourf':
        return ax.contourf(matrixToPlot, **kwargs)
