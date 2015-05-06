###################
# Class PdAlgorithm
###################
#
# defines a PD algorithm for a given configuration
#

from ..algorithm import Algorithm
from ...grid import grid
from ...init.initialFields import initialStaggeredField
from ...proximals.defineProximals import proximalForConfig

from pdState import PdState
from pdStep import PdStep
from proxPd import Prox1Pd
from proxPd import Prox2Pd

class PdAlgorithm( Algorithm ):
    '''
    class to handle a PD Algorithm
    '''

    def __init__(self, config):
        Algorithm.__init__(self, config)
        
        proxCdiv,proxCsc,proxJ,proxCb = proximalForConfig(config)
        prox1 = Prox1Pd(config, proxJ)
        prox2 = Prox2Pd(proxCdiv)
        self.stepFunction = PdStep(config, prox1, prox2)
        
    def __repr__(self):
        return ( 'PD algorithm' )

    def setState(self, newState):
        stagField = newState
        centField = stagField.interpolation()

        self.stateN = PdState( self.N , self.P , stagField , stagField.copy() , centField )
        self.stateNP1 = self.stateN.copy()

    def initialize(self):
        Algorithm.initialize(self)

        if self.stateN is None:
            u = initialStaggeredField(self.config)
            y = u.copy()
            v = u.interpolation()

            self.stateN = PdState( self.N , self.P , u , y , v )
            self.stateNP1 = self.stateN.copy()
    
