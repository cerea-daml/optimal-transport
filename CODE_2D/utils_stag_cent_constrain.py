import numpy as np
import scipy.fftpack as fft
import time as tm

from utils_grid import *

class ProxCstagcent:
    '''
    Utils related to the staggered/centered constrain
    C_s_c = { (U,V) in E_s x E_c \ V = interpolation(U) }
          = { (U,V) in E_s x E_c \ A_s_c.(U,V) = (0) }
    '''

    def __init__(self, M, N, P):
        self.M = M
        self.N = N
        self.P = P
        
        self.inv_A_T_A_s_c_mx = np.linalg.inv(self.A_T_A_s_c_mx())
        self.inv_A_T_A_s_c_my = np.linalg.inv(self.A_T_A_s_c_my())
        self.inv_A_T_A_s_c_f  = np.linalg.inv(self.A_T_A_s_c_f())

###############
# Sub operators
###############

    def A_T_A_s_c_mx(self):
        alpha = 0.5
        diag = np.ones(self.M+1) + 2.*alpha**2
        diagSup = np.zeros(self.M)+alpha**2
        return np.diag(diag)+np.diag(diagSup,-1)+np.diag(diagSup,1)

    def A_T_A_s_c_my(self):
        alpha = 0.5
        diag = np.ones(self.N+1) + 2.*alpha**2
        diagSup = np.zeros(self.N)+alpha**2
        return np.diag(diag)+np.diag(diagSup,-1)+np.diag(diagSup,1)

    def A_T_A_s_c_f(self):
        alpha = 0.5
        diag = np.ones(self.P+1) + 2.*alpha**2
        diagSup = np.zeros(self.P)+alpha**2
        return np.diag(diag)+np.diag(diagSup,-1)+np.diag(diagSup,1)

######################
# Projection functions
######################

    def __repr__(self):
        return ( 'Proximal operator associated to the staggered/centered constrain on a grid with shape :' +
                 str(self.M) + ' x ' +
                 str(self.N) + ' x ' +
                 str(self.P) )

    def __delattr__(self, nom_attr):
        raise AttributeError('You can not delete any attribute from this class : ProxCstagcent')

    def A_s_c(self, grid):
        return grid.interpolationDefault()
               
    def T_A_s_c(self, grid):
        return grid.T_interpolationDefault()

    def A_T_A_s_c(self, grid):
        return self.A_s_c(self.T_A_s_c(grid))

    def inv_A_T_A_s_c(self, grid):
        # inverts operator A o T_A
        # this function modifies grid

        grid.mx = np.tensordot(self.inv_A_T_A_s_c_mx,grid.mx,([1],[0]))
        grid.my = np.tensordot(self.inv_A_T_A_s_c_my,grid.my,([1],[1])).transpose((1,0,2))
        grid.f  = np.tensordot(self.inv_A_T_A_s_c_f, grid.f, ([1],[2])).transpose((1,2,0))

        return grid

    def __call__(self, stagCentGrid):
        # projects staggered/centered grid the staggered/centered constrain        
        centGrid = self.A_s_c(stagCentGrid)
        centGrid = self.inv_A_T_A_s_c(centGrid)
        gridP    = self.T_A_s_c(centGrid)
        return ( stagCentGrid - gridP )

    def test(self):
        M = self.M
        N = self.N
        P = self.P

        grid1 = CenteredGrid.random(M, N, P)
        e = 0.
        t = 0.

        grid2 = grid1.copy()
        time_start = tm.time()
        grid2 = self.inv_A_T_A_s_c(grid2)
        grid2 = self.A_T_A_s_c(grid2)
        t += tm.time() - time_start
        e += ( grid1 - grid2 ).LInftyNorm()

        grid2 = grid1.copy()
        time_start = tm.time()
        grid2 = self.A_T_A_s_c(grid2)
        grid2 = self.inv_A_T_A_s_c(grid2)
        t += tm.time() - time_start

        e += ( grid1 - grid2 ).LInftyNorm()
        return e, t

    def timing(self,nTiming):
        t = 0.
        for i in xrange(nTiming):
            grid = StaggeredCenteredGrid.random(self.M, self.N, self.P)
            time_start = tm.time()
            grid = self(grid)
            t += tm.time() - time_start
        return t
