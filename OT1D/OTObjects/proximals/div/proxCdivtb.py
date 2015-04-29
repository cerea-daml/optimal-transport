##################
# Class ProxCdivtb
##################
#
# Projector on the divergence and temporal boundary conditions constrain
#

import time as tm
import numpy as np
import scipy.fftpack as fft
from .. import projector as proj
from ...grid import grid

class ProxCdivtb( proj.Projector ):
    '''
    Projector on the divergence and temporal boundary conditions constrain
    '''
    
    def __init__( self ,
                  N , P ,
                  kernel=None ):
        if kernel is None:
            kernel = grid.DivergenceTemporalBoundaries(N,P)

        proj.Projector.__init__( self ,
                                 N , P ,
                                 kernel )

        x = np.arange(N+1)
        t = np.arange(P+1)

        X,T = np.meshgrid(x,t,indexing='ij')

        self.eigvalues = ( 2. * (N**2) * ( 1. - np.cos( np.pi * ( X + 1. ) / ( N + 2. ) ) ) +
                           2. * (P**2) * ( 1. - np.cos( np.pi *   T        / ( P + 1. ) ) ) )

    def __repr__(self):
        return ( 'Projector on the divergence and temporal boundary conditions constrain space.' )

    def A(self, field):
        return field.divergenceTemporalBoundaries()

    def TA(self, div):
        return div.TdivergenceTemporalBoundaries()

    def inverseATA(self, divTempBound):
        divTempBound.applyGaussForward()

        div = divTempBound.divergence.div
        div = 0.5*fft.dct(div, axis=1)
        div = 0.5*fft.dst(div, axis=0, type=1)

        div = div / self.eigvalues

        div = fft.idct(div, axis=1) / ( self.P + 1. )
        div = fft.dst(div, axis=0, type=1) / ( self.N + 2. )

        divTempBound.divergence.div = div
        divTempBound.applyGaussBackward()

        return divTempBound

    def testInverse(self,nTest):
        e = 0.

        for i in xrange(nTest):
            divTB1 = grid.DivergenceTemporalBoundaries.random( self.N , self.P )
            
            divTB2 = divTB1.copy()
            divTB2 = self.inverseATA(divTB2)
            divTB2 = self.ATA(divTB2)
            e += ( divTB1 - divTB2 ).LInftyNorm()

            divTB2 = divTB1.copy()
            divTB2 = self.ATA(divTB2)
            divTB2 = self.inverseATA(divTB2)
            e += ( divTB1 - divTB2 ).LInftyNorm()

        return e/nTest

    def test(self,nTest):
        e = 0.
        for i in xrange(nTest):
            field = grid.StaggeredField.random(self.N, self.P)
            field = self(field)
            e += ( self.A(field) - self.kernel ).LInftyNorm()
        return e/nTest

    def timing(self,nTiming):
        t = 0.
        for i in xrange(nTiming):
            field = grid.StaggeredField.random(self.N, self.P)
            time_start = tm.time()
            field = self(field)
            t += tm.time() - time_start
        return t
