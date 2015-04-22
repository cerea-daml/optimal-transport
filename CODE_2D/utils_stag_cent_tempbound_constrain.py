import numpy as np
import scipy.fftpack as fft
import time as tm

from utils_grid import *

class ProxCstagcenttempbound:
    '''
    Utils related to the staggered/centered and temporal boundary condition constrain
    C_s_c_tb = { (U,V) in E_s x E_c \ V - interpolation(U) = interpDefault & boundary(U) = (f_init,f_final) }
             = { (U,V) in E_s x E_c \ A_s_c_tb.(U,V) = (interpDefault,f_init,f_final) }
    '''

    def __init__(self, M, N, P,
                 interpDefault=None,
                 f0=None,  f1=None):
        self.M = M
        self.N = N
        self.P = P
        
        self.kernel = CenteredGridTempBound(M, N, P, CenteredGrid(M,N,P,interpDefault), f0, f1)

        self.inv_A_T_A_s_c_tb_mx = np.linalg.inv(self.A_T_A_s_c_tb_mx())
        self.inv_A_T_A_s_c_tb_my = np.linalg.inv(self.A_T_A_s_c_tb_my())
        self.inv_A_T_A_s_c_tb_f  = np.linalg.inv(self.A_T_A_s_c_tb_f())

###############
# Sub operators
###############

    def A_T_A_s_c_tb_mx(self):
        alpha = 0.5
        diag    = np.ones(self.M+1)+2*alpha**2
        diagSup = np.zeros(self.M)+alpha**2
        return np.diag(diag)+np.diag(diagSup,-1)+np.diag(diagSup,1)

    def A_T_A_s_c_tb_my(self):
        alpha = 0.5
        diag    = np.ones(self.N+1)+2*alpha**2
        diagSup = np.zeros(self.N)+alpha**2
        return np.diag(diag)+np.diag(diagSup,-1)+np.diag(diagSup,1)

    def A_T_A_s_c_tb_f(self):
        alpha = 0.5
        diag           = np.ones(self.P+1+2)+2*alpha**2
        diag[0]        = 1.
        diag[self.P+2] = 1.

        diagSup           = np.zeros(self.P+1+1)+alpha**2
        diagSup[0]        = -alpha
        diagSup[self.P+1] = -alpha

        return np.diag(diag)+np.diag(diagSup,-1)+np.diag(diagSup,1)

######################
# Projection functions
######################

    def __repr__(self):
        return ( 'Proximal operator associated to the staggered/centered and temporal boundary condition constrain on a grid with shape :' +
                 str(self.M) + ' x ' +
                 str(self.N) + ' x ' +
                 str(self.P) )

    def __delattr__(self, nom_attr):
        raise AttributeError('You can not delete any attribute from this class : ProxCstagcenttempbound')

    def A_s_c_tb(self, grid):
        return grid.interpolationDefault_TemporalBoundary()
               
    def T_A_s_c_tb(self, gridTempBound):
        return gridTempBound.T_interpolationDefault_TemporalBoundary()

    def A_T_A_s_c_tb(self, gridTempBound):
        return self.A_s_c_tb(self.T_A_s_c_tb(gridTempBound))

    def inv_A_T_A_s_c_tb(self, gridTempBound):
        # inverts operator A o T_A
        # this function modifies grid

        mx = np.tensordot(self.inv_A_T_A_s_c_tb_mx,gridTempBound.centGrid.mx,([1],[0]))
        my = np.tensordot(self.inv_A_T_A_s_c_tb_my,gridTempBound.centGrid.my,([1],[1])).transpose((1,0,2))

        f = np.zeros(shape=(self.M+1,self.N+1,self.P+3))
        f[:,:,0]          = gridTempBound.bt0[:,:]
        f[:,:,1:self.P+2] = gridTempBound.centGrid.f[:,:,0:self.P+1]
        f[:,:,self.P+2]   = gridTempBound.bt1[:,:]
        f = np.tensordot(self.inv_A_T_A_s_c_tb_f,f,([1],[2])).transpose((1,2,0))

        return CenteredGridTempBound( self.M, self.N, self.P,
                                      CenteredGrid( self.M, self.N, self.P,
                                                    mx, my, f[:,:,1:self.P+2] ),
                                      f[:,:,0],  f[:,:,self.P+2] )

    def __call__(self, stagCentGrid):
        # projects staggered/centered grid on the staggered/centered and boundary condition constrain        
        gridTempBound =  self.A_s_c_tb(stagCentGrid)
        gridTempBound -= self.kernel
        gridTempBound =  self.inv_A_T_A_s_c_tb(gridTempBound)
        gridP         =  self.T_A_s_c_tb(gridTempBound)
        return ( stagCentGrid - gridP )

    def test(self):
        M = self.M
        N = self.N
        P = self.P

        gridTB1 = CenteredGridTempBound.random(M, N, P)
        e = 0.
        t = 0.

        gridTB2 = gridTB1.copy()
        time_start = tm.time()
        gridTB2 = self.inv_A_T_A_s_c_tb(gridTB2)
        gridTB2 = self.A_T_A_s_c_tb(gridTB2)
        t += tm.time() - time_start
        e += ( gridTB1 - gridTB2 ).LInftyNorm()

        gridTB2 = gridTB1.copy()
        time_start = tm.time()
        gridTB2 = self.A_T_A_s_c_tb(gridTB2)
        gridTB2 = self.inv_A_T_A_s_c_tb(gridTB2)
        t += tm.time() - time_start

        e += ( gridTB1 - gridTB2 ).LInftyNorm()
        return e, t

    def timing(self,nTiming):
        t = 0.
        for i in xrange(nTiming):
            grid = StaggeredCenteredGrid.random(self.M, self.N, self.P)
            time_start = tm.time()
            grid = self(grid)
            t += tm.time() - time_start
        return t
