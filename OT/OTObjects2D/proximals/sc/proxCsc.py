#==================================================
#__________________________________________________

# Copyrigth 2016 A. Farchi and M. Bocquet
# CEREA, joint laboratory Ecole des Ponts ParisTech and EDF R&D

# Code for the paper: Using the Wasserstein distance to compare fields of pollutants:
# Application to the radionuclide atmospheric dispersion of the Fukushima-Daiichi accident
# by A. Farchi, M. Bocquet, Y. Roustan, A. Mathieu and A. Querel

#__________________________________________________
#==================================================

###############
# Class ProxCsc
###############
#
# Projector on the staggered centered interpolation constrain
#

import time as tm
import numpy as np
from ..projector import Projector
from ...grid import grid

class ProxCsc( Projector ):
    '''
    Projector on the staggered centered interpolation constrain
    '''
    
    def __init__( self ,
                  M , N , P ,
                  kernel=None ):
        if kernel is None:
            kernel = grid.CenteredField(M,N,P)

        Projector.__init__( self ,
                            M , N , P ,
                            kernel )

        self.inverseATAmx = np.linalg.inv( self.ATAmx() )
        self.inverseATAmy = np.linalg.inv( self.ATAmy() )
        self.inverseATAf  = np.linalg.inv( self.ATAf() )

    def ATAmx(self):
        alpha   = 0.5
        diag    = np.ones(self.M+1) + 2.*alpha**2
        diagSup = np.zeros(self.M) + alpha**2
        return ( np.diag(diag) + np.diag(diagSup,-1) + np.diag(diagSup,1) )

    def ATAmy(self):
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
        cField.mx = np.tensordot( self.inverseATAmx , cField.mx , ([1],[0]))
        cField.my = np.tensordot( self.inverseATAmy , cField.my , ([1],[1])).transpose((1,0,2))
        cField.f  = np.tensordot( self.inverseATAf  , cField.f  , ([1],[2])).transpose((1,2,0))
        return cField

    def testInverse(self,nTest):
        e = 0.
        for i in range(nTest):
            field1 = grid.CenteredField.random(self.M, self.N , self.P)

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
            field = grid.StaggeredCenteredField.random(self.M, self.N, self.P)
            field = self(field)
            e += ( self.A(field) - self.kernel ).LInftyNorm()
        return e/nTest

    def timing(self,nTiming):
        t = 0.
        for i in range(nTiming):
            field = grid.StaggeredCenteredField.random(self.M, self.N, self.P)
            time_start = tm.time()
            field = self(field)
            t += tm.time() - time_start
        return t
