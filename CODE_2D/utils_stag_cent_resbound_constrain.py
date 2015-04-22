import numpy as np
import scipy.fftpack as fft
import time as tm

from utils_grid import *

class ProxCstagcentresbound:
    '''
    Utils related to the staggered/centered and boundary condition constrain with a reservoir
    C_s_c_rb = { (U,V) in E_s x E_c \ V - interpolation(U) = interpDefault & boundary(U) = (m_left,m_right,m_down,m_up,f_init,f_final[1:M,1:N]) }
             = { (U,V) in E_s x E_c \ A_s_c_rb.(U,V) = (interpDefault,m_left,m_right,m_down,m_up,f_init,f_final[1:M,1:N]) }
    '''

    def __init__(self, M, N, P,
                 interpDefault=None,
                 mx0=None, mx1=None,
                 my0=None, my1=None,
                 f0=None,  f1=None):
        self.M = M
        self.N = N
        self.P = P
        
        self.kernel = CenteredGridResBound(M, N, P, CenteredGrid(M,N,P,interpDefault), mx0, mx1, my0, my1, f0, f1)

        self.inv_A_T_A_s_c_rb_mx     = np.linalg.inv(self.A_T_A_s_c_rb_mx())
        self.inv_A_T_A_s_c_rb_my     = np.linalg.inv(self.A_T_A_s_c_rb_my())
        self.inv_A_T_A_s_c_rb_f      = np.linalg.inv(self.A_T_A_s_c_rb_f())
        self.inv_A_T_A_s_c_rb_f_lim  = np.linalg.inv(self.A_T_A_s_c_rb_f_lim())

###############
# Sub operators
###############

    def A_T_A_s_c_rb_mx(self):
        alpha = 0.5
        diag           = np.ones(self.M+1+2)+2*alpha**2
        diag[0]        = 1.
        diag[self.M+2] = 1.

        diagSup           = np.zeros(self.M+1+1)+alpha**2
        diagSup[0]        = -alpha
        diagSup[self.M+1] = -alpha

        return np.diag(diag)+np.diag(diagSup,-1)+np.diag(diagSup,1)

    def A_T_A_s_c_rb_my(self):
        alpha = 0.5
        diag           = np.ones(self.N+1+2)+2*alpha**2
        diag[0]        = 1.
        diag[self.N+2] = 1.

        diagSup           = np.zeros(self.N+1+1)+alpha**2
        diagSup[0]        = -alpha
        diagSup[self.N+1] = -alpha

        return np.diag(diag)+np.diag(diagSup,-1)+np.diag(diagSup,1)

    def A_T_A_s_c_rb_f(self):
        alpha = 0.5
        diag           = np.ones(self.P+1+2)+2*alpha**2
        diag[0]        = 1.
        diag[self.P+2] = 1.

        diagSup           = np.zeros(self.P+1+1)+alpha**2
        diagSup[0]        = -alpha
        diagSup[self.P+1] = -alpha

        return np.diag(diag)+np.diag(diagSup,-1)+np.diag(diagSup,1)

    def A_T_A_s_c_rb_f_lim(self):
        alpha = 0.5
        diag           = np.ones(self.P+1+1)+2*alpha**2
        diag[0]        = 1.

        diagSup           = np.zeros(self.P+1)+alpha**2
        diagSup[0]        = -alpha

        return np.diag(diag)+np.diag(diagSup,-1)+np.diag(diagSup,1)

