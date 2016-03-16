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
# Class PdState
###############
#
# defines the state for a PD algorithm
#

from ...OTObject import OTObject
from ...grid import grid

class PdState( OTObject ):
    '''
    class to handle the state for a PD algorithm
    '''

    def __init__( self ,
                  M , N , P ,
                  u=None , y=None , v=None ):
        OTObject.__init__( self ,
                           M , N , P )
        if u is None:
            self.u = grid.StaggeredField(M,N,P)
        else:
            self.u = u
        if y is None:
            self.y = grid.StaggeredField(M,N,P)
        else:
            self.y = y
        if v is None:
            self.v = grid.CenteredField(M,N,P)
        else:
            self.v = v

    def LInftyNorm(self):
        return np.max( [ self.u.LInftyNorm() ,
                         self.y.LInftyNorm() ,
                         self.v.LinftyNorm() ] )

    def convergingStaggeredField(self):
        return self.u

    def functionalJ(self):
        return self.u.interpolation().functionalJ()

    def __repr__(self):
        return 'Object representing the state of a PD algorithm'

    def __add__(self, other):
        if isinstance(other,PdState):
            return PdState( self.M , self.N , self.P ,
                            self.u + other.u , self.y + other.y , self.v + other.v )
        else:
            return PdState( self.M , self.N , self.P ,
                            self.u + other , self.y + other , self.v + other )

    def __sub__(self, other):
        if isinstance(other,PdState):
            return PdState( self.M , self.N , self.P ,
                            self.u - other.u , self.y - other.y , self.v - other.v )
        else:
            return PdState( self.M , self.N , self.P ,
                            self.u - other , self.y - other , self.v - other )

    def __mul__(self, other):
        if isinstance(other,PdState):
            return PdState( self.M , self.N , self.P ,
                            self.u * other.u , self.y * other.y , self.v * other.v )
        else:
            return PdState( self.M , self.N , self.P ,
                            self.u * other , self.y * other , self.v * other )

    def __div__(self, other):
        if isinstance(other,PdState):
            return PdState( self.M , self.N , self.P ,
                            self.u / other.u , self.y / other.y , self.v / other.v )
        else:
            return PdState( self.M , self.N , self.P ,
                            self.u / other , self.y / other , self.v / other )

    def __radd__(self, other):
        return PdState( self.M , self.N , self.P ,
                        other + self.u , other + self.y , other + self.v )

    def __rsub__(self, other):
        return PdState( self.M , self.N , self.P ,
                        other - self.u , other - self.y , other - self.v )

    def __rmul__(self, other):
        return PdState( self.M , self.N , self.P ,
                        other * self.u , other * self.y , other * self.v )

    def __rdiv__(self, other):
        return PdState( self.N , self.P ,
                        other / self.u , other / self.y , other / self.v )

    def __iadd__(self, other):
        if isinstance(other,PdState):
            self.u += other.u
            self.y += other.y
            self.v += other.v
            return self
        else:
            self.u += other
            self.y += other
            self.v += other
            return self

    def __isub__(self, other):
        if isinstance(other,PdState):
            self.u -= other.u
            self.y -= other.y
            self.v -= other.v
            return self
        else:
            self.u -= other
            self.y -= other
            self.v -= other
            return self

    def __imul__(self, other):
        if isinstance(other,PdState):
            self.u *= other.u
            self.y *= other.y
            self.v *= other.v
            return self
        else:
            self.u *= other
            self.y *= other
            self.v *= other
            return self

    def __idiv__(self, other):
        if isinstance(other,PdState):
            self.u /= other.u
            self.y /= other.y
            self.v /= other.v
            return self
        else:
            self.u /= other
            self.y /= other
            self.v /= other
            return self

    def __neg__(self):
        return PdState( self.M , self.N , self.P ,
                        - self.u , - self.y , - self.v )

    def __pos__(self):
        return PdState( self.M , self.N , self.P ,
                        + self.u , + self.y , + self.v )

    def __abs__(self):
        return PdState( self.M , self.N , self.P ,
                        abs ( self.u ) , abs ( self.y ) , abs ( self.v ) )
    def copy(self):
        return PdState( self.M , self.N , self.P ,
                        self.u.copy() , self.y.copy() , self.v.copy() )

