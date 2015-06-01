################
# interpolate.py
################

import numpy as np
from scipy.interpolate import interp1d

def interpolateTimeFinalState(f, newP, copy=True):
    oldP    = f.shape[len(f.shape)-1] - 2
    if oldP == newP:
        return f
    else:
        interpF = interp1d(np.linspace(0.0, 1.0, oldP+2), f, copy=copy, bounds_error=False, fill_value=0.0)
        return interpF(np.linspace(0.0, 1.0, newP+2))

def interpolateTimeFinalStateMultiSim(fs, newP, copy=True):
    fs_corr = []
    for f in fs:
        fs_corr.append(interpolateTimeFinalState(f, newP, copy=copy))
    return fs_corr
