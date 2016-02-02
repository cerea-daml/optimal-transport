###########
# proxPd.py
###########
#
# Defines the correct proximal operators for a PD algorithm
#

from ...OTObject import OTObject

class Prox1Pd:
    '''
    First proximal operator for a PD algorithm
    '''

    def __init__(self,
                 config, 
                 proxJ):
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
