################
# Class Prox1Adr
################
#
# First proximal operator for an ADR Algorithm
#

from .. import OTObject as oto
from ..grid import grid

class Prox1Adr( oto.OTObject ):
    '''
    First proximal operator for an ADR algorithm
    '''

    def __init__(self,
                 config , 
                 proxCdiv, proxJ):
        oto.OTObject.__init__( self ,
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
