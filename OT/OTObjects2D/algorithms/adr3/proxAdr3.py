#############
# proxAdr3.py
#############
#
# Define proximal operators for an ADR3 Algorithm
#

from ...OTObject import OTObject
from ...grid import grid

class Prox1Adr3( OTObject ):
    '''
    First proximal operator for an ADR3 algorithm
    '''

    def __init__(self,
                 config , 
                 proxCdiv, proxJ):
        OTObject.__init__( self ,
                           config.M , config.N , config.P )
        self.proxCdiv = proxCdiv
        self.proxJ    = proxJ

    def __repr__(self):
        return ( 'First proximal operator for an ADR3 algorithm' ) 

    def __call__(self, stagCentField, gamma):
        stagField = self.proxCdiv(stagCentField.staggeredField)
        centField = self.proxJ(stagCentField.centeredField, gamma)
        return grid.StaggeredCenteredField( self.M, self.N, self.P, 
                                            stagField, centField)

class Prox2Adr3:
    '''
    Second proximal operator for an ADR3 algorithm
    '''

    def __init__(self,
                 proxCsc):
        self.proxCsc = proxCsc

    def __repr__(self):
        return ( 'Second proximal operator for an ADR3 algorithm' )

    def __call__(self, stagCentField):
        return self.proxCsc(stagCentField)

class Prox3Adr3( OTObject ):
    '''
    Third proximal operator for an ADR3 algorithm
    '''

    def __init__(self,
                 config,
                 proxCb):
        OTObject.__init__( self ,
                           config.M , config.N , config.P )
        self.proxCb = proxCb

    def __repr__(self):
        return ( 'Third proximal operator for an ADR3 algorithm' )

    def __call__(self, stagCentField):
        stagField = self.proxCb(stagCentField.staggeredField)
        centField = stagCentField.centeredField.copy()
        return grid.StaggeredCenteredField( self.M , self.N, self.P,
                                            stagField, centField)

