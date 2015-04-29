#################
# Class ProxCdivb
#################
#
# Projector on the divergence and boundary conditions constrain
#

import time as tm
import numpy as np
import scipy.fftpack as fft
from .. import projector as proj
from ...grid import grid

class ProxCdivb( proj.Projector ):
    '''
    Projector on the divergence and boundary conditions constrain
    '''
    
    def __init__( self ,
                  N , P ,
                  kernel=None ):
        if kernel is None:
            kernel = grid.DivergenceBoundaries(N,P)

        proj.Projector.__init__( self ,
                                 N , P ,
                                 kernel )

        x = np.arange(N+1)
        t = np.arange(P+1)

        X,T = np.meshgrid(x,t,indexing='ij')
        self.eigvalues = ( 2. * (N**2) * ( 1. - np.cos( np.pi * X / ( N + 1. ) ) ) +
                           2. * (P**2) * ( 1. - np.cos( np.pi * T / ( P + 1. ) ) ) )

        self.eigvalues[0,0] = 1.

    def __repr__(self):
        return ( 'Projector on the divergence and boundary conditions constrain space.' )

    def A(self, field):
        return field.divergenceBoundaries()

    def TA(self, div):
        return div.TdivergenceBoundaries()

    def inverseATA(self, divBound):
        divBound.applyGaussForward()

        div = divBound.divergence.div
        div = 0.5*fft.dct(div, axis=0)
        div = 0.5*fft.dct(div, axis=1)

        div[0,0] = 0.0
        div = div / self.eigvalues

        div = fft.idct(div, axis=0) / ( self.N + 1. )
        div = fft.idct(div, axis=1) / ( self.P + 1. )

        divBound.divergence.div = div
        divBound.applyGaussBackward()

        return divBound

    def testInverse(self,nTest):
        EPS = 1e-8
        e = 0.

        for i in xrange(nTest):
            divB1 = grid.DivergenceBoundaries.random( self.N , self.P )
            divB1.correctMassDefault(EPS)

            divB2 = divB1.copy()
            divB2 = self.inverseATA(divB2)
            divB2 = self.ATA(divB2)
            e += ( divB1 - divB2 ).LInftyNorm()

            divB2 = divB1.copy()
            divB2 = self.ATA(divB2)
            divB2 = self.inverseATA(divB2)

            diff = divB2.divergence.div[0,0] - divB1.divergence.div[0,0]

            divB3 = grid.DivergenceBoundaries.ones(self.N,self.P)
            e += ( divB1 - divB2 + diff*divB3 ).LInftyNorm()
        return e/nTest

    def test(self,nTest):
        e = 0.
        for i in xrange(nTest):
            field = grid.StaggeredField.random(self.N, self.P)

            db = field.divergenceBoundaries()
            #db -= self.kernel
            db2 = self.inverseATA(db)
            f2 = db2.TdivergenceBoundaries()
            fp = field - f2
            e += (fp.divergenceBoundaries()).LInftyNorm()

            #Avector  = self.A( vector )
            #Avector -= self.kernel
            #Avector  = self.inverseATA( Avector )
            #Avector  = self.TA( Avector )
            #return ( vector - Avector )

            #field = self(field)
            #e += ( self.A(field) - self.kernel ).LInftyNorm()
        return e/nTest

    def timing(self,nTiming):
        t = 0.
        for i in xrange(nTiming):
            field = grid.StaggeredField.random(self.N, self.P)
            time_start = tm.time()
            field = self(field)
            t += tm.time() - time_start
        return t
