import numpy as np
import scipy.fftpack as fft
import time as tm

from utils_grid import *

class ProxCstagcentbound:
    '''
    Utils related to the staggered/centered and boundary condition constrain
    C_s_c_b = { (U,V) in E_s x E_c \ V - interpolation(U) = interpDefault & boundary(U) = (m_left,m_right,m_down,m_up,f_init,f_final) }
            = { (U,V) in E_s x E_c \ A_s_c_b.(U,V) = (interpDefault,m_left,m_right,m_down,m_up,f_init,f_final) }
    '''

    def __init__(self, M, N, P,
                 interpDefault=None,
                 mx0=None, mx1=None,
                 my0=None, my1=None,
                 f0=None,  f1=None):
        self.M = M
        self.N = N
        self.P = P
        
        self.kernel = CenteredGridBound(M, N, P, CenteredGrid(M,N,P,interpDefault), mx0, mx1, my0, my1, f0, f1)

        self.inv_A_T_A_s_c_b_mx = np.linalg.inv(self.A_T_A_s_c_b_mx())
        self.inv_A_T_A_s_c_b_my = np.linalg.inv(self.A_T_A_s_c_b_my())
        self.inv_A_T_A_s_c_b_f  = np.linalg.inv(self.A_T_A_s_c_b_f())

###############
# Sub operators
###############

    def A_T_A_s_c_b_mx(self):
        alpha = 0.5
        diag           = np.ones(self.M+1+2)+2*alpha**2
        diag[0]        = 1.
        diag[self.M+2] = 1.

        diagSup           = np.zeros(self.M+1+1)+alpha**2
        diagSup[0]        = -alpha
        diagSup[self.M+1] = -alpha

        return np.diag(diag)+np.diag(diagSup,-1)+np.diag(diagSup,1)

    def A_T_A_s_c_b_my(self):
        alpha = 0.5
        diag           = np.ones(self.N+1+2)+2*alpha**2
        diag[0]        = 1.
        diag[self.N+2] = 1.

        diagSup           = np.zeros(self.N+1+1)+alpha**2
        diagSup[0]        = -alpha
        diagSup[self.N+1] = -alpha

        return np.diag(diag)+np.diag(diagSup,-1)+np.diag(diagSup,1)

    def A_T_A_s_c_b_f(self):
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
        return ( 'Proximal operator associated to the staggered/centered and boundary condition constrain on a grid with shape :' +
                 str(self.M) + ' x ' +
                 str(self.N) + ' x ' +
                 str(self.P) )

    def __delattr__(self, nom_attr):
        raise AttributeError('You can not delete any attribute from this class : ProxCstagcentbound')

    def A_s_c_b(self, grid):
        return grid.interpolationDefault_Boundary()
               
    def T_A_s_c_b(self, gridBound):
        return gridBound.T_interpolationDefault_Boundary()

    def A_T_A_s_c_b(self, gridBound):
        return self.A_s_c_b(self.T_A_s_c_b(gridBound))

    def inv_A_T_A_s_c_b(self, gridBound):
        # inverts operator A o T_A
        # this function modifies grid

        mx = np.zeros(shape=(self.M+3,self.N+1,self.P+1))
        mx[0,:,:]          = gridBound.bx0[:,:]
        mx[1:self.M+2,:,:] = gridBound.centGrid.mx[0:self.M+1,:,:]
        mx[self.M+2,:,:]   = gridBound.bx1[:,:]
        mx = np.tensordot(self.inv_A_T_A_s_c_b_mx,mx,([1],[0]))

        my = np.zeros(shape=(self.M+1,self.N+3,self.P+1))
        my[:,0,:]          = gridBound.by0[:,:]
        my[:,1:self.N+2,:] = gridBound.centGrid.my[:,0:self.N+1,:]
        my[:,self.N+2,:]   = gridBound.by1[:,:]
        my = np.tensordot(self.inv_A_T_A_s_c_b_my,my,([1],[1])).transpose((1,0,2))

        f = np.zeros(shape=(self.M+1,self.N+1,self.P+3))
        f[:,:,0]          = gridBound.bt0[:,:]
        f[:,:,1:self.P+2] = gridBound.centGrid.f[:,:,0:self.P+1]
        f[:,:,self.P+2]   = gridBound.bt1[:,:]
        f = np.tensordot(self.inv_A_T_A_s_c_b_f,f,([1],[2])).transpose((1,2,0))

        return CenteredGridBound( self.M, self.N, self.P,
                                  CenteredGrid( self.M, self.N, self.P,
                                                mx[1:self.M+2,:,:], my[:,1:self.N+2,:], f[:,:,1:self.P+2] ),
                                  mx[0,:,:], mx[self.M+2,:,:],
                                  my[:,0,:], my[:,self.N+2,:],
                                  f[:,:,0],  f[:,:,self.P+2] )

    def __call__(self, stagCentGrid):
        # projects staggered/centered grid on the staggered/centered and boundary condition constrain        
        gridBound = self.A_s_c_b(stagCentGrid)
        gridBound -= self.kernel
        gridBound = self.inv_A_T_A_s_c_b(gridBound)
        gridP    = self.T_A_s_c_b(gridBound)
        return ( stagCentGrid - gridP )

    def test(self):
        M = self.M
        N = self.N
        P = self.P

        gridB1 = CenteredGridBound.random(M, N, P)
        e = 0.
        t = 0.

        gridB2 = gridB1.copy()
        time_start = tm.time()
        gridB2 = self.inv_A_T_A_s_c_b(gridB2)
        gridB2 = self.A_T_A_s_c_b(gridB2)
        t += tm.time() - time_start
        e += ( gridB1 - gridB2 ).LInftyNorm()

        gridB2 = gridB1.copy()
        time_start = tm.time()
        gridB2 = self.A_T_A_s_c_b(gridB2)
        gridB2 = self.inv_A_T_A_s_c_b(gridB2)
        t += tm.time() - time_start

        e += ( gridB1 - gridB2 ).LInftyNorm()
        return e, t

    def timing(self,nTiming):
        t = 0.
        for i in xrange(nTiming):
            grid = StaggeredCenteredGrid.random(self.M, self.N, self.P)
            time_start = tm.time()
            grid = self(grid)
            t += tm.time() - time_start
        return t
