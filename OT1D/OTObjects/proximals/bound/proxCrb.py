###############
# Class ProxCrb
###############
#
# Projector on the boundary condition constrain with reservoir
#

import time as tm
from .. import projector as proj
from ...grid import grid

class ProxCrb( proj.Projector ):
    '''
    Projector on the boundary condition constrain with reservoir
    '''
    
    def __init__( self ,
                  N , P ,
                  kernel=None ):
        if kernel is None:
            kernel = grid.Boundaries(N,P)

        self.massDefault = kernel.massDefault()
        proj.Projector.__init__( self ,
                                 N , P ,
                                 kernel )

    def __repr__(self):
        return ( 'Projector on the boundary contion constrain space with reservoir.' )

    def __call__(self, field, overwrite=True):
        if overwrite:
            field.m[0,:]        = self.kernel.spatialBoundaries.bx0[:]
            field.m[self.N+1,:] = self.kernel.spatialBoundaries.bx1[:]

            field.f[1:self.N,0]        = self.kernel.temporalBoundaries.bt0[1:self.N]
            field.f[1:self.N,self.P+1] = self.kernel.temporalBoundaries.bt1[1:self.N]

            field.f[0,0]      = 0.
            field.f[self.N,0] = 0.

            deltaMassCurrent = field.boundaries().massDefault() - self.massDefault

            deltaMassCurrent /= 2. * self.P

            field.f[0,self.P+1]      += deltaMassCurrent
            field.f[self.N,self.P+1] += deltaMassCurrent

            return field
        else:
            return self(field.copy(), True)

    def test(self):
        field = grid.StaggeredField.random(self.N, self.P)
        field = self(field)

        diff = field.boundaries() - self.kernel
        diff.temporalBoundaries.bt0[0] = 0.
        diff.temporalBoundaries.bt1[0] = 0.
        diff.temporalBoundaries.bt0[self.N] = 0.
        diff.temporalBoundaries.bt1[self.N] = 0.
        
        return ( diff.LInftyNorm() + abs( field.boundaries().massDefault() - self.massDefault ) )

    def timing(self,nTiming,overwrite=True):
        t = 0.
        for i in xrange(nTiming):
            field = grid.StaggeredField.random(self.N, self.P)
            time_start = tm.time()
            field = self(field,overwrite)
            t += tm.time() - time_start
        return t
