####################
# Class AdrAlgorithm
####################
#
# defines an ADR algorithm for a given configuration
#

from ..algorithm import Algorithm
from ...grid import grid
from ...init.initialFields import initialStaggeredCenteredField
from ...proximals.defineProximals import proximalForConfig

from adrState import AdrState
from adrStep import AdrStep
from prox1Adr import Prox1Adr

class AdrAlgorithm( Algorithm ):
    '''
    class to handle an ADR Algorithm
    '''

    def __init__(self, config):
        Algorithm.__init__(self, config)
        
        proxCdiv,proxCsc,proxJ,proxCb = proximalForConfig(config)
        prox1 = Prox1Adr(config, proxCdiv, proxJ)
        self.stepFunction = AdrStep(config, prox1, proxCsc)
        
    def __repr__(self):
        return ( 'ADR algorithm' )

    def setState(self, newState):
        stagField = newState.convergingStaggeredField()
        centField = stagField.interpolation()
        z = grid.StaggeredCenteredField( self.config.N , self.config.P ,
                                         stagField, centField )
        w = z.copy()
        self.stateN = AdrState( self.config.N , self.config.P , z , w )
        self.stateNP1 = self.stateN.copy()

    def initialize(self):
        Algorithm.initialize(self)

        if self.stateN is None:
            z = initialStaggeredCenteredField(self.config)
            w = z.copy()
            self.stateN   = AdrState( self.N , self.P , z , w )
            self.stateNP1 = self.stateN.copy()
