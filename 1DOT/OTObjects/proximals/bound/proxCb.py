##############
# Class ProxCb
##############
#
# Projector on the boundary condition constrain
#

import time as tm
from .. import projector as proj
from ...grid import grid

class ProxCb( proj.Projector ):
    '''
    Projector on the boundary condition constrain
    '''
    
    def __init__( self ,
                  N , P ,
                  kernel=None ):
        if kernel is None:
            kernel = grid.Boundaries(N,P)

        proj.Projector.__init__( self ,
                                 N , P ,
                                 kernel )

    def __repr__(self):
        return ( 'Projector on the boundary contion constrain space.' )

    def __call__(self, field, overwrite=True):
        if overwrite:
            field.m[0,:]        = self.kernel.spatialBoundaries.bx0[:]
            field.m[self.N+1,:] = self.kernel.spatialBoundaries.bx1[:]
            field.f[:,0]        = self.kernel.temporalBoundaries.bt0[:]
            field.f[:,self.P+1] = self.kernel.temporalBoundaries.bt1[:]
            return grid
        else:
            return self(grid.copy(), True)

    def timing(self,nTiming):
        t = 0.
        for i in xrange(nTiming):
            field = grid.StaggeredField.random(self.N, self.P)
            time_start = tm.time()
            field = self(field)
            t += tm.time() - time_start
        return t
