#__________________________________________________
#__________________________________________________

# Copyrigth 2016 A. Farchi and M. Bocquet
# CEREA, joint laboratory Ecole des Ponts ParisTech and EDF R&D

# Code for the paper: Using the Wasserstein distance to compare fields of pollutants:
# Application to the radionuclide atmospheric dispersion of the Fukushima-Daiichi accident
# by A. Farchi, M. Bocquet, Y. Roustan, A. Mathieu and A. Querel

#__________________________________________________

#__________________________________________________
################
# Class Adr3Step
################
#
# Step function for an ADR3 Algorithm
#

from ...grid import grid

class Adr3Step:
    '''
    Step function for an ADR3 algorithm
    '''

    def __init__(self, config, prox1, prox2, prox3):
        self.prox1 = prox1
        self.prox2 = prox2
        self.prox3 = prox3

        self.alpha  = config.alpha3
        self.gamma  = config.gamma3
        self.omega1 = config.omega1
        self.omega2 = config.omega2
        self.omega3 = config.omega3

    def __repr__(self):
        return ( 'Step function for an ADR3 algorithm' )

    def __call__(self, stateN, stateNP1):
        p1 = self.prox1( stateN.u1 , self.gamma )
        p2 = self.prox2( stateN.u2 )
        p3 = self.prox3( stateN.u3 )

        p  = ( self.omega1 * p1 + 
               self.omega2 * p2 + 
               self.omega3 * p3 )

        stateNP1.u1 = stateN.u1 + self.alpha * ( 2. * p - stateN.x - p1 )
        stateNP1.u2 = stateN.u2 + self.alpha * ( 2. * p - stateN.x - p2 )
        stateNP1.u3 = stateN.u3 + self.alpha * ( 2. * p - stateN.x - p3 )

        stateNP1.x  = ( 1. - self.alpha ) * stateN.x + self.alpha * p
