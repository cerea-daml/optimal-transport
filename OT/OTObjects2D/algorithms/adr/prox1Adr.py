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
                           config.M , config.N , config.P )
        self.proxCdiv = proxCdiv
        self.proxJ    = proxJ

    def __repr__(self):
        return ( 'First proximal operator for an ADR algorithm' ) 

    def __call__(self, stagCentField, gamma):
        stagField = self.proxCdiv(stagCentField.staggeredField)
        centField = self.proxJ(stagCentField.centeredField, gamma)
        return grid.StaggeredCenteredField( self.M, self.N, self.P, 
                                            stagField, centField)
