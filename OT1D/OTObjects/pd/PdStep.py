###############
# Class PdStep
###############
#
# Step function for a PD Algorithm
#

from .. import OTObject as oto
from ..grid import grid

class PdStep:
    '''
    Step function for a PD algorithm
    '''

    def __init__(self, config, prox1, prox2):
        self.prox1 = prox1
        self.prox2 = prox2
        self.sigma = config.sigma
        self.tau   = config.tau
        self.theta = config.theta

    def __repr__(self):
        return ( 'Step function for a PD algorithm' )

    def __call__(self, stateN, stateNP1):
        stateNP1.v = self.prox1( stateN.v + ( self.sigma * stateN.y.interpolation() ) )
        stateNP1.u = self.prox2( stateN.u - ( self.tau * stateNP1.v.Tinterpolation() ) ) 
        stateNP1.y = ( ( ( 1. + self.theta ) * stateNP1.u ) - 
                       ( self.theta * stateN.u ) )


