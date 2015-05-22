#####################
# Class Adr3Algorithm
#####################
#
# defines an ADR3 algorithm for a given configuration
#

from ..algorithm                  import Algorithm
from ...grid                      import grid
from ...init.initialFields        import initialStaggeredCenteredField
from ...proximals.defineProximals import proximalForConfig

from adr3State import Adr3State
from adr3Step  import Adr3Step
from proxAdr3  import Prox1Adr3
from proxAdr3  import Prox2Adr3
from proxAdr3  import Prox3Adr3

class Adr3Algorithm( Algorithm ):
    '''
    class to handle an ADR3 Algorithm
    '''

    def __init__(self, config):
        Algorithm.__init__(self, config)
        
        proxCdiv,proxCsc,proxJ,proxCb = proximalForConfig(config)
        prox1 = Prox1Adr3(config, proxCdiv, proxJ)
        prox2 = Prox2Adr3(proxCsc)
        prox3 = Prox3Adr3(config, proxCb)
        self.stepFunction = Adr3Step(config, prox1, prox2, prox3)
        
    def __repr__(self):
        return ( 'ADR3 algorithm' )

    def setState(self, newState, copy=True):
        if isinstance(newState, Adr3State):
            if copy:
                self.stateN = newState.copy()
            else:
                self.stateN = newState
        else:
            if copy:
                stagField = newState.convergingStaggeredField().copy()
            else:
                stagField = newState.convergingStaggeredField()

            centField   = stagField.interpolation()
            u1          = grid.StaggeredCenteredField( self.M , self.N , self.P ,
                                                        stagField, centField )
        
            self.stateN = Adr3State( self.M , self.N , self.P , u1 , u1.copy() , u1.copy() , u1.copy() )

        self.stateNP1 = self.stateN.copy()

    def initialize(self):
        Algorithm.initialize(self)

        if self.stateN is None:
            u1 = initialStaggeredCenteredField(self.config)
            self.stateN   = Adr3State( self.M , self.N , self.P , u1 , u1.copy() , u1.copy() , u1.copy() )
            self.stateNP1 = self.stateN.copy()
