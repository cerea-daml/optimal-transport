#__________________________________________________
#__________________________________________________

# Copyrigth 2016 A. Farchi and M. Bocquet
# CEREA, joint laboratory Ecole des Ponts ParisTech and EDF R&D

# Code for the paper: Using the Wasserstein distance to compare fields of pollutants:
# Application to the radionuclide atmospheric dispersion of the Fukushima-Daiichi accident
# by A. Farchi, M. Bocquet, Y. Roustan, A. Mathieu and A. Querel

#__________________________________________________

#__________________________________________________
#_______________
# interpolate.py
#_______________

import numpy as np
from scipy.interpolate import interp1d

#__________________________________________________

def interpolateTimeFinalState(f, newP, copy=True):
    oldP    = f.shape[len(f.shape)-1] - 2
    if oldP == newP:
        return f
    else:
        interpF = interp1d(np.linspace(0.0, 1.0, oldP+2), f, copy=copy, bounds_error=False, fill_value=0.0)
        return interpF(np.linspace(0.0, 1.0, newP+2))

#__________________________________________________

def interpolateTimeFinalStateMultiSim(fs, newP, copy=True):
    fs_corr = []
    for f in fs:
        fs_corr.append(interpolateTimeFinalState(f, newP, copy=copy))
    return fs_corr

#__________________________________________________

def makeInterpolatorPP(X, Y, copy=True):
    if copy:
        return makeInterpolatorPP(X.copy(), Y.copy(), copy=False)

    XPP       = np.zeros(X.size+2)
    XPP[1:-1] = X[:]
    XPP[0]    = X[0] - 1.0
    XPP[-1]   = X[-1] + 1.0

    YPP       = np.zeros(Y.size+2)
    YPP[1:-1] = Y[:]
    YPP[0]    = Y[0]
    YPP[-1]   = Y[-1]

    return interp1d(XPP, YPP, copy=False, bounds_error=False, fill_value=0.0)

#__________________________________________________
