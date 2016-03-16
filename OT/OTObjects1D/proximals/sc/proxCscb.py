#==================================================
#__________________________________________________

# Copyrigth 2016 A. Farchi and M. Bocquet
# CEREA, joint laboratory Ecole des Ponts ParisTech and EDF R&D

# Code for the paper: Using the Wasserstein distance to compare fields of pollutants:
# Application to the radionuclide atmospheric dispersion of the Fukushima-Daiichi accident
# by A. Farchi, M. Bocquet, Y. Roustan, A. Mathieu and A. Querel

#__________________________________________________
#==================================================

################
# Class ProxCscb
################
#
# Projector on the staggered centered interpolation and boundary condition constrain
#

import time as tm
import numpy as np
from .. import projector as proj
from ...grid import grid

class ProxCscb( proj.Projector ):
    '''
    Projector on the staggered centered interpolation and boundary condition constrain
    '''
    
    def __init__( self ,
                  N , P ,
                  kernel=None ):
        if kernel is None:
            kernel = grid.CenteredFieldBoundaries(N,P)

        proj.Projector.__init__( self ,
                                 N , P ,
                                 kernel )

        self.inverseATAm = np.linalg.inv( self.ATAm() )
        self.inverseATAf = np.linalg.inv( self.ATAf() )

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

    def __repr__(self):
        return ( 'Projector on the staggered centered interpolation and boundary contion constrain space.' )

    def A(self, scField):
        return scField.interpolationErrorBoundaries()

    def TA(self, cFieldb):
        return cFieldb.TinterpolationErrorBoundaries()

    def inverseATA(self, cFieldb):
        m = np.zeros(shape=(self.N+3,self.P+1))
        m[0,:]          = cFieldb.boundaries.spatialBoundaries.bx0[:]
        m[1:self.N+2,:] = cFieldb.centeredField.m[0:self.N+1,:]
        m[self.N+2,:]   = cFieldb.boundaries.spatialBoundaries.bx1[:]
        m = np.tensordot( self.inverseATAm , m , ([1],[0]) )

        f = np.zeros(shape=(self.N+1,self.P+3))
        f[:,0]          = cFieldb.boundaries.temporalBoundaries.bt0[:]
        f[:,1:self.P+2] = cFieldb.centeredField.f[:,0:self.P+1]
        f[:,self.P+2]   = cFieldb.boundaries.temporalBoundaries.bt1[:]
        f = np.tensordot( self.inverseATAf , f , ([1],[1]) ).transpose()

        cFieldb.centeredField.m                   = m[1:self.N+2,:]
        cFieldb.centeredField.f                   = f[:,1:self.P+2]
        cFieldb.boundaries.spatialBoundaries.bx0  = m[0,:]
        cFieldb.boundaries.spatialBoundaries.bx1  = m[self.N+2,:]
        cFieldb.boundaries.temporalBoundaries.bt0 = f[:,0]
        cFieldb.boundaries.temporalBoundaries.bt1 = f[:,self.P+2]

        return cFieldb

    def testInverse(self,nTest):
        e = 0.
        for i in range(nTest):
            field1 = grid.CenteredFieldBoundaries.random(self.N , self.P)

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
        for i in range(nTest):
            field = grid.StaggeredCenteredField.random(self.N, self.P)
            field = self(field)
            e += ( self.A(field) - self.kernel ).LInftyNorm()
        return e/nTest

    def timing(self,nTiming):
        t = 0.
        for i in range(nTiming):
            field = grid.StaggeredCenteredField.random(self.N, self.P)
            time_start = tm.time()
            field = self(field)
            t += tm.time() - time_start
        return t
