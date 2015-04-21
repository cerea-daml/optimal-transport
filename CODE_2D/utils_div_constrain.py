import numpy as np
import scipy.fftpack as fft
import time as tm

from utils_grid import *

class ProxCdiv:
    '''
    Utils related to the divergence constrain
    C_div = { U in E_s \ div(U)=0 }
          = { U in E_s \ A_div.U = (0) }
    '''

    def __init__(self, M, N, P, div=None):
        self.M = M
        self.N = N
        self.P = P
        x = np.arange(M+1)
        y = np.arange(N+1)
        z = np.arange(P+1)

        if div is None:
            self.kernel = np.zeros(shape=(M+1,N+1,P+1))
        else:
            self.kernel = div

        Xm,Ym,Zm =np.meshgrid(x,y,z,indexing='ij')
        self.eigvalues_A_div = ( 2. * (M**2) * ( 1. - np.cos( np.pi * ( Xm + 1. ) / ( M + 2. ) ) ) +
                                 2. * (N**2) * ( 1. - np.cos( np.pi * ( Ym + 1. ) / ( N + 2. ) ) ) +
                                 2. * (P**2) * ( 1. - np.cos( np.pi * ( Zm + 1. ) / ( P + 2. ) ) ) )

    def __repr__(self):
        return ( 'Proximal operator associated to the divergence free constrain on a grid with shape :' +
                 str(self.M) + ' x ' +
                 str(self.N) + ' x ' +
                 str(self.P) )

    def __delattr__(self, nom_attr):
        raise AttributeError('You can not delete any attribute from this class : Prox_C_div')

    def A_div(self,grid):
        return grid.divergence()

    def T_A_div(self,div):
        return div.T_divergence()

    def A_T_A_div(self,div):
        return self.A_div(self.T_A_div(div))

    def inv_A_T_A_div(self,divergence):
        # inverts operator A o T_A
        # this function modifies divergence
        
        div = divergence.div

        div = 0.5*fft.dst(div, type=1, axis=0)
        div = 0.5*fft.dst(div, type=1, axis=1)
        div = 0.5*fft.dst(div, type=1, axis=2)
        
        div = div/self.eigvalues_A_div

        div = fft.dst(div, type=1, axis=0) / ( self.M + 2. )
        div = fft.dst(div, type=1, axis=1) / ( self.N + 2. )
        div = fft.dst(div, type=1, axis=2) / ( self.P + 2. )

        divergence.div = div
        return divergence

    def __call__(self,grid):
        # projects StaggeredGrid grid on the divergence free constrain
        
        div = self.A_div(grid)
        div -= self.kernel
        div = self.inv_A_T_A_div(div)
        gridP = self.T_A_div(div)

        return ( grid - gridP )

    def test(self):
        div1 = Divergence.random(self.M, self.N, self.P)
        e = 0.
        t = 0.

        div2 = div1.copy()
        time_start = tm.time()
        div2 = self.inv_A_T_A_div(div2)
        div2 = self.A_T_A_div(div2)
        t += tm.time() - time_start
        e += ( div1 - div2 ).LInftyNorm()

        div2 = div1.copy()
        time_start = tm.time()
        div2 = self.A_T_A_div(div2)
        div2 = self.inv_A_T_A_div(div2)
        t += tm.time() - time_start
        e += ( div1 - div2 ).LInftyNorm()

        return e, t

    def timing(self,nTiming):
        t = 0.
        for i in xrange(nTiming):
            grid = StaggeredGrid.random(self.M, self.N, self.P)
            time_start = tm.time()
            grid = self(grid)
            t += tm.time() - time_start
        return t
