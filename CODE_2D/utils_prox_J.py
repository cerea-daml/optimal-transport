import numpy as np
import time as tm

from utils_grid import *

class ProxJ:
    '''
    Proximal operator for the cost function J = sum(m**2/f)
    '''

    def __init__(self, gamma):
        self.gamma = gamma

    def __repr__(self):
        return ( 'Proximal operator associated to the cost function J = sum(m**2/f)' )

    def __delattr__(self, nom_attr):
        raise AttributeError('You can not delete any attribute from this class : ProxJ')

    def __call__(self, grid):
        return grid.proxJ(self.gamma)

    def timing(self,M,N,P,nTiming):
        t = 0.
        for i in xrange(nTiming):
            grid = CenteredGrid.random(M,N,P)
            time_start = tm.time()
            grid = self(grid)
            t += tm.time() - time_start
        return t
