###############
# Class ProxCtb
###############
#
# Projector on the temporal boundary condition constrain
#

import time as tm
from .. import projector as proj
from ...grid import grid

class ProxCtb( proj.Projector ):
    '''
    Projector on the temporal boundary condition constrain
    '''
    
    def __init__( self ,
                  N , P ,
                  kernel=None ):
        if kernel is None:
            kernel = grid.TemporalBoundaries(N,P)

        proj.Projector.__init__( self ,
                                 N , P ,
                                 kernel )

    def __repr__(self):
        return ( 'Projector on the temporal boundary contion constrain space.' )

    def __call__(self, field, overwrite=True):
        if overwrite:
            field.f[:,0]        = self.kernel.bt0[:]
            field.f[:,self.P+1] = self.kernel.bt1[:]
            return field
        else:
            return self(field.copy(), True)

    def timing(self,nTiming,overwrite=True):
        t = 0.
        for i in xrange(nTiming):
            field = grid.StaggeredField.random(self.N, self.P)
            time_start = tm.time()
            field = self(field,overwrite)
            t += tm.time() - time_start
        return t
