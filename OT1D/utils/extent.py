###########
# extent.py
###########

import numpy as np

def xExtent(N):
    return np.linspace(0.5/(N+1.), 1.0-0.5/(N+1.), N+1)

def xyExtent(M,N):
    x = np.linspace(0.5/(M+1.), 1.0-0.5/(M+1.), M + 1)
    y = np.linspace(0.5/(N+1.), 1.0-0.5/(N+1.), N + 1)
    return np.meshgrid(x, y, indexing='ij')

def xExtentPP(N):
    X        = np.zeros(N+3)
    X[1:N+2] = xExtent(N)
    X[N+2]   = 1.0
    return X

def extendY1d(Y, copy=True):
    if not copy:
        YPP             = np.zeros(Y.size+2)
        YPP[1:Y.size+1] = Y[:]
        return YPP
    else:
        return extendY1d(Y.copy(), False)

def extendY2d(Y, axis=0, copy=True):
    if not copy:
        if axis == 0:
            YPP = np.zeros(shape=(Y.shape[0]+2, Y.shape[1]))
            YPP[1:Y.shape[0]+1,:] = Y[:,:]
            return YPP
        elif axis == 1:
            YPP = np.zeros(shape=(Y.shape[0], Y.shape[1]+2))
            YPP[:,1:Y.shape[1]+1] = Y[:,:]
            return YPP
        else:
            return
    else:
        return extendY2d(Y.copy(), axis, False)
