#==================================================
#__________________________________________________

# Copyrigth 2016 A. Farchi and M. Bocquet
# CEREA, joint laboratory Ecole des Ponts ParisTech and EDF R&D

# Code for the paper: Using the Wasserstein distance to compare fields of pollutants:
# Application to the radionuclide atmospheric dispersion of the Fukushima-Daiichi accident
# by A. Farchi, M. Bocquet, Y. Roustan, A. Mathieu and A. Querel

#__________________________________________________
#==================================================

#################
# Class ProxCdivb
#################
#
# Projector on the divergence and boundary conditions constrain
#

import time as tm
import numpy as np
import scipy.fftpack as fft
from ..projector import Projector
from ...grid import grid

class ProxCdivb( Projector ):
    '''
    Projector on the divergence and boundary conditions constrain
    '''
    
    def __init__( self ,
                  M , N , P ,
                  kernel=None ):
        if kernel is None:
            kernel = grid.DivergenceBoundaries(M,N,P)

        Projector.__init__( self ,
                            M , N , P ,
                            kernel )

        x = np.arange(M+1)
        y = np.arange(N+1)
        t = np.arange(P+1)

        X,Y,T = np.meshgrid(x,y,t,indexing='ij')
        self.eigvalues = ( 2. * (M**2) * ( 1. - np.cos( np.pi * X / ( M + 1. ) ) ) +
                           2. * (N**2) * ( 1. - np.cos( np.pi * Y / ( N + 1. ) ) ) +
                           2. * (P**2) * ( 1. - np.cos( np.pi * T / ( P + 1. ) ) ) )

        self.eigvalues[0,0,0] = 1.

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
        div = 0.5*fft.dct(div, axis=2)

        div[0,0,0] = 0.0
        div = div / self.eigvalues

        div = fft.idct(div, axis=0) / ( self.M + 1. )
        div = fft.idct(div, axis=1) / ( self.N + 1. )
        div = fft.idct(div, axis=2) / ( self.P + 1. )

        divBound.divergence.div = div
        divBound.applyGaussBackward()

        return divBound

    def testInverse(self,nTest):
        EPS = 1e-8
        e = 0.

        for i in xrange(nTest):
            divB1 = grid.DivergenceBoundaries.random(self.M, self.N, self.P)
            divB1.correctMassDefault(EPS)

            divB2 = divB1.copy()
            divB2 = self.inverseATA(divB2)
            divB2 = self.ATA(divB2)
            e += ( divB1 - divB2 ).LInftyNorm()

            divB2 = divB1.copy()
            divB2 = self.ATA(divB2)
            divB2 = self.inverseATA(divB2)

            diff = divB2.divergence.div[0,0,0] - divB1.divergence.div[0,0,0]

            divB3 = grid.DivergenceBoundaries.ones(self.M, self.N, self.P)
            e += ( divB1 - divB2 + diff*divB3 ).LInftyNorm()
        return e/nTest

    def test(self,nTest):
        e = 0.
        for i in xrange(nTest):
            field = grid.StaggeredField.random(self.M, self.N, self.P)

            db = field.divergenceBoundaries()
            db2 = self.inverseATA(db)
            f2 = db2.TdivergenceBoundaries()
            fp = field - f2
            e += (fp.divergenceBoundaries()).LInftyNorm()

        return e/nTest

    def timing(self,nTiming):
        t = 0.
        for i in xrange(nTiming):
            field = grid.StaggeredField.random(self.M, self.N, self.P)
            time_start = tm.time()
            field = self(field)
            t += tm.time() - time_start
        return t
