#==================================================
#__________________________________________________

# Copyrigth 2016 A. Farchi and M. Bocquet
# CEREA, joint laboratory Ecole des Ponts ParisTech and EDF R&D

# Code for the paper: Using the Wasserstein distance to compare fields of pollutants:
# Application to the radionuclide atmospheric dispersion of the Fukushima-Daiichi accident
# by A. Farchi, M. Bocquet, Y. Roustan, A. Mathieu and A. Querel

#__________________________________________________
#==================================================

###################
# Class PdAlgorithm
###################
#
# defines a PD algorithm for a given configuration
#

from ..algorithm                  import Algorithm
from ...grid                      import grid
from ...init.initialFields        import initialStaggeredField
from ...proximals.defineProximals import proximalForConfig

from .pdState import PdState
from .pdStep  import PdStep
from .proxPd  import Prox1Pd
from .proxPd  import Prox2Pd

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

    def setState(self, newState, copy=True):
        if isinstance(newState, PdState):
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
            self.stateN = PdState( self.M , self.N , self.P , stagField , stagField.copy() , centField )

        self.stateNP1 = self.stateN.copy()

    def initialize(self):
        Algorithm.initialize(self)

        if self.stateN is None:
            u = initialStaggeredField(self.config)
            y = u.copy()
            v = u.interpolation()

            self.stateN = PdState( self.M , self.N , self.P , u , y , v )
            self.stateNP1 = self.stateN.copy()
    
