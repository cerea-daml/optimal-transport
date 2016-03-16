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
# Class ProxCrb
###############
#
# Projector on the boundary condition constrain with reservoir
#

import time as tm
from ..projector import Projector
from ...grid import grid

class ProxCrb( Projector ):
    '''
    Projector on the boundary condition constrain with reservoir
    '''
    
    def __init__( self ,
                  M , N , P ,
                  kernel=None ):
        if kernel is None:
            kernel = grid.Boundaries(M,N,P)

        self.massDefault = kernel.massDefault()
        Projector.__init__( self ,
                            M , N , P ,
                            kernel )

    def __repr__(self):
        return ( 'Projector on the boundary contion constrain space with reservoir.' )

    def __call__(self, field, overwrite=True):
        if overwrite:
            field.mx[0,:,:]        = self.kernel.spatialBoundaries.bx0[:,:]
            field.mx[self.M+1,:,:] = self.kernel.spatialBoundaries.bx1[:,:]
            field.my[:,0,:]        = self.kernel.spatialBoundaries.by0[:,:]
            field.my[:,self.N+1,:] = self.kernel.spatialBoundaries.by1[:,:]

            field.f[1:self.M,1:self.N,0]        = self.kernel.temporalBoundaries.bt0[1:self.M,1:self.N]
            field.f[1:self.M,1:self.N,self.P+1] = self.kernel.temporalBoundaries.bt1[1:self.M,1:self.N]

            field.f[0,:,0]      = 0.
            field.f[self.M,:,0] = 0.
            field.f[:,0,0]      = 0.
            field.f[:,self.N,0] = 0.

            # Trying to correct mass default...
            # should accelerate convergence
            # but this version lacks of a non-zero filter !
            #deltaMassCurrent = field.boundaries().massDefault()
            #deltaMassCurrent /= 2. * ( self.M + self.N ) * self.P

            #field.f[0,:,self.P+1]             += deltaMassCurrent
            #field.f[self.M,:,self.P+1]        += deltaMassCurrent
            #field.f[1:self.M,0,self.P+1]      += deltaMassCurrent
            #field.f[1:self.M,self.N,self.P+1] += deltaMassCurrent

            return field
        else:
            return self(field.copy(), True)

    def test(self,nTest,overwrite=True):
        e = 0.
        for i in xrange(nTest):
            field = grid.StaggeredField.random(self.M, self.N, self.P)
            field = self(field,overwrite)

            diff = field.boundaries() - self.kernel

            diff.temporalBoundaries.bt0[0,:]      = 0.
            diff.temporalBoundaries.bt0[self.M,:] = 0.
            diff.temporalBoundaries.bt0[:,0]      = 0.
            diff.temporalBoundaries.bt0[:,self.N] = 0.

            diff.temporalBoundaries.bt1[0,:]      = 0.
            diff.temporalBoundaries.bt1[self.M,:] = 0.
            diff.temporalBoundaries.bt1[:,0]      = 0.
            diff.temporalBoundaries.bt1[:,self.N] = 0.
        
            e += ( diff.LInftyNorm() + abs( field.boundaries().massDefault() - self.massDefault ) )
        return e/nTest

    def timing(self,nTiming,overwrite=True):
        t = 0.
        for i in xrange(nTiming):
            field = grid.StaggeredField.random(self.M, self.N, self.P)
            time_start = tm.time()
            field = self(field,overwrite)
            t += tm.time() - time_start
        return t
