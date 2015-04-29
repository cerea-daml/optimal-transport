###############
# Class ProxCsc
###############
#
# Projector on the staggered centered interpolation constrain
#

import time as tm
import numpy as np
from .. import projector as proj
from ...grid import grid

class ProxCsc( proj.Projector ):
    '''
    Projector on the staggered centered interpolation constrain
    '''
    
    def __init__( self ,
                  N , P ,
                  kernel=None ):
        if kernel is None:
            kernel = grid.CenteredField(N,P)

        proj.Projector.__init__( self ,
                                 N , P ,
                                 kernel )

        self.inverseATAm = np.linalg.inv( self.ATAm() )
        self.inverseATAf = np.linalg.inv( self.ATAf() )

    def ATAm(self):
        alpha   = 0.5
        diag    = np.ones(self.N+1) + 2.*alpha**2
        diagSup = np.zeros(self.N) + alpha**2
        return ( np.diag(diag) + np.diag(diagSup,-1) + np.diag(diagSup,1) )

    def ATAf(self):
        alpha   = 0.5
        diag    = np.ones(self.P+1) + 2.*alpha**2
        diagSup = np.zeros(self.P) + alpha**2
        return ( np.diag(diag) + np.diag(diagSup,-1) + np.diag(diagSup,1) )

    def __repr__(self):
        return ( 'Projector on the staggered centered interpolation constrain space.' )

    def A(self, scField):
        return scField.interpolationError()

    def TA(self, cField):
        return cField.TinterpolationError()

    def inverseATA(self, cField):
        cField.m = np.tensordot( self.inverseATAm , cField.m , ([1],[0]))
        cField.f = np.tensordot( self.inverseATAf , cField.f , ([1],[1])).transpose()
        return cField

    def testInverse(self,nTest):
        e = 0.
        for i in xrange(nTest):
            field1 = grid.CenteredField.random(self.N , self.P)

            field2 = field1.copy()
            field2 = self.inverseATA(field2)
            field2 = self.ATA(field2)
            e += ( field1 - field2 ).LInftyNorm()

            field2 = field1.copy()
            field2 = self.ATA(field2)
            field2 = self.inverseATA(field2)
            e += ( field1 - field2 ).LInftyNorm()

        return e/nTest

    def test(self,nTest):
        e = 0.
        for i in xrange(nTest):
            field = grid.StaggeredCenteredField.random(self.N, self.P)
            field = self(field)
            e += ( self.A(field) - self.kernel ).LInftyNorm()
        return e/nTest

    def timing(self,nTiming):
        t = 0.
        for i in xrange(nTiming):
            field = grid.StaggeredCenteredField.random(self.N, self.P)
            time_start = tm.time()
            field = self(field)
            t += tm.time() - time_start
        return t
