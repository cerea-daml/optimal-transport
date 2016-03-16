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
# Class Prox1Adr
################
#
# First proximal operator for an ADR Algorithm
#

from ...OTObject import OTObject
from ...grid import grid

class Prox1Adr( OTObject ):
    '''
    First proximal operator for an ADR algorithm
    '''

    def __init__(self,
                 config , 
                 proxCdiv, proxJ):
        OTObject.__init__( self ,
                           config.N , config.P )
        self.proxCdiv = proxCdiv
        self.proxJ    = proxJ

    def __repr__(self):
        return ( 'First proximal operator for an ADR algorithm' ) 

    def __call__(self, stagCentField, gamma):
        stagField = self.proxCdiv(stagCentField.staggeredField)
        centField = self.proxJ(stagCentField.centeredField, gamma)
        return grid.StaggeredCenteredField( self.N, self.P, 
                                            stagField, centField)
