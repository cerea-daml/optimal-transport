#################
# Class ProxCscrb
#################
#
# Projector on the staggered centered interpolation and boundary condition constrain with a reservoir
#

import time as tm
import numpy as np
from .. import projector as proj
from ...grid import grid

class ProxCscrb( proj.Projector ):
    '''
    Projector on the staggered centered interpolation and boundary condition constrain with a reservoir
    '''
    
    def __init__( self ,
                  N , P ,
                  kernel=None ):
        if kernel is None:
            kernel = grid.CenteredFieldBoundaries(N,P)

        proj.Projector.__init__( self ,
                                 N , P ,
                                 kernel )

        self.inverseATAm  = np.linalg.inv( self.ATAm() )
        self.inverseATAf  = np.linalg.inv( self.ATAf() )
        self.inverseATAfr = np.linalg.inv( self.ATAfr() )


    def ATAm(self):
        alpha = 0.5
        diag           = np.ones(self.N+1+2)+2*alpha**2
        diag[0]        = 1.
        diag[self.N+2] = 1.

        diagSup           = np.zeros(self.N+1+1)+alpha**2
        diagSup[0]        = -alpha
        diagSup[self.N+1] = -alpha

        return ( np.diag(diag) + np.diag(diagSup,-1) + np.diag(diagSup,1) )

    def ATAf(self):
        alpha = 0.5
        diag           = np.ones(self.P+1+2)+2*alpha**2
        diag[0]        = 1.
        diag[self.P+2] = 1.

        diagSup           = np.zeros(self.P+1+1)+alpha**2
        diagSup[0]        = -alpha
        diagSup[self.P+1] = -alpha

        return ( np.diag(diag) + np.diag(diagSup,-1) + np.diag(diagSup,1) )

    def ATAfr(self):
        alpha = 0.5
        diag    = np.ones(self.P+1+1)+2*alpha**2
        diag[0] = 1.

        diagSup    = np.zeros(self.P+1)+alpha**2
        diagSup[0] = -alpha

        return ( np.diag(diag) + np.diag(diagSup,-1) + np.diag(diagSup,1) )

    def __repr__(self):
        return ( 'Projector on the staggered centered interpolation and boundary contion constrain space with a reservoir.' )

    def A(self, scField):
        return scField.interpolationErrorReservoirBoundaries()

    def TA(self, cFieldb):
        return cFieldb.TinterpolationErrorReservoirBoundaries()

    def inverseATA(self, cFieldrb):
        m = np.zeros(shape=(self.N+3,self.P+1))
        m[0,:]          = cFieldrb.boundaries.spatialBoundaries.bx0[:]
        m[1:self.N+2,:] = cFieldrb.centeredField.m[0:self.N+1,:]
        m[self.N+2,:]   = cFieldrb.boundaries.spatialBoundaries.bx1[:]
        m = np.tensordot( self.inverseATAm , m , ([1],[0]) )

        fv  = np.zeros(shape=(self.N+1,self.P+1))
        bt0 = np.zeros(shape=(self.N+1))
        bt1 = np.zeros(shape=(self.N+1))

        # x = 0
        f             = np.zeros(shape=(self.P+2))
        f[0]          = cFieldrb.boundaries.temporalBoundaries.bt0[0]
        f[1:self.P+2] = cFieldrb.centeredField.f[0,0:self.P+1]
        f = np.tensordot( self.inverseATAfr , f , ([1],[0]) )

        bt0[0]           = f[0]
        fv[0,0:self.P+1] = f[1:self.P+2]

        # 0 < x < N
        f               = np.zeros(shape=(self.N-1,self.P+3))
        f[:,0]          = cFieldrb.boundaries.temporalBoundaries.bt0[1:self.N]
        f[:,1:self.P+2] = cFieldrb.centeredField.f[1:self.N,0:self.P+1]
        f[:,self.P+2]   = cFieldrb.boundaries.temporalBoundaries.bt1[1:self.N]
        f = np.tensordot( self.inverseATAf , f , ([1],[1]) ).transpose()

        bt0[1:self.N] = f[:,0]
        fv[1:self.N]  = f[:,1:self.P+2]
        bt1[1:self.N] = f[:,self.P+2]

        # x = N
        f             = np.zeros(shape=(self.P+2))
        f[0]          = cFieldrb.boundaries.temporalBoundaries.bt0[self.N]
        f[1:self.P+2] = cFieldrb.centeredField.f[self.N,0:self.P+1]
        f = np.tensordot( self.inverseATAfr , f , ([1],[0]) )

        bt0[self.N]           = f[0]
        fv[self.N,0:self.P+1] = f[1:self.P+2]

        cFieldrb.centeredField.m                   = m[1:self.N+2,:]
        cFieldrb.centeredField.f                   = fv
        cFieldrb.boundaries.spatialBoundaries.bx0  = m[0,:]
        cFieldrb.boundaries.spatialBoundaries.bx1  = m[self.N+2,:]
        cFieldrb.boundaries.temporalBoundaries.bt0 = bt0
        cFieldrb.boundaries.temporalBoundaries.bt1 = bt1

        return cFieldrb

    def test(self):
        field1 = grid.CenteredFieldBoundaries.random(self.N , self.P)
        field1.boundaries.temporalBoundaries.bt1[0]      = 0.
        field1.boundaries.temporalBoundaries.bt1[self.N] = 0.
        e = 0.

        field2 = field1.copy()
        field2 = self.inverseATA(field2)
        field2 = self.ATA(field2)
        e += ( field1 - field2 ).LInftyNorm()

        field2 = field1.copy()
        field2 = self.ATA(field2)
        field2 = self.inverseATA(field2)
        e += ( field1 - field2 ).LInftyNorm()

        return e

    def timing(self,nTiming):
        t = 0.
        for i in xrange(nTiming):
            field = grid.StaggeredCenteredField.random(self.N, self.P)
            time_start = tm.time()
            field = self(field)
            t += tm.time() - time_start
        return t
