#__________________________________________________
#__________________________________________________

# Copyrigth 2016 A. Farchi and M. Bocquet
# CEREA, joint laboratory Ecole des Ponts ParisTech and EDF R&D

# Code for the paper: Using the Wasserstein distance to compare fields of pollutants:
# Application to the radionuclide atmospheric dispersion of the Fukushima-Daiichi accident
# by A. Farchi, M. Bocquet, Y. Roustan, A. Mathieu and A. Querel

#__________________________________________________

#__________________________________________________
####################
# Class AdrAlgorithm
####################
#
# defines an ADR algorithm for a given configuration
#

from ..algorithm                  import Algorithm
from ...grid                      import grid
from ...init.initialFields        import initialStaggeredCenteredField
from ...proximals.defineProximals import proximalForConfig

from adrState import AdrState
from adrStep  import AdrStep
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

    def setState(self, newState, copy=True):
        if isinstance(newState, AdrState):
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
            z           = grid.StaggeredCenteredField( self.M , self.N , self.P ,
                                                       stagField, centField )
            w           = z.copy()
            self.stateN = AdrState( self.M , self.N , self.P , z , w )

        self.stateNP1 = self.stateN.copy()

    def initialize(self):
        Algorithm.initialize(self)

        if self.stateN is None:
            z = initialStaggeredCenteredField(self.config)
            w = z.copy()
            self.stateN   = AdrState( self.M , self.N , self.P , z , w )
            self.stateNP1 = self.stateN.copy()
