#########
# grid.py
#########
#
# Contains all the classes related to the grid
#

import numpy as np
from ../OTObject import OTObject

class Field( OTObject ):
    '''
    Default class to handle a field (m,f)
    '''

    def __init__( self ,
                  N , P ,
                  m , f ):
        OTObject.__init__( self ,
                           N , P )
        self.m = m
        self.f = f

    def __repr__(self):
        return 'Object representing a field (m,f)'

    def __add__(self, other):
        if isinstance(other,Field):
            return Field( self.N , self.P ,
                          self.m + other.m , self.f + other.f )
        else:
            return Field( self.N , self.P ,
                          self.m + other , self.f + other )

    def __sub__(self, other):
        if isinstance(other,Field):
            return Field( self.N , self.P ,
                          self.m - other.m , self.f - other.f )
        else:
            return Field( self.N , self.P ,
                          self.m - other , self.f - other )

    def __mul__(self, other):
        if isinstance(other,Field):
            return Field( self.N , self.P ,
                          self.m * other.m , self.f * other.f )
        else:
            return Field( self.N , self.P ,
                          self.m * other , self.f * other )

    def __div__(self, other):
        if isinstance(other,Field):
            return Field( self.N , self.P ,
                          self.m / other.m , self.f / other.f )
        else:
            return Field( self.N , self.P ,
                          self.m / other , self.f / other )

    def __radd__(self, other):
        return Field( self.N , self.P ,
                      other + self.m , other + self.f )

    def __rsub__(self, other):
        return Field( self.N , self.P ,
                      other - self.m , other - self.f )

    def __rmul__(self, other):
        return Field( self.N , self.P ,
                      other * self.m , other * self.f )

    def __rdiv__(self, other):
        return Field( self.N , self.P ,
                      other / self.m , other / self.f )

    def __iadd__(self, other):
        if isinstance(other,Field):
            self.m += other.m
            self.f += other.f
            return self
        else:
            self.m += other
            self.f += other
            return self

    def __isub__(self, other):
        if isinstance(other,Field):
            self.m -= other.m
            self.f -= other.f
            return self
        else:
            self.m -= other
            self.f -= other
            return self

    def __imul__(self, other):
        if isinstance(other,Field):
            self.m *= other.m
            self.f *= other.f
            return self
        else:
            self.m *= other
            self.f *= other
            return self

    def __idiv__(self, other):
        if isinstance(other,Field):
            self.m /= other.m
            self.f /= other.f
            return self
        else:
            self.m /= other
            self.f /= other
            return self

    def __neg__(self):
        return Field( self.N , self.P ,
                      - self.m , - self.f )

    def __pos__(self):
        return Field( self.N , self.P ,
                      + self.m , + self.f )

    def __abs__(self):
        return Field( self.N , self.P ,
                      abs ( self.m ) , abs ( self.f ) )
    def copy(self):
        return Field( self.N , self.P ,
                      self.m.copy() , self.f.copy() )

class StaggeredField( Field ):
    '''
    Class to handle a field defined on a staggered grid
    '''
    
    def __init__( self ,
                  N , P ,
                  m=None , f=None ):
        if m is None:
            m = np.zeros(shape=(N+2,P+1))
        if f is None:
            f = np.zeros(shape=(N+1,P+2))

        Field.__init__( self ,
                        N , P ,
                        m , f )

    def __repr__(self):
        return 'Object representing a field (m,f) on a staggered grid'

    def interpolation(self):
        m = np.zeros(shape=(N+1,P+1))
        m[:,:]           = 0.5*self.m[0:self.N+1,:]
        m[0:self.N+1,:] += 0.5*self.m[1:self.N+2,:]

        f = np.zeros(shape=(N+1,P+1))
        f[:,:]           = 0.5*self.f[:,0:self.P+1]
        f[:,0:self.P+1] += 0.5*self.f[:,1:self.P+2]

        return CenteredField( self.N, self.P,
                              m, f )

    def divergence(self):
        div = ( self.N*( self.m[1:self.N+2,:] - self.m[0:self.N+1,:] ) +
                self.P*( self.f[:,1:self.P+2] - self.f[:,0:self.P+1]  ) )
#        return Divergence(N,P,div)

    # Boundary function
    # DivBound function
    # DivTempBound function

class CenteredField( Field ):
    '''
    Class to handle a field defined on a centered grid
    '''

    def __init__( self ,
                  N , P ,
                  m=None , f=None ):
        if m is None:
            m = np.zeros(shape=(N+1,P+1))
        if f is None:
            f = np.zeros(shape=(N+1,P+1))

        Field.__init__( self ,
                        N , P ,
                        m , f )

    def __repr__(self):
        return 'Object representing a field (m,f) on a centered grid'

    def functionalJ(self):
        return ( ( self.m * self.m ) *
                 ( self.f > 0 ) / self.f ).sum()

    def Tinterpolation(self):
        m = np.zeros(shape=(N+2,P+1))
        m[0:self.N+1,:]  = 0.5*self.m[:,:]
        m[1:self.N+2,:] += 0.5*self.m[:,:]

        f = np.zeros(shape=(N+1,P+2))
        f[:,0:self.P+1]  = 0.5*self.f[:,:]
        f[:,1:self.P+2] += 0.5*self.f[:,:]

        return StaggeredField( N, P,
                               m, f )
