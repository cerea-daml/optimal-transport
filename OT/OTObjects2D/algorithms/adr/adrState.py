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
# Class AdrState
################
#
# defines the state for ADR algorithm
#

from ...OTObject import OTObject
from ...grid import grid

class AdrState( OTObject ):
    '''
    class to handle the state for an ADR algorithm
    '''

    def __init__( self ,
                  M , N , P ,
                  z=None , w=None ):
        OTObject.__init__( self ,
                           M , N , P )
        if z is None:
            self.z = grid.StaggeredCenteredField(M,N,P)
        else:
            self.z = z
        if w is None:
            self.w = grid.StaggeredCenteredField(M,N,P)
        else:
            self.w = w

    def LInftyNorm(self):
        return max( self.z.LInftyNorm() ,
                    self.w.LInftyNorm() )

    def convergingStaggeredField(self):
        return self.z.staggeredField

    def functionalJ(self):
        return self.z.centeredField.functionalJ()

    def __repr__(self):
        return 'Object representing the state of an ADR algorithm'

    def __add__(self, other):
        if isinstance(other,AdrState):
            return AdrState( self.M , self.N , self.P ,
                             self.z + other.z , self.w + other.w )
        else:
            return AdrState( self.M , self.N , self.P ,
                             self.z + other , self.w + other )

    def __sub__(self, other):
        if isinstance(other,AdrState):
            return AdrState( self.M , self.N , self.P ,
                             self.z - other.z , self.w - other.w )
        else:
            return AdrState( self.M , self.N , self.P ,
                             self.z - other , self.w - other )

    def __mul__(self, other):
        if isinstance(other,AdrState):
            return AdrState( self.M , self.N , self.P ,
                             self.z * other.z , self.w * other.w )
        else:
            return AdrState( self.M , self.N , self.P ,
                             self.z * other , self.w * other )

    def __div__(self, other):
        if isinstance(other,AdrState):
            return AdrState( self.M , self.N , self.P ,
                             self.z / other.z , self.w / other.w )
        else:
            return AdrState( self.M , self.N , self.P ,
                             self.z / other , self.w / other )

    def __radd__(self, other):
        return AdrState( self.M , self.N , self.P ,
                         other + self.z , other + self.w )

    def __rsub__(self, other):
        return AdrState( self.M , self.N , self.P ,
                         other - self.z , other - self.w )

    def __rmul__(self, other):
        return AdrState( self.M , self.N , self.P ,
                         other * self.z , other * self.w )

    def __rdiv__(self, other):
        return AdrState( self.M , self.N , self.P ,
                         other / self.z , other / self.w )

    def __iadd__(self, other):
        if isinstance(other,AdrState):
            self.z += other.z
            self.w += other.w
            return self
        else:
            self.z += other
            self.w += other
            return self

    def __isub__(self, other):
        if isinstance(other,AdrState):
            self.z -= other.z
            self.w -= other.w
            return self
        else:
            self.z -= other
            self.w -= other
            return self

    def __imul__(self, other):
        if isinstance(other,AdrState):
            self.z *= other.z
            self.w *= other.w
            return self
        else:
            self.z *= other
            self.w *= other
            return self

    def __idiv__(self, other):
        if isinstance(other,AdrState):
            self.z /= other.z
            self.w /= other.w
            return self
        else:
            self.z /= other
            self.w /= other
            return self

    def __neg__(self):
        return AdrState( self.M , self.N , self.P ,
                         - self.z , - self.w )

    def __pos__(self):
        return AdrState( self.M , self.N , self.P ,
                         + self.z , + self.w )

    def __abs__(self):
        return AdrState( self.M , self.N , self.P ,
                         abs ( self.z ) , abs ( self.w ) )
    def copy(self):
        return AdrState( self.M , self.N , self.P ,
                         self.z.copy() , self.w.copy() )

