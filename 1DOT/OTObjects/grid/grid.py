#########
# grid.py
#########
#
# Contains all the classes related to the grid
#

import numpy as np
from .. import OTObject as oto

class Field( oto.OTObject ):
    '''
    Default class to handle a field (m,f)
    '''

    def __init__( self ,
                  N , P ,
                  m , f ):
        oto.OTObject.__init__( self ,
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

    def LInftyNorm(self):
        return np.max( [ np.abs(self.m).max() ,
                         np.abs(self.f).max() ] )

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

    def random(N, P):
        return StaggeredField( N , P ,
                               np.random.rand(N+2,P+1) , np.random.rand(N+1,P+2) )

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
        return Divergence( N , P , div )

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

    def random(N, P):
        return CenteredField( N , P ,
                              np.random.rand(N+1,P+1) , np.random.rand(N+1,P+1) )

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

class Divergence( oto.OTObject ):
    '''
    class to handle the divergence of a field
    '''
    def __init__( self ,
                  N , P ,
                  div=None ):

        oto.OTObject.__init__( self ,
                               N , P )

        if div is None:
            self.div = np.zeros(shape=(N+1,P+1))
        else:
            self.div = div

    def __repr__(self):
        return 'Object representing the divergence of a field'

    def random(N, P):
        return Divergence( N , P ,
                           np.random.rand(N+1,P+1) )

    def Tdivergence(self):
        m = np.zeros(shape=(N+2,P+1))
        m[0:self.N+1,:] = -self.N*self.div[0:self.N+1,:]
        m[1:self.N+2,:] += self.N*self.div[0:self.N+1,:]

        f = np.zeros(shape=(N+1,P+2))
        f[:,0:self.P+1] = -self.P*self.div[:,0:self.P+1]
        f[:,1:self.P+2] += self.P*self.div[:,0:self.P+1]

        return StaggeredField( N, P,
                               m, f )

    def __add__(self, other):
        if isinstance(other,Divergence):
            return Divergence( self.N , self.P ,
                               self.div + other.div )
        else:
            return Divergence( self.N , self.P ,
                               self.div + other )

    def __sub__(self, other):
        if isinstance(other,Divergence):
            return Divergence( self.N , self.P ,
                               self.div - other.div )
        else:
            return Divergence( self.N , self.P ,
                               self.div - other )

    def __mul__(self, other):
        if isinstance(other,Divergence):
            return Divergence( self.N , self.P ,
                               self.div * other.div )
        else:
            return Divergence( self.N , self.P ,
                               self.div * other )

    def __div__(self, other):
        if isinstance(other,Divergence):
            return Divergence( self.N , self.P ,
                               self.div / other.div )
        else:
            return Divergence( self.N , self.P ,
                               self.div / other )

    def __radd__(self, other):
        return Divergence( self.N , self.P ,
                           other + self.div )

    def __rsub__(self, other):
        return Divergence( self.N , self.P ,
                           other - self.div )

    def __rmul__(self, other):
        return Divergence( self.N , self.P ,
                           other * self.div )

    def __rdiv__(self, other):
        return Divergence( self.N , self.P ,
                           other / self.div )

    def __iadd__(self, other):
        if isinstance(other,Divergence):
            self.div += other.div
            return self
        else:
            self.div += other
            return self

    def __isub__(self, other):
        if isinstance(other,Divergence):
            self.div -= other.div
            return self
        else:
            self.div -= other
            return self

    def __imul__(self, other):
        if isinstance(other,Divergence):
            self.div *= other.div
            return self
        else:
            self.div *= other
            return self

    def __idiv__(self, other):
        if isinstance(other,Divergence):
            self.div /= other.div
            return self
        else:
            self.div /= other
            return self

    def __neg__(self):
        return Divergence( self.N , self.P ,
                           - self.div )

    def __pos__(self):
        return Divergence( self.N , self.P ,
                           + self.div )

    def __abs__(self):
        return Divergence( self.N , self.P ,
                           abs ( self.div ) )
    def copy(self):
        return Divergence( self.N , self.P ,
                           self.div.copy() )

    def LInftyNorm(self):
        return np.abs(self.div).max()
