###############
# Class AdrStep
###############
#
# Step function for an ADR Algorithm
#

from .. import OTObject as oto
from ..grid import grid

class AdrStep:
    '''
    Step function for an ADR algorithm
    '''

    def __init__(self, prox1, prox2, alpha):
        self.prox1 = prox1
        self.prox2 = prox2
        self.alpha = alpha

    def __repr__(self):
        return ( 'Step function for an ADR algorithm' )

    def __call__(self, stateN, stateNP1):
        stateNP1.w = stateN.w + self.alpha * ( self.prox1( 2 * stateN.z - stateN.w ) - stateN.z )
        stateNP1.z = self.prox2(stateNP1.w)