######################
# Projection functions
######################

    def __repr__(self):
        return ( 'Proximal operator associated to the staggered/centered and boundary condition constrain with a reservoir on a grid with shape :' +
                 str(self.M) + ' x ' +
                 str(self.N) + ' x ' +
                 str(self.P) )

    def __delattr__(self, nom_attr):
        raise AttributeError('You can not delete any attribute from this class : ProxCstagcentresbound')

    def A_s_c_rb(self, grid):
        return grid.interpolationDefault_ResBoundary()
               
    def T_A_s_c_rb(self, gridResBound):
        return gridResBound.T_interpolationDefault_ResBoundary()

    def A_T_A_s_c_rb(self, gridResBound):
        return self.A_s_c_rb(self.T_A_s_c_rb(gridResBound))

    def inv_A_T_A_s_c_rb(self, gridResBound):
        # inverts operator A o T_A

        mx = np.zeros(shape=(self.M+3,self.N+1,self.P+1))
        mx[0,:,:]          = gridResBound.bx0[:,:]
        mx[1:self.M+2,:,:] = gridResBound.centGrid.mx[0:self.M+1,:,:]
        mx[self.M+2,:,:]   = gridResBound.bx1[:,:]
        mx = np.tensordot(self.inv_A_T_A_s_c_rb_mx,mx,([1],[0]))

        my = np.zeros(shape=(self.M+1,self.N+3,self.P+1))
        my[:,0,:]          = gridResBound.by0[:,:]
        my[:,1:self.N+2,:] = gridResBound.centGrid.my[:,0:self.N+1,:]
        my[:,self.N+2,:]   = gridResBound.by1[:,:]
        my = np.tensordot(self.inv_A_T_A_s_c_rb_my,my,([1],[1])).transpose((1,0,2))

        # Inversion for f
        fv = np.zeros(shape=(self.M+1,self.N+1,self.P+1))
        bt0 = np.zeros(shape=(self.M+1,self.N+1))
        bt1 = np.zeros(shape=(self.M-1,self.N-1))

        # x = 0
        f                        = np.zeros(shape=(self.N+1,self.P+2))
        f[:,0]                   = gridResBound.bt0[0,:]
        f[0:self.N+1,1:self.P+2] = gridResBound.centGrid.f[0,0:self.N+1,0:self.P+1]
        f = np.transpose(np.tensordot(self.inv_A_T_A_s_c_rb_f_lim,f,([1],[1])))

        bt0[0,:]                    = f[:,0]
        fv[0,0:self.N+1,0:self.P+1] = f[0:self.N+1,1:self.P+2]

        # y = 0
        f                        = np.zeros(shape=(self.M+1,self.P+2))
        f[:,0]                   = gridResBound.bt0[:,0]
        f[0:self.M+1,1:self.P+2] = gridResBound.centGrid.f[0:self.M+1,0,0:self.P+1]
        f = np.transpose(np.tensordot(self.inv_A_T_A_s_c_rb_f_lim,f,([1],[1])))

        bt0[:,0]                    = f[:,0]
        fv[0:self.M+1,0,0:self.P+1] = f[0:self.M+1,1:self.P+2]

        # x = 1..M, y = 1..N
        f                 = np.zeros(shape=(self.M-1,self.N-1,self.P+3))
        f[:,:,0]          = gridResBound.bt0[1:self.M,1:self.N]
        f[:,:,1:self.P+2] = gridResBound.centGrid.f[1:self.M,1:self.N,0:self.P+1]
        f[:,:,self.P+2]   = gridResBound.bt1[:,:]
        f = np.tensordot(self.inv_A_T_A_s_c_rb_f,f,([1],[2])).transpose((1,2,0))

        bt0[1:self.M,1:self.N] = f[:,:,0]
        fv[1:self.M,1:self.N]  = f[:,:,1:self.P+2]
        bt1[:,:]               = f[:,:,self.P+2]

        # x = M
        f                        = np.zeros(shape=(self.N+1,self.P+2))
        f[:,0]                   = gridResBound.bt0[self.M,:]
        f[0:self.N+1,1:self.P+2] = gridResBound.centGrid.f[self.M,0:self.N+1,0:self.P+1]
        f = np.transpose(np.tensordot(self.inv_A_T_A_s_c_rb_f_lim,f,([1],[1])))

        bt0[self.M,:]                    = f[:,0]
        fv[self.M,0:self.N+1,0:self.P+1] = f[0:self.N+1,1:self.P+2]

        # y = N
        f                        = np.zeros(shape=(self.M+1,self.P+2))
        f[:,0]                   = gridResBound.bt0[:,self.N]
        f[0:self.M+1,1:self.P+2] = gridResBound.centGrid.f[0:self.M+1,self.N,0:self.P+1]
        f = np.transpose(np.tensordot(self.inv_A_T_A_s_c_rb_f_lim,f,([1],[1])))

        bt0[:,self.N]                    = f[:,0]
        fv[0:self.M+1,self.N,0:self.P+1] = f[0:self.M+1,1:self.P+2]

        return CenteredGridResBound( self.M, self.N, self.P,
                                     CenteredGrid( self.M, self.N, self.P,
                                                   mx[1:self.M+2,:,:], my[:,1:self.N+2,:], fv ),
                                     mx[0,:,:], mx[self.M+2,:,:],
                                     my[:,0,:], my[:,self.N+2,:],
                                     bt0, bt1 )

    def __call__(self, stagCentGrid):
        # projects staggered/centered grid on the staggered/centered and boundary condition constrain        
        gridResBound  = self.A_s_c_rb(stagCentGrid)
        gridResBound -= self.kernel
        gridResBound  = self.inv_A_T_A_s_c_rb(gridResBound)
        gridP         = self.T_A_s_c_rb(gridResBound)
        return ( stagCentGrid - gridP )

    def test(self):
        M = self.M
        N = self.N
        P = self.P

        gridRB1 = CenteredGridResBound.random(M, N, P)
        e = 0.
        t = 0.

        gridRB2 = gridRB1.copy()
        time_start = tm.time()
        gridRB2 = self.inv_A_T_A_s_c_rb(gridRB2)
        gridRB2 = self.A_T_A_s_c_rb(gridRB2)
        t += tm.time() - time_start
        e += ( gridRB1 - gridRB2 ).LInftyNorm()

        gridRB2 = gridRB1.copy()
        time_start = tm.time()
        gridRB2 = self.A_T_A_s_c_rb(gridRB2)
        gridRB2 = self.inv_A_T_A_s_c_rb(gridRB2)
        t += tm.time() - time_start

        e += ( gridRB1 - gridRB2 ).LInftyNorm()
        return e, t

    def timing(self,nTiming):
        t = 0.
        for i in xrange(nTiming):
            grid = StaggeredCenteredGrid.random(self.M, self.N, self.P)
            time_start = tm.time()
            grid = self(grid)
            t += tm.time() - time_start
        return t
