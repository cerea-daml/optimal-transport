import numpy as np
import scipy.fftpack as fft
import time as tm

from utils_grid import *

class ProxCdivbound:
    '''
    Utils related to the divergence and boundary condition constrain
    C_div_b = { U in E_s \ div(U)=div & boundary(U) = (m_left,m_right,m_down,m_up,f_init,f_final) }
            = { U in E_s \ A_div_b.U = (div,m_left,m_right,m_down,m_up,f_init,f_final) }
    '''

    def __init__(self, M, N, P,
                 div=None,
                 mx0=None, mx1=None,
                 my0=None, my1=None,
                 f0=None,  f1=None):
        self.M = M
        self.N = N
        self.P = P
        self.kernel = DivergenceBound(M, N, P, div,
                                      mx0, mx1,
                                      my0, my1,
                                      f0,  f1 )        
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
        return grid.divBound()
               
    def T_A_div_b(self, divBound):
        return divBound.T_divBound()

    def A_T_A_div_b(self, divBound):
        return self.A_div_b(self.T_A_div_b(divBound))

    def inv_A_T_A_div_b(self, divBound):
        # inverts operator A o T_A
        # this function modifies div and the boundary conditions

        divBound.applyGaussForward()

        div = divBound.div
        div = 0.5*fft.dct(div, axis=0)
        div = 0.5*fft.dct(div, axis=1)
        div = 0.5*fft.dct(div, axis=2)
        
        div[0,0,0] = 0.0
        div = div/self.eigvalues_A_div_b

        div = fft.idct(div, axis=0) / ( self.M + 1. )
        div = fft.idct(div, axis=1) / ( self.N + 1. )
        div = fft.idct(div, axis=2) / ( self.P + 1. )

        divBound.div = div
        divBound.applyGaussBackward()

        return divBound

    def __call__(self, grid):
        # projects StaggeredGrid grid on the divergence and boundary condition constrain        
        divBound = self.A_div_b(grid)
        divBound -= self.kernel
        divBound = self.inv_A_T_A_div_b(divBound)
        gridP = self.T_A_div_b(divBound)
        return ( grid - gridP )

    def test(self):
        M = self.M
        N = self.N
        P = self.P
        EPS = 1e-8

        d = np.random.rand(M+1,N+1,P+1)
        mx0 = np.random.rand(N+1,P+1)
        mx1 = np.random.rand(N+1,P+1)
        my0 = np.random.rand(M+1,P+1)
        my1 = np.random.rand(M+1,P+1)
        f0 = np.random.rand(M+1,N+1)
        f1 = np.random.rand(M+1,N+1)

        sum = ( d.sum() +
                M*(mx0.sum() - mx1.sum()) +
                N*(my0.sum() - my1.sum()) +
                P*(f0.sum()  - f1.sum())  )

        if np.abs(sum) > EPS:
            nbrPts = ( (M+1.)*(N+1.)*(P+1.) + 
                        2.*(N+1.)*(P+1.) +
                        2.*(M+1.)*(P+1.) +
                        2.*(M+1.)*(N+1.) )
            d   -= sum/nbrPts
            mx0 -= sum/(M*nbrPts)
            mx1 += sum/(M*nbrPts)
            my0 -= sum/(N*nbrPts)
            my1 += sum/(N*nbrPts)
            f0  -= sum/(P*nbrPts)
            f1  += sum/(P*nbrPts)
            
            sum = ( d.sum()+
                    M*(mx0.sum() - mx1.sum()) +
                    N*(my0.sum() - my1.sum()) +
                    P*(f0.sum()  - f1.sum())  )

        e = 0.
        t = 0.
        divB1 = DivergenceBound(M, N, P, d, 
                                mx0, mx1,
                                my0, my1,
                                f0,  f1 )
        
        divB2 = divB1.copy()
        time_start = tm.time()
        divB2 = self.inv_A_T_A_div_b(divB2)
        divB2 = self.A_T_A_div_b(divB2)
        t += tm.time() - time_start
        e += ( divB1 - divB2 ).LInftyNorm()

        divB2 = divB1.copy()
        time_start = tm.time()
        divB2 = self.A_T_A_div_b(divB2)
        divB2 = self.inv_A_T_A_div_b(divB2)
        t += tm.time() - time_start

        diff = divB2.div[0,0,0] - divB1.div[0,0,0]

        d = np.ones(shape=(M+1,N+1,P+1))
        mx0 = M*np.ones(shape=(N+1,P+1))
        mx1 = -M*np.ones(shape=(N+1,P+1))
        my0 = N*np.ones(shape=(M+1,P+1))
        my1 = -N*np.ones(shape=(M+1,P+1))
        f0 = P*np.ones(shape=(M+1,N+1))
        f1 = -P*np.ones(shape=(M+1,N+1))

        divB3 = DivergenceBound(M, N, P, d,
                                mx0, mx1,
                                my0, my1,
                                f0,  f1 )
        
        e += ( divB1 - divB2 + diff*divB3 ).LInftyNorm()
        return e, t

    def timing(self,nTiming):
        t = 0.
        for i in xrange(nTiming):
            mx = np.random.rand(self.M+2, self.N+1, self.P+1)
            my = np.random.rand(self.M+1, self.N+2, self.P+1)
            f  = np.random.rand(self.M+1, self.N+1, self.P+2)
            grid = StaggeredGrid(self.M, self.N, self.P, mx, my, f)
            time_start = tm.time()
            grid = self(grid)
            t += tm.time() - time_start
        return t
