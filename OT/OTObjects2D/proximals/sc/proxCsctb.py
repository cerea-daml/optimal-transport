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
# Class ProxCsctb
#################
#
# Projector on the staggered centered interpolation and temporal boundary condition constrain
#

import time as tm
import numpy as np
from ..projector import Projector
from ...grid import grid

class ProxCsctb( Projector ):
    '''
    Projector on the staggered centered interpolation and temporal boundary condition constrain
    '''
    
    def __init__( self ,
                  M , N , P ,
                  kernel=None ):
        if kernel is None:
            kernel = grid.CenteredFieldTemporalBoundaries(M,N,P)

        Projector.__init__( self ,
                            M , N , P ,
                            kernel )

        self.inverseATAmx = np.linalg.inv( self.ATAmx() )
        self.inverseATAmy = np.linalg.inv( self.ATAmy() )
        self.inverseATAf  = np.linalg.inv( self.ATAf() )

    def ATAmx(self):
        alpha = 0.5
        diag    = np.ones(self.M+1)+2*alpha**2
        diagSup = np.zeros(self.M)+alpha**2
        return ( np.diag(diag) + np.diag(diagSup,-1) + np.diag(diagSup,1) )

    def ATAmy(self):
        alpha = 0.5
        diag    = np.ones(self.N+1)+2*alpha**2
        diagSup = np.zeros(self.N)+alpha**2
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
        return ( 'Projector on the staggered centered interpolation and temporal boundary contion constrain space.' )

    def A(self, scField):
        return scField.interpolationErrorTemporalBoundaries()

    def TA(self, cFieldtb):
        return cFieldtb.TinterpolationErrorTemporalBoundaries()

    def inverseATA(self, cFieldtb):
        cFieldtb.centeredField.mx = np.tensordot( self.inverseATAmx , cFieldtb.centeredField.mx , ([1],[0]) )
        cFieldtb.centeredField.my = np.tensordot( self.inverseATAmy , cFieldtb.centeredField.my , ([1],[1]) ).transpose((1,0,2))

        f = np.zeros(shape=(self.M+1,self.N+1,self.P+3))
        f[:,:,0]          = cFieldtb.temporalBoundaries.bt0[:,:]
        f[:,:,1:self.P+2] = cFieldtb.centeredField.f[:,:,0:self.P+1]
        f[:,:,self.P+2]   = cFieldtb.temporalBoundaries.bt1[:,:]
        f = np.tensordot( self.inverseATAf , f , ([1],[2]) ).transpose((1,2,0))

        cFieldtb.centeredField.f        = f[:,:,1:self.P+2]
        cFieldtb.temporalBoundaries.bt0 = f[:,:,0]
        cFieldtb.temporalBoundaries.bt1 = f[:,:,self.P+2]

        return cFieldtb

    def testInverse(self,nTest):
        e = 0.
        for i in range(nTest):
            field1 = grid.CenteredFieldTemporalBoundaries.random(self.M, self.N , self.P)
            
            field2 = field1.copy()
            field2 = self.inverseATA(field2)
            field2 = self.ATA(field2)
            e += ( field1 - field2 ).LInftyNorm()
            
            field2 = field1.copy()
            field2 = self.ATA(field2)
            field2 = self.inverseATA(field2)        
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
