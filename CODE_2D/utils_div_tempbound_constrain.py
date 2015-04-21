import numpy as np
import scipy.fftpack as fft
import time as tm

from utils_grid import *

class ProxCdivtempbound:
    '''
    Utils related to the divergence and temporal boundary condition constrain
    C_div_tb = { U in E_s \ div(U)=div & boundary(U) = (f_init,f_final) }
             = { U in E_s \ A_div_b.U = (div,f_init,f_final) }
    '''

    def __init__(self, M, N, P,
                 div=None,
                 f0=None,  f1=None):
        self.M = M
        self.N = N
        self.P = P
        self.kernel = DivergenceTempBound(M, N, P, div,
                                          f0,  f1 )        
        x = np.arange(M+1)
        y = np.arange(N+1)
        z = np.arange(P+1)

        Xm,Ym,Zm = np.meshgrid(x,y,z,indexing='ij')
        self.eigvalues_A_div_tb = ( 2. * (M**2) * ( 1. - np.cos( np.pi * ( Xm + 1. ) / ( M + 2. ) ) ) +
                                    2. * (N**2) * ( 1. - np.cos( np.pi * ( Ym + 1. ) / ( N + 2. ) ) ) +
                                    2. * (P**2) * ( 1. - np.cos( np.pi *   Zm        / ( P + 1. ) ) ) )

    def __repr__(self):
        return ( 'Proximal operator associated to the divergence and temporal boundary condition constrain on a grid with shape :' +
                 str(self.M) + ' x ' +
                 str(self.N) + ' x ' +
                 str(self.P) )

    def __delattr__(self, nom_attr):
        raise AttributeError('You can not delete any attribute from this class : ProxCdivtempbound')

    def A_div_tb(self, grid):
        return grid.divTempBound()
               
    def T_A_div_tb(self, divTempBound):
        return divTempBound.T_divTempBound()

    def A_T_A_div_tb(self, divTempBound):
        return self.A_div_tb(self.T_A_div_tb(divTempBound))

    def inv_A_T_A_div_tb(self, divTempBound):
        # inverts operator A o T_A
        # this function modifies divTempBound

        divTempBound.applyGaussForward()

        div = divTempBound.div
        div = 0.5*fft.dct(div, axis=2)
        div = 0.5*fft.dst(div, axis=1, type=1)
        div = 0.5*fft.dst(div, axis=0, type=1)

        div = div / self.eigvalues_A_div_tb

        div = fft.idct(div, axis=2) / ( self.P + 1. )
        div = fft.dst(div, axis=1, type=1) / ( self.N + 2. )
        div = fft.dst(div, axis=0, type=1) / ( self.M + 2. )

        divTempBound.div = div
        divTempBound.applyGaussBackward()

        return divTempBound

    def __call__(self, grid):
        # projects StaggeredGrid grid on the divergence and temporal boundary condition constrain        
        divTempBound = self.A_div_tb(grid)
        divTempBound -= self.kernel
        divTempBound = self.inv_A_T_A_div_tb(divTempBound)
        gridP = self.T_A_div_tb(divTempBound)
        return ( grid - gridP )

    def test(self):
        divTB1 = DivergenceTempBound.random(self.M, self.N, self.P)
        e = 0.
        t = 0.

        divTB2 = divTB1.copy()
        time_start = tm.time()
        divTB2 = self.inv_A_T_A_div_tb(divTB2)
        divTB2 = self.A_T_A_div_tb(divTB2)
        t += tm.time() - time_start
        e += ( divTB1 - divTB2 ).LInftyNorm()

        divTB2 = divTB1.copy()
        time_start = tm.time()
        divTB2 = self.A_T_A_div_tb(divTB2)
        divTB2 = self.inv_A_T_A_div_tb(divTB2)
        t += tm.time() - time_start
        e += ( divTB1 - divTB2 ).LInftyNorm()
        return e, t

    def timing(self,nTiming):
        t = 0.
        for i in xrange(nTiming):
            grid = StaggeredGrid.random(self.M, self.N, self.P)
            time_start = tm.time()
            grid = self(grid)
            t += tm.time() - time_start
        return t
