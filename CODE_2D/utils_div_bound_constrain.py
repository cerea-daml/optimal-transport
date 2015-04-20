import numpy as np
import scipy.fftpack as fft
import time as tm

from utils_grid import *

class ProxCdivbound:
    '''
    Utils related to the divergence free and boundary condition constrain
    C_div_b = { U in E_s \ div(U)=0 & boundary(U) = (m_left,m_right,m_down,m_up,f_init,f_final) }
            = { U in E_s \ A_div_b.U = (0,m_left,m_right,m_down,m_up,f_init,f_final) }
    '''

    def __init__(self, M, N, P,
                 mx0, mx1,
                 my0, my1,
                 f0,  f1):
        self.M = M
        self.N = N
        self.P = P
        self.mx0 = mx0
        self.mx1 = mx1
        self.my0 = my0
        self.my1 = my1
        self.f0  = f0
        self.f1  = f1
        
        x = np.arange(M+1)
        y = np.arange(N+1)
        z = np.arange(P+1)

        Xm,Ym,Zm = np.meshgrid(x,y,z,indexing='ij')
        self.eigvalues_A_div_b = ( 2. * (M**2) * ( 1. - np.cos( np.pi * Xm / ( M + 1. ) ) ) +
                                   2. * (N**2) * ( 1. - np.cos( np.pi * Ym / ( N + 1. ) ) ) +
                                   2. * (P**2) * ( 1. - np.cos( np.pi * Zm / ( P + 1. ) ) ) )

        self.eigvalues_A_div_b[0,0,0] = 1.

    def __repr__(self):
        return ( 'Proximal operator associated to the divergence free and boundary condition constrain on a grid with shape :' +
                 str(self.M) + ' x ' +
                 str(self.N) + ' x ' +
                 str(self.P) )

    def __delattr__(self, nom_attr):
        raise AttributeError('You can not delete any attribute from this class : ProxCdivbound')

    def A_div_b(self, grid):
        return ( grid.divergence(), 
                 grid.bx0(), grid.bx1(),
                 grid.by0(), grid.by1(),
                 grid.bt0(), grid.bt1() )

    def T_A_div_b(self, div, 
                  bx0, bx1,
                  by0, by1,
                  bt0, bt1 ):
        M = self.M
        N = self.N
        P = self.P
        mx = np.zeros(shape=(M+2,N+1,P+1))
        my = np.zeros(shape=(M+1,N+2,P+1))
        f  = np.zeros(shape=(M+1,N+1,P+2))

        mx[0:M+1,:,:] = -M*div[0:M+1,:,:]
        mx[1:M+2,:,:] = mx[1:M+2,:,:] + M*div[0:M+1,:,:]
        mx[0,:,:] = mx[0,:,:] + bx0[:,:]
        mx[M+1,:,:] = mx[M+1,:,:] + bx1[:,:]

        my[:,0:N+1,:] = -N*div[:,0:N+1,:]
        my[:,1:N+2,:] = my[:,1:N+2,:] + N*div[:,0:N+1,:]
        my[:,0,:] = my[:,0,:] + by0[:,:]
        my[:,N+1,:] = my[:,N+1,:] + by1[:,:]

        f[:,:,0:P+1] = -P*div[:,:,0:P+1]
        f[:,:,1:P+2] = f[:,:,1:P+2] + P*div[:,:,0:P+1]
        f[:,:,0] = f[:,:,0] + bt0[:,:]
        f[:,:,P+1] = f[:,:,P+1] + bt1[:,:]
        return StaggeredGrid( M, N, P,
                              mx, my, f)

    def A_T_A_div_b(self, div,
                    bx0, bx1,
                    by0, by1,
                    bt0, bt1 ):
        return self.A_div_b(self.T_A_div_b(div, bx0, bx1, by0, by1, bt0, bt1))

    def inv_A_T_A_div_b(self, div,
                        bx0, bx1,
                        by0, by1,
                        bt0, bt1 ):
        # inverts operator A o T_A
        # this function modifies div and the boundary conditions

        div[0,:,:]      += self.M*bx0[:,:]
        div[self.M,:,:] -= self.M*bx1[:,:]
        div[:,0,:]      += self.N*by0[:,:]
        div[:,self.N,:] -= self.N*by1[:,:]
        div[:,:,0]      += self.P*bt0[:,:]
        div[:,:,self.P] -= self.P*bt1[:,:]

        div = 0.5*fft.dct(div, axis=0)
        div = 0.5*fft.dct(div, axis=1)
        div = 0.5*fft.dct(div, axis=2)
        
        div[0,0,0] = 0.0
        div = div/self.eigvalues_A_div_b

        div = fft.idct(div, axis=0) / ( self.M + 1. )
        div = fft.idct(div, axis=1) / ( self.N + 1. )
        div = fft.idct(div, axis=2) / ( self.P + 1. )

        bx0 += self.M*div[0,:,:]
        bx1 -= self.M*div[self.M,:,:]
        by0 += self.N*div[:,0,:]
        by1 -= self.N*div[:,self.N,:]
        bt0 += self.P*div[:,:,0]
        bt1 -= self.P*div[:,:,self.P]

        return ( div, 
                 bx0, bx1,
                 by0, by1,
                 bt0, bt1 )

    def __call__(self, grid):
        # projects StaggeredGrid grid on the divergence free and boundary condition constrain        
        div, bx0, bx1, by0, by1, bt0, bt1 = self.A_div_b(grid)

        bx0 -= self.mx0
        bx1 -= self.mx1
        by0 -= self.my0
        by1 -= self.my1
        bt0 -= self.f0
        bt1 -= self.f1

        div, bx0, bx1, by0, by1, bt0, bt1 = self.inv_A_T_A_div_b(div, bx0, bx1, by0, by1, bt0, bt1)
        gridP = self.T_A_div_b(div, bx0, bx1, by0, by1, bt0, bt1)
        return ( grid - gridP )

