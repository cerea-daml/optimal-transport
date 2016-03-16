#__________________________________________________
#__________________________________________________

# Copyrigth 2016 A. Farchi and M. Bocquet
# CEREA, joint laboratory Ecole des Ponts ParisTech and EDF R&D

# Code for the paper: Using the Wasserstein distance to compare fields of pollutants:
# Application to the radionuclide atmospheric dispersion of the Fukushima-Daiichi accident
# by A. Farchi, M. Bocquet, Y. Roustan, A. Mathieu and A. Querel

#__________________________________________________

#__________________________________________________
#################
# Class Adr3State
#################
#
# defines the state for ADR3 algorithm
#

from ...OTObject import OTObject
from ...grid import grid

class Adr3State( OTObject ):
    '''
    class to handle the state for an ADR3 algorithm
    '''

    def __init__( self ,
                  M , N , P ,
                  u1=None , u2=None , u3=None , x=None ):
        OTObject.__init__( self ,
                           M , N , P )
        if u1 is None:
            self.u1 = grid.StaggeredCenteredField(M,N,P)
        else:
            self.u1 = u1

        if u2 is None:
            self.u2 = grid.StaggeredCenteredField(M,N,P)
        else:
            self.u2 = u2

        if u3 is None:
            self.u3 = grid.StaggeredCenteredField(M,N,P)
        else:
            self.u3 = u3

        if x is None:
            self.x = grid.StaggeredCenteredField(M,N,P)
        else:
            self.x = x

    def LInftyNorm(self):
        return np.max( [ self.u1.LInftyNorm() ,
                         self.u2.LInftyNorm() ,
                         self.u3.LInftyNorm() ,
                         self.x.LInftyNorm()  ] )

    def convergingStaggeredField(self):
        return self.x.staggeredField

    def functionalJ(self):
        return self.x.centeredField.functionalJ()

    def __repr__(self):
        return 'Object representing the state of an ADR3 algorithm'

    def __add__(self, other):
        if isinstance(other,Adr3State):
            return Adr3State( self.M , self.N , self.P ,
                              self.u1 + other.u1 , self.u2 + other.u2 , self.u3 + other.u3 , self.x + other.x )
        else:
            return Adr3State( self.M , self.N , self.P ,
                              self.u1 + other , self.u2 + other , self.u3 + other , self.x + other )

    def __sub__(self, other):
        if isinstance(other,Adr3State):
            return Adr3State( self.M , self.N , self.P ,
                              self.u1 - other.u1 , self.u2 - other.u2 , self.u3 - other.u3 , self.x - other.x )
        else:
            return Adr3State( self.M , self.N , self.P ,
                              self.u1 - other , self.u2 - other , self.u3 - other , self.x - other )

    def __mul__(self, other):
        if isinstance(other,Adr3State):
            return Adr3State( self.M , self.N , self.P ,
                              self.u1 * other.u1 , self.u2 * other.u2 , self.u3 * other.u3 , self.x * other.x )
        else:
            return Adr3State( self.M , self.N , self.P ,
                              self.u1 * other , self.u2 * other , self.u3 * other , self.x * other )

    def __div__(self, other):
        if isinstance(other,Adr3State):
            return Adr3State( self.M , self.N , self.P ,
                              self.u1 / other.u1 , self.u2 / other.u2 , self.u3 / other.u3 , self.x / other.x )
        else:
            return Adr3State( self.M , self.N , self.P ,
                              self.u1 / other , self.u2 / other , self.u3 / other , self.x / other )

    def __radd__(self, other):
        return Adr3State( self.M , self.N , self.P ,
                          other + self.u1 , other + self.u2 , other + self.u3 , other + self.x )

    def __rsub__(self, other):
        return Adr3State( self.M , self.N , self.P ,
                          other - self.u1 , other - self.u2 , other - self.u3 , other - self.x )

    def __rmul__(self, other):
        return Adr3State( self.M , self.N , self.P ,
                          other * self.u1 , other * self.u2 , other * self.u3 , other * self.x )

    def __rdiv__(self, other):
        return Adr3State( self.M , self.N , self.P ,
                          other / self.u1 , other / self.u2 , other / self.u3 , other / self.x )

    def __iadd__(self, other):
        if isinstance(other,Adr3State):
            self.u1 += other.u1
            self.u2 += other.u2
            self.u3 += other.u3
            self.x += other.x
            return self
        else:
            self.u1 += other
            self.u2 += other
            self.u3 += other
            self.x += other
            return self

    def __isub__(self, other):
        if isinstance(other,Adr3State):
            self.u1 -= other.u1
            self.u2 -= other.u2
            self.u3 -= other.u3
            self.x -= other.x
            return self
        else:
            self.u1 -= other
            self.u2 -= other
            self.u3 -= other
            self.x -= other
            return self

    def __imul__(self, other):
        if isinstance(other,Adr3State):
            self.u1 *= other.u1
            self.u2 *= other.u2
            self.u3 *= other.u3
            self.x *= other.x
            return self
        else:
            self.u1 *= other
            self.u2 *= other
            self.u3 *= other
            self.x *= other
            return self

    def __idiv__(self, other):
        if isinstance(other,Adr3State):
            self.u1 /= other.u1
            self.u2 /= other.u2
            self.u3 /= other.u3
            self.x /= other.x
            return self
        else:
            self.u1 /= other
            self.u2 /= other
            self.u3 /= other
            self.x /= other
            return self

    def __neg__(self):
        return Adr3State( self.M , self.N , self.P ,
                          - self.u1 , - self.u2 , - self.u3 , - self.x )

    def __pos__(self):
        return Adr3State( self.M , self.N , self.P ,
                          + self.u1 , + self.u2 , + self.u3 , + self.x )

    def __abs__(self):
        return Adr3State( self.M , self.N , self.P ,
                          abs ( self.u1 ) , abs ( self.u2 ) , abs ( self.u3 ) , abs ( self.x ) )
    def copy(self):
        return Adr3State( self.M , self.N , self.P ,
                          self.u1.copy() , self.u2.copy() , self.u3.copy() , self.x.copy() )

