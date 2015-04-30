###########
# proxPd.py
###########
#
# Defines the correct proximal operators for a PD algorithm
#

from .. import OTObject as oto
from ..grid import grid

class Prox1Pd( oto.OTObject ):
    '''
    First proximal operator for an ADR algorithm
    '''

    def __init__(self,
                 config, 
                 proxJ):
        oto.OTObject.__init__( self ,
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
