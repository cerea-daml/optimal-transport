#==================================================
#__________________________________________________

# Copyrigth 2016 A. Farchi and M. Bocquet
# CEREA, joint laboratory Ecole des Ponts ParisTech and EDF R&D

# Code for the paper: Using the Wasserstein distance to compare fields of pollutants:
# Application to the radionuclide atmospheric dispersion of the Fukushima-Daiichi accident
# by A. Farchi, M. Bocquet, Y. Roustan, A. Mathieu and A. Querel

#__________________________________________________
#==================================================

###############
# Class AdrStep
###############
#
# Step function for an ADR Algorithm
#

from ...grid import grid

class AdrStep:
    '''
    Step function for an ADR algorithm
    '''

    def __init__(self, config, prox1, prox2):
        self.prox1 = prox1
        self.prox2 = prox2
        self.alpha = config.alpha
        self.gamma = config.gamma

    def __repr__(self):
        return ( 'Step function for an ADR algorithm' )

    def __call__(self, stateN, stateNP1):
        stateNP1.w = stateN.w + self.alpha * ( self.prox1( 2 * stateN.z - stateN.w , self.gamma ) - stateN.z )
        stateNP1.z = self.prox2(stateNP1.w)
