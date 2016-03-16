#==================================================
#__________________________________________________

# Copyrigth 2016 A. Farchi and M. Bocquet
# CEREA, joint laboratory Ecole des Ponts ParisTech and EDF R&D

# Code for the paper: Using the Wasserstein distance to compare fields of pollutants:
# Application to the radionuclide atmospheric dispersion of the Fukushima-Daiichi accident
# by A. Farchi, M. Bocquet, Y. Roustan, A. Mathieu and A. Querel

#__________________________________________________
#==================================================

###########
# proxPd.py
###########
#
# Defines the correct proximal operators for a PD algorithm
#

from ...OTObject import OTObject

class Prox1Pd( OTObject ):
    '''
    First proximal operator for an ADR algorithm
    '''

    def __init__(self,
                 config, 
                 proxJ):
        OTObject.__init__( self ,
                           config.N , config.P )
        self.proxJ = proxJ
        self.gamma = 1. / config.sigma
        self.sigma = config.sigma

    def __repr__(self):
        return ( 'First proximal operator for a PD algorithm' ) 

    def __call__(self, centField):
        return ( centField - self.sigma * self.proxJ( self.gamma * centField , self.gamma ) )

class Prox2Pd:
    '''
    Second proximal operator for a PD algorithm
    '''

    def __init__(self, proxCdiv):
        self.prox = proxCdiv

    def __repr__(self):
        return ( 'Second proximal operator for a PD algorithm' )

    def __call__(self, stagField):
        return self.prox(stagField)
