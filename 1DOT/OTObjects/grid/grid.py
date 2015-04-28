#########
# grid.py
#########
#
# Contains all the classes related to the grid
#

import numpy as np
from .. import OTObject as oto

#__________________________________________________

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

#__________________________________________________

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
    random = staticmethod(random)

    def interpolation(self):
        m = np.zeros(shape=(self.N+1,self.P+1))
        m[:,:]           = 0.5*self.m[0:self.N+1,:]
        m[0:self.N+1,:] += 0.5*self.m[1:self.N+2,:]

        f = np.zeros(shape=(self.N+1,self.P+1))
        f[:,:]           = 0.5*self.f[:,0:self.P+1]
        f[:,0:self.P+1] += 0.5*self.f[:,1:self.P+2]

        return CenteredField( self.N, self.P,
                              m, f )

    def divergence(self):
        div = ( self.N*( self.m[1:self.N+2,:] - self.m[0:self.N+1,:] ) +
                self.P*( self.f[:,1:self.P+2] - self.f[:,0:self.P+1]  ) )
        return Divergence( self.N , self.P , div )

    def temporalBoundaries(self):
        return TemporalBoundaries( self.N, self.P,
                                   self.f[:,0], self.f[:,self.P+1] )

    def temporalReservoirBoundaries(self):
        trb = self.temporalBoundaries()
        trb.bt1[0] = 0.
        trb.bt1[self.N] = 0.
        return trb

    def spatialBoundaries(self):
        return SpatialBoundaries( self.N, self.P,
                                  self.m[0,:], self.m[self.N+1,:] )

    def boundaries(self):
        return Boundaries( self.N, self.P,
                           self.temporalBoundaries(), self.spatialBoundaries() )

    def reservoirBoundaries(self):
        return Boundaries( self.N, self.P,
                           self.temporalReservoirBoundaries(), self.spatialBoundaries() )
    
    def divergenceBoundaries(self):
        return DivergenceBoundaries( self.N, self.P,
                                     self.divergence(), self.boundaries() )

    def divergenceTemporalBoundaries(self):
        return DivergenceTemporalBoundaries( self.N, self.P,
                                             self.divergence(), self.temporalBoundaries() )

    def __add__(self, other):
        if isinstance(other,StaggeredField):
            return StaggeredField( self.N , self.P ,
                                   self.m + other.m , self.f + other.f )
        else:
            return StaggeredField( self.N , self.P ,
                                   self.m + other , self.f + other )

    def __sub__(self, other):
        if isinstance(other,StaggeredField):
            return StaggeredField( self.N , self.P ,
                                   self.m - other.m , self.f - other.f )
        else:
            return StaggeredField( self.N , self.P ,
                                   self.m - other , self.f - other )

    def __mul__(self, other):
        if isinstance(other,StaggeredField):
            return StaggeredField( self.N , self.P ,
                                   self.m * other.m , self.f * other.f )
        else:
            return StaggeredField( self.N , self.P ,
                                   self.m * other , self.f * other )

    def __div__(self, other):
        if isinstance(other,StaggeredField):
            return StaggeredField( self.N , self.P ,
                                   self.m / other.m , self.f / other.f )
        else:
            return StaggeredField( self.N , self.P ,
                                   self.m / other , self.f / other )

    def __radd__(self, other):
        return StaggeredField( self.N , self.P ,
                               other + self.m , other + self.f )

    def __rsub__(self, other):
        return StaggeredField( self.N , self.P ,
                               other - self.m , other - self.f )

    def __rmul__(self, other):
        return StaggeredField( self.N , self.P ,
                               other * self.m , other * self.f )

    def __rdiv__(self, other):
        return StaggeredField( self.N , self.P ,
                               other / self.m , other / self.f )

    def __neg__(self):
        return StaggeredField( self.N , self.P ,
                               - self.m , - self.f )

    def __pos__(self):
        return StaggeredField( self.N , self.P ,
                               + self.m , + self.f )

    def __abs__(self):
        return StaggeredField( self.N , self.P ,
                               abs ( self.m ) , abs ( self.f ) )
    def copy(self):
        return StaggeredField( self.N , self.P ,
                               self.m.copy() , self.f.copy() )

#__________________________________________________

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
    random = staticmethod(random)

    def functionalJ(self):
        return ( ( self.m * self.m ) *
                 ( self.f > 0 ) / self.f ).sum()

    def Tinterpolation(self):
        m = np.zeros(shape=(self.N+2,self.P+1))
        m[0:self.N+1,:]  = 0.5*self.m[:,:]
        m[1:self.N+2,:] += 0.5*self.m[:,:]

        f = np.zeros(shape=(self.N+1,self.P+2))
        f[:,0:self.P+1]  = 0.5*self.f[:,:]
        f[:,1:self.P+2] += 0.5*self.f[:,:]

        return StaggeredField( self.N, self.P,
                               m, f )

    def TinterpolationError(self):
        mu = np.zeros(shape=(self.N+2,self.P+1))
        fu = np.zeros(shape=(self.N+1,self.P+2))

        mu[0:self.N+1,:] = -0.5*self.m[:,:]
        mu[1:self.N+2,:] -= 0.5*self.m[:,:]

        fu[:,0:self.P+1] = -0.5*self.f[:,:]
        fu[:,1:self.P+2] -= 0.5*self.f[:,:]

        staggeredField = StaggeredField( self.N , self.P , mu , fu )

        return StaggeredCenteredField( self.N , self.P , staggeredField , self )

    def __add__(self, other):
        if isinstance(other,CenteredField):
            return CenteredField( self.N , self.P ,
                                  self.m + other.m , self.f + other.f )
        else:
            return CenteredField( self.N , self.P ,
                                  self.m + other , self.f + other )

    def __sub__(self, other):
        if isinstance(other,CenteredField):
            return CenteredField( self.N , self.P ,
                                  self.m - other.m , self.f - other.f )
        else:
            return CenteredField( self.N , self.P ,
                                  self.m - other , self.f - other )

    def __mul__(self, other):
        if isinstance(other,CenteredField):
            return CenteredField( self.N , self.P ,
                                  self.m * other.m , self.f * other.f )
        else:
            return CenteredField( self.N , self.P ,
                                  self.m * other , self.f * other )

    def __div__(self, other):
        if isinstance(other,CenteredField):
            return CenteredField( self.N , self.P ,
                                  self.m / other.m , self.f / other.f )
        else:
            return CenteredField( self.N , self.P ,
                                  self.m / other , self.f / other )

    def __radd__(self, other):
        return CenteredField( self.N , self.P ,
                              other + self.m , other + self.f )

    def __rsub__(self, other):
        return CenteredField( self.N , self.P ,
                              other - self.m , other - self.f )

    def __rmul__(self, other):
        return CenteredField( self.N , self.P ,
                              other * self.m , other * self.f )

    def __rdiv__(self, other):
        return CenteredField( self.N , self.P ,
                              other / self.m , other / self.f )

    def __neg__(self):
        return CenteredField( self.N , self.P ,
                              - self.m , - self.f )

    def __pos__(self):
        return CenteredField( self.N , self.P ,
                              + self.m , + self.f )

    def __abs__(self):
        return CenteredField( self.N , self.P ,
                              abs ( self.m ) , abs ( self.f ) )
    def copy(self):
        return CenteredField( self.N , self.P ,
                              self.m.copy() , self.f.copy() )

#__________________________________________________

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
    random = staticmethod(random)

    def Tdivergence(self):
        m = np.zeros(shape=(self.N+2,self.P+1))
        m[0:self.N+1,:] = -self.N*self.div[0:self.N+1,:]
        m[1:self.N+2,:] += self.N*self.div[0:self.N+1,:]

        f = np.zeros(shape=(self.N+1,self.P+2))
        f[:,0:self.P+1] = -self.P*self.div[:,0:self.P+1]
        f[:,1:self.P+2] += self.P*self.div[:,0:self.P+1]

        return StaggeredField( self.N, self.P,
                               m, f )

    def sum(self):
        return self.div.sum()

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

#__________________________________________________

class TemporalBoundaries( oto.OTObject ):
    '''
    class to store the temporal boundaries of a field
    '''

    def __init__( self ,
                  N , P ,
                  bt0=None , bt1=None ):
        oto.OTObject.__init__( self ,
                               N , P )
        if bt0 is None:
            self.bt0 = np.zeros(N+1)
        else:
            self.bt0 = bt0
        if bt1 is None:
            self.bt1 = np.zeros(N+1)
        else:
            self.bt1 = bt1

    def __repr__(self):
        return "Object representing the temporal boundaries of a field"

    def random( N , P ):
        bt0 = np.random.rand(N+1)
        bt1 = np.random.rand(N+1)
        return TemporalBoundaries( N , P ,
                                   bt0 , bt1 )
    random = staticmethod(random)

    def TtemporalBoundaries(self):
        m = np.zeros(shape=(self.N+2,self.P+1))
        f = np.zeros(shape=(self.N+1,self.P+2))

        f[:,0]        = self.bt0[:]
        f[:,self.P+1] = self.bt1[:]

        return StaggeredField( self.N, self.P,
                               m, f )

    def TtemporalReservoirBoundaries(self):
        m = np.zeros(shape=(self.N+2,self.P+1))
        f = np.zeros(shape=(self.N+1,self.P+2))

        f[:,0]               = self.bt0[:]
        f[1:self.N,self.P+1] = self.bt1[1:self.N]

        return StaggeredField( self.N, self.P,
                               m, f )

    def massDefault(self):
        return ( self.P * ( self.bt0.sum() - self.bt1.sum() ) )

    def LInftyNorm(self):
        return np.max( [ abs(self.bt0).max() , abs(self.bt1).max() ] )

    def __add__(self, other):
        if isinstance(other,TemporalBoundaries):
            return TemporalBoundaries( self.N , self.P ,
                                       self.bt0 + other.bt0 , self.bt1 + other.bt1 )
        else:
            return TemporalBoundaries( self.N , self.P ,
                                       self.bt0 + other , self.bt1 + other )

    def __sub__(self, other):
        if isinstance(other,TemporalBoundaries):
            return TemporalBoundaries( self.N , self.P ,
                                       self.bt0 - other.bt0 , self.bt1 - other.bt1 )
        else:
            return TemporalBoundaries( self.N , self.P ,
                                       self.bt0 - other , self.bt1 - other )

    def __mul__(self, other):
        if isinstance(other,TemporalBoundaries):
            return TemporalBoundaries( self.N , self.P ,
                                       self.bt0 * other.bt0 , self.bt1 * other.bt1 )
        else:
            return TemporalBoundaries( self.N , self.P ,
                                       self.bt0 * other , self.bt1 * other )

    def __div__(self, other):
        if isinstance(other,TemporalBoundaries):
            return TemporalBoundaries( self.N , self.P ,
                                       self.bt0 / other.bt0 , self.bt1 / other.bt1 )
        else:
            return TemporalBoundaries( self.N , self.P ,
                                       self.bt0 / other , self.bt1 / other )

    def __radd__(self, other):
        return TemporalBoundaries( self.N , self.P ,
                                   other + self.bt0 , other + self.bt1 )

    def __rsub__(self, other):
        return TemporalBoundaries( self.N , self.P ,
                                   other - self.bt0 , other - self.bt1 )

    def __rmul__(self, other):
        return TemporalBoundaries( self.N , self.P ,
                                   other * self.bt0 , other * self.bt1 )

    def __rdiv__(self, other):
        return TemporalBoundaries( self.N , self.P ,
                                   other / self.bt0 , other / self.bt1 )

    def __iadd__(self, other):
        if isinstance(other,TemporalBoundaries):
            self.bt0 += other.bt0
            self.bt1 += other.bt1
            return self
        else:
            self.bt0 += other
            self.bt1 += other
            return self

    def __isub__(self, other):
        if isinstance(other,TemporalBoundaries):
            self.bt0 -= other.bt0
            self.bt1 -= other.bt1
            return self
        else:
            self.bt0 -= other
            self.bt1 -= other
            return self

    def __imul__(self, other):
        if isinstance(other,TemporalBoundaries):
            self.bt0 *= other.bt0
            self.bt1 *= other.bt1
            return self
        else:
            self.bt0 *= other
            self.bt1 *= other
            return self

    def __idiv__(self, other):
        if isinstance(other,TemporalBoundaries):
            self.bt0 /= other.bt0
            self.bt1 /= other.bt1
            return self
        else:
            self.bt0 /= other
            self.bt1 /= other
            return self

    def __neg__(self):
        return TemporalBoundaries( self.N , self.P ,
                                   - self.bt0 , - self.bt1 )

    def __pos__(self):
        return TemporalBoundaries( self.N , self.P ,
                                   + self.bt0 , + self.bt1 )

    def __abs__(self):
        return TemporalBoundaries( self.N , self.P ,
                                   abs ( self.bt0 ) , abs ( self.bt1 ) )
    def copy(self):
        return TemporalBoundaries( self.N , self.P ,
                                   self.bt0.copy() , self.bt1.copy() )

#__________________________________________________

class SpatialBoundaries( oto.OTObject ):
    '''
    class to store the spatial boundaries of a field
    '''

    def __init__( self ,
                  N , P ,
                  bx0=None , bx1=None ):
        oto.OTObject.__init__( self ,
                               N , P )
        if bx0 is None:
            self.bx0 = np.zeros(P+1)
        else:
            self.bx0 = bx0
        if bx1 is None:
            self.bx1 = np.zeros(P+1)
        else:
            self.bx1 = bx1

    def __repr__(self):
        return "Object representing the spatial boundaries of a field"

    def random( N , P ):
        bx0 = np.random.rand(P+1)
        bx1 = np.random.rand(P+1)
        return SpatialBoundaries( N , P ,
                                  bx0 , bx1 )
    random = staticmethod(random)

    def TspatialBoundaries(self):
        m = np.zeros(shape=(self.N+2,self.P+1))
        f = np.zeros(shape=(self.N+1,self.P+2))

        m[0,:]        = self.bx0[:]
        m[self.N+1,:] = self.bx1[:]

        return StaggeredField( self.N, self.P,
                               m, f )

    def massDefault(self):
        return ( self.N * ( self.bx0.sum() - self.bx1.sum() ) )

    def LInftyNorm(self):
        return np.max( [ abs(self.bx0).max() , abs(self.bx1).max() ] )

    def __add__(self, other):
        if isinstance(other,SpatialBoundaries):
            return SpatialBoundaries( self.N , self.P ,
                                      self.bx0 + other.bx0 , self.bx1 + other.bx1 )
        else:
            return SpatialBoundaries( self.N , self.P ,
                                      self.bx0 + other , self.bx1 + other )

    def __sub__(self, other):
        if isinstance(other,SpatialBoundaries):
            return SpatialBoundaries( self.N , self.P ,
                                      self.bx0 - other.bx0 , self.bx1 - other.bx1 )
        else:
            return SpatialBoundaries( self.N , self.P ,
                                      self.bx0 - other , self.bx1 - other )

    def __mul__(self, other):
        if isinstance(other,SpatialBoundaries):
            return SpatialBoundaries( self.N , self.P ,
                                      self.bx0 * other.bx0 , self.bx1 * other.bx1 )
        else:
            return SpatialBoundaries( self.N , self.P ,
                                      self.bx0 * other , self.bx1 * other )

    def __div__(self, other):
        if isinstance(other,SpatialBoundaries):
            return SpatialBoundaries( self.N , self.P ,
                                      self.bx0 / other.bx0 , self.bx1 / other.bx1 )
        else:
            return SpatialBoundaries( self.N , self.P ,
                                      self.bx0 / other , self.bx1 / other )

    def __radd__(self, other):
        return SpatialBoundaries( self.N , self.P ,
                                  other + self.bx0 , other + self.bx1 )

    def __rsub__(self, other):
        return SpatialBoundaries( self.N , self.P ,
                                  other - self.bx0 , other - self.bx1 )

    def __rmul__(self, other):
        return SpatialBoundaries( self.N , self.P ,
                                  other * self.bx0 , other * self.bx1 )

    def __rdiv__(self, other):
        return SpatialBoundaries( self.N , self.P ,
                                  other / self.bx0 , other / self.bx1 )

    def __iadd__(self, other):
        if isinstance(other,SpatialBoundaries):
            self.bx0 += other.bx0
            self.bx1 += other.bx1
            return self
        else:
            self.bx0 += other
            self.bx1 += other
            return self

    def __isub__(self, other):
        if isinstance(other,SpatialBoundaries):
            self.bx0 -= other.bx0
            self.bx1 -= other.bx1
            return self
        else:
            self.bx0 -= other
            self.bx1 -= other
            return self

    def __imul__(self, other):
        if isinstance(other,SpatialBoundaries):
            self.bx0 *= other.bx0
            self.bx1 *= other.bx1
            return self
        else:
            self.bx0 *= other
            self.bx1 *= other
            return self

    def __idiv__(self, other):
        if isinstance(other,SpatialBoundaries):
            self.bx0 /= other.bx0
            self.bx1 /= other.bx1
            return self
        else:
            self.bx0 /= other
            self.bx1 /= other
            return self

    def __neg__(self):
        return SpatialBoundaries( self.N , self.P ,
                                  - self.bx0 , - self.bx1 )

    def __pos__(self):
        return SpatialBoundaries( self.N , self.P ,
                                  + self.bx0 , + self.bx1 )

    def __abs__(self):
        return SpatialBoundaries( self.N , self.P ,
                                  abs ( self.bx0 ) , abs ( self.bx1 ) )
    def copy(self):
        return SpatialBoundaries( self.N , self.P ,
                                  self.bx0.copy() , self.bx1.copy() )

#__________________________________________________

class Boundaries( oto.OTObject ):
    '''
    class to store the boundaries of a field
    '''

    def __init__( self ,
                  N , P ,
                  temporalBoundaries=None , spatialBoundaries=None ):
        oto.OTObject.__init__( self ,
                           N , P )
        if temporalBoundaries is None:
            self.temporalBoundaries = TemporalBoundaries( N , P )
        else:
            self.temporalBoundaries = temporalBoundaries
        if spatialBoundaries is None:
            self.spatialBoundaries = SpatialBoundaries( N , P )
        else:
            self.spatialBoundaries = spatialBoundaries

    def __repr__(self):
        return "Object representing the boundaries of a field"

    def Tboundaries(self):
        gridT = self.temporalBoundaries.TtemporalBoundaries()
        gridS = self.spatialBoundaries.TspatialBoundaries()
        return ( gridT + gridS )

    def TreservoirBoundaries(self):
        gridT = self.temporalBoundaries.TtemporalReservoirBoundaries()
        gridS = self.spatialBoundaries.TspatialBoundaries()
        return ( gridT + gridS )

    def random( N , P ):
        return Boundaries( N , P ,
                           TemporalBoundaries.random(N,P) , SpatialBoundaries.random(N,P) )
    random = staticmethod(random)

    def massDefault(self):
        return ( self.temporalBoundaries.massDefault() + self.spatialBoundaries.massDefault() )

    def LInftyNorm(self):
        return np.max( [ self.temporalBoundaries.LInftyNorm() , self.spatialBoundaries.LInftyNorm() ] )

    def __add__(self, other):
        if isinstance(other,Boundaries):
            return Boundaries( self.N , self.P ,
                               self.temporalBoundaries + other.temporalBoundaries , self.spatialBoundaries + other.spatialBoundaries )
        else:
            return Boundaries( self.N , self.P ,
                               self.temporalBoundaries + other , self.spatialBoundaries + other )

    def __sub__(self, other):
        if isinstance(other,Boundaries):
            return Boundaries( self.N , self.P ,
                               self.temporalBoundaries - other.temporalBoundaries , self.spatialBoundaries - other.spatialBoundaries )
        else:
            return Boundaries( self.N , self.P ,
                               self.temporalBoundaries - other , self.spatialBoundaries - other )

    def __mul__(self, other):
        if isinstance(other,Boundaries):
            return Boundaries( self.N , self.P ,
                               self.temporalBoundaries * other.temporalBoundaries , self.spatialBoundaries * other.spatialBoundaries )
        else:
            return Boundaries( self.N , self.P ,
                               self.temporalBoundaries * other , self.spatialBoundaries * other )

    def __div__(self, other):
        if isinstance(other,Boundaries):
            return Boundaries( self.N , self.P ,
                               self.temporalBoundaries / other.temporalBoundaries , self.spatialBoundaries / other.spatialBoundaries )
        else:
            return Boundaries( self.N , self.P ,
                               self.temporalBoundaries / other , self.spatialBoundaries / other )

    def __radd__(self, other):
        return Boundaries( self.N , self.P ,
                           other + self.temporalBoundaries , other + self.spatialBoundaries )

    def __rsub__(self, other):
        return Boundaries( self.N , self.P ,
                           other - self.temporalBoundaries , other - self.spatialBoundaries )

    def __rmul__(self, other):
        return Boundaries( self.N , self.P ,
                           other * self.temporalBoundaries , other * self.spatialBoundaries )

    def __rdiv__(self, other):
        return Boundaries( self.N , self.P ,
                           other / self.temporalBoundaries , other / self.spatialBoundaries )

    def __iadd__(self, other):
        if isinstance(other,Boundaries):
            self.temporalBoundaries += other.temporalBoundaries
            self.spatialBoundaries += other.spatialBoundaries
            return self
        else:
            self.temporalBoundaries += other
            self.spatialBoundaries += other
            return self

    def __isub__(self, other):
        if isinstance(other,Boundaries):
            self.temporalBoundaries -= other.temporalBoundaries
            self.spatialBoundaries -= other.spatialBoundaries
            return self
        else:
            self.temporalBoundaries -= other
            self.spatialBoundaries -= other
            return self

    def __imul__(self, other):
        if isinstance(other,Boundaries):
            self.temporalBoundaries *= other.temporalBoundaries
            self.spatialBoundaries *= other.spatialBoundaries
            return self
        else:
            self.temporalBoundaries *= other
            self.spatialBoundaries *= other
            return self

    def __idiv__(self, other):
        if isinstance(other,Boundaries):
            self.temporalBoundaries /= other.temporalBoundaries
            self.spatialBoundaries /= other.spatialBoundaries
            return self
        else:
            self.temporalBoundaries /= other
            self.spatialBoundaries /= other
            return self

    def __neg__(self):
        return Boundaries( self.N , self.P ,
                           - self.temporalBoundaries , - self.spatialBoundaries )

    def __pos__(self):
        return Boundaries( self.N , self.P ,
                           + self.temporalBoundaries , + self.spatialBoundaries )

    def __abs__(self):
        return Boundaries( self.N , self.P ,
                           abs ( self.temporalBoundaries ) , abs ( self.spatialBoundaries ) )
    def copy(self):
        return Boundaries( self.N , self.P ,
                           self.temporalBoundaries.copy() , self.spatialBoundaries.copy() )

#__________________________________________________

class DivergenceBoundaries( oto.OTObject ):
    '''
    class to store the divergence and boundary conditions of a field
    '''

    def __init__( self ,
                  N , P ,
                  divergence=None , boundaries=None ):
        oto.OTObject.__init__( self ,
                               N , P )
        if divergence is None:
            self.divergence = Divergence( N , P )
        else:
            self.divergence = divergence
        if boundaries is None:
            self.boundaries = Boundaries( N , P )
        else:
            self.boundaries = boundaries

    def __repr__(self):
        return "Object representing the divergence and boundary conditions of a field"

    def TdivergenceBoundaries(self):
        gridDiv = self.divergence.Tdivergence()
        gridB   = self.boundaries.Tboundaries()
        return ( gridDiv + gridB )

    def applyGaussForward(self):
        self.divergence.div[0,:]      += self.N*self.boundaries.spatialBoundaries.bx0[:]
        self.divergence.div[self.N,:] -= self.N*self.boundaries.spatialBoundaries.bx1[:]
        self.divergence.div[:,0]      += self.P*self.boundaries.temporalBoundaries.bt0[:]
        self.divergence.div[:,self.P] -= self.P*self.boundaries.temporalBoundaries.bt1[:]

    def applyGaussBackward(self):
        self.boundaries.spatialBoundaries.bx0  += self.N*self.divergence.div[0,:]
        self.boundaries.spatialBoundaries.bx1  -= self.N*self.divergence.div[self.N,:]
        self.boundaries.temporalBoundaries.bt0 += self.P*self.divergence.div[:,0]
        self.boundaries.temporalBoundaries.bt1 -= self.P*self.divergence.div[:,self.P]

    def massDefault(self):
        return ( self.divergence.sum() +
                 self.boundaries.massDefault() )

    def correctMassDefault(self, EPS):
        deltaM = self.massDefault()

        if abs(deltaM) > EPS:
            nbrPts = ( (self.N+1.)*(self.P+1.) +
                       2.*(self.P+1.) +
                       2.*(self.N+1.) )

            self.divergence -= deltaM / nbrPts
            self.boundaries.spatialBoundaries.bx0  -= deltaM / ( self.N * nbrPts )
            self.boundaries.spatialBoundaries.bx1  += deltaM / ( self.N * nbrPts )
            self.boundaries.temporalBoundaries.bt0 -= deltaM / ( self.P * nbrPts )
            self.boundaries.temporalBoundaries.bt1 += deltaM / ( self.P * nbrPts )

            deltaM = self.massDefault()
        return deltaM

    def random( N , P ):
        return DivergenceBoundaries( N , P ,
                                     Divergence.random(N,P) , Boundaries.random(N,P) )
    random = staticmethod(random)

    def ones( N , P ):
        div =  np.ones(shape=(N+1,P+1))
        bx0 =  N*np.ones(P+1)
        bx1 = -N*np.ones(P+1)
        bt0 =  P*np.ones(N+1)
        bt1 = -P*np.ones(N+1)
        return DivergenceBoundaries( N , P , 
                                     Divergence( N , P ,
                                                 div ) ,
                                     Boundaries( N , P ,
                                                 TemporalBoundaries( N , P ,
                                                                     bt0 , bt1 ) ,
                                                 SpatialBoundaries( N , P ,
                                                                    bx0 , bx1 ) ) )
    ones = staticmethod(ones)

    def LInftyNorm(self):
        return np.max( [ self.divergence.LInftyNorm() , self.boundaries.LInftyNorm() ] )

    def __add__(self, other):
        if isinstance(other,DivergenceBoundaries):
            return DivergenceBoundaries( self.N , self.P ,
                                         self.divergence + other.divergence , self.boundaries + other.boundaries )
        else:
            return DivergenceBoundaries( self.N , self.P ,
                                         self.divergence + other , self.boundaries + other )

    def __sub__(self, other):
        if isinstance(other,DivergenceBoundaries):
            return DivergenceBoundaries( self.N , self.P ,
                                         self.divergence - other.divergence , self.boundaries - other.boundaries )
        else:
            return DivergenceBoundaries( self.N , self.P ,
                                         self.divergence - other , self.boundaries - other )

    def __mul__(self, other):
        if isinstance(other,DivergenceBoundaries):
            return DivergenceBoundaries( self.N , self.P ,
                                         self.divergence * other.divergence , self.boundaries * other.boundaries )
        else:
            return DivergenceBoundaries( self.N , self.P ,
                                         self.divergence * other , self.boundaries * other )

    def __div__(self, other):
        if isinstance(other,DivergenceBoundaries):
            return DivergenceBoundaries( self.N , self.P ,
                                         self.divergence / other.divergence , self.boundaries / other.boundaries )
        else:
            return DivergenceBoundaries( self.N , self.P ,
                                         self.divergence / other , self.boundaries / other )

    def __radd__(self, other):
        return DivergenceBoundaries( self.N , self.P ,
                                     other + self.divergence , other + self.boundaries )

    def __rsub__(self, other):
        return DivergenceBoundaries( self.N , self.P ,
                                     other - self.divergence , other - self.boundaries )

    def __rmul__(self, other):
        return DivergenceBoundaries( self.N , self.P ,
                                     other * self.divergence , other * self.boundaries )

    def __rdiv__(self, other):
        return DivergenceBoundaries( self.N , self.P ,
                                     other / self.divergence , other / self.boundaries )

    def __iadd__(self, other):
        if isinstance(other,DivergenceBoundaries):
            self.divergence += other.divergence
            self.boundaries += other.boundaries
            return self
        else:
            self.divergence += other
            self.boundaries += other
            return self

    def __isub__(self, other):
        if isinstance(other,DivergenceBoundaries):
            self.divergence -= other.divergence
            self.boundaries -= other.boundaries
            return self
        else:
            self.divergence -= other
            self.boundaries -= other
            return self

    def __imul__(self, other):
        if isinstance(other,DivergenceBoundaries):
            self.divergence *= other.divergence
            self.boundaries *= other.boundaries
            return self
        else:
            self.divergence *= other
            self.boundaries *= other
            return self

    def __idiv__(self, other):
        if isinstance(other,DivergenceBoundaries):
            self.divergence /= other.divergence
            self.boundaries /= other.boundaries
            return self
        else:
            self.divergence /= other
            self.boundaries /= other
            return self

    def __neg__(self):
        return DivergenceBoundaries( self.N , self.P ,
                                     - self.divergence , - self.boundaries )

    def __pos__(self):
        return DivergenceBoundaries( self.N , self.P ,
                                     + self.divergence , + self.boundaries )

    def __abs__(self):
        return DivergenceBoundaries( self.N , self.P ,
                                     abs ( self.divergence ) , abs ( self.boundaries ) )
    def copy(self):
        return DivergenceBoundaries( self.N , self.P ,
                                     self.divergence.copy() , self.boundaries.copy() )

#__________________________________________________

class DivergenceTemporalBoundaries( oto.OTObject ):
    '''
    class to store the divergence and temporal boundary conditions of a field
    '''

    def __init__( self ,
                  N , P ,
                  divergence=None , temporalBoundaries=None ):
        oto.OTObject.__init__( self ,
                               N , P )
        if divergence is None:
            self.divergence = Divergence( N , P )
        else:
            self.divergence = divergence
        if temporalBoundaries is None:
            self.temporalBoundaries = TemporalBoundaries( N , P )
        else:
            self.temporalBoundaries = temporalBoundaries

    def __repr__(self):
        return "Object representing the divergence and temporal boundary conditions of a field"

    def TdivergenceTemporalBoundaries(self):
        gridDiv = self.divergence.Tdivergence()
        gridB   = self.temporalBoundaries.TtemporalBoundaries()
        return ( gridDiv + gridB )

    def applyGaussForward(self):
        self.divergence.div[:,0]      += self.P*self.temporalBoundaries.bt0[:]
        self.divergence.div[:,self.P] -= self.P*self.temporalBoundaries.bt1[:]

    def applyGaussBackward(self):
        self.temporalBoundaries.bt0 += self.P*self.divergence.div[:,0]
        self.temporalBoundaries.bt1 -= self.P*self.divergence.div[:,self.P]

    def random( N , P ):
        return DivergenceTemporalBoundaries( N , P ,
                                             Divergence.random(N,P) , TemporalBoundaries.random(N,P) )
    random = staticmethod(random)

    def LInftyNorm(self):
        return np.max( [ self.divergence.LInftyNorm() , self.temporalBoundaries.LInftyNorm() ] )

    def __add__(self, other):
        if isinstance(other,DivergenceTemporalBoundaries):
            return DivergenceTemporalBoundaries( self.N , self.P ,
                                                 self.divergence + other.divergence , self.temporalBoundaries + other.temporalBoundaries )
        else:
            return DivergenceTemporalBoundaries( self.N , self.P ,
                                                 self.divergence + other , self.temporalBoundaries + other )

    def __sub__(self, other):
        if isinstance(other,DivergenceTemporalBoundaries):
            return DivergenceTemporalBoundaries( self.N , self.P ,
                                                 self.divergence - other.divergence , self.temporalBoundaries - other.temporalBoundaries )
        else:
            return DivergenceTemporalBoundaries( self.N , self.P ,
                                                 self.divergence - other , self.temporalBoundaries - other )

    def __mul__(self, other):
        if isinstance(other,DivergenceTemporalBoundaries):
            return DivergenceTemporalBoundaries( self.N , self.P ,
                                                 self.divergence * other.divergence , self.temporalBoundaries * other.temporalBoundaries )
        else:
            return DivergenceTemporalBoundaries( self.N , self.P ,
                                                 self.divergence * other , self.temporalBoundaries * other )

    def __div__(self, other):
        if isinstance(other,DivergenceTemporalBoundaries):
            return DivergenceTemporalBoundaries( self.N , self.P ,
                                                 self.divergence / other.divergence , self.temporalBoundaries / other.temporalBoundaries )
        else:
            return DivergenceTemporalBoundaries( self.N , self.P ,
                                                 self.divergence / other , self.temporalBoundaries / other )

    def __radd__(self, other):
        return DivergenceTemporalBoundaries( self.N , self.P ,
                                             other + self.divergence , other + self.temporalBoundaries )

    def __rsub__(self, other):
        return DivergenceTemporalBoundaries( self.N , self.P ,
                                             other - self.divergence , other - self.temporalBoundaries )

    def __rmul__(self, other):
        return DivergenceTemporalBoundaries( self.N , self.P ,
                                             other * self.divergence , other * self.temporalBoundaries )

    def __rdiv__(self, other):
        return DivergenceTemporalBoundaries( self.N , self.P ,
                                             other / self.divergence , other / self.temporalBoundaries )

    def __iadd__(self, other):
        if isinstance(other,DivergenceTemporalBoundaries):
            self.divergence += other.divergence
            self.temporalBoundaries += other.temporalBoundaries
            return self
        else:
            self.divergence += other
            self.temporalBoundaries += other
            return self

    def __isub__(self, other):
        if isinstance(other,DivergenceTemporalBoundaries):
            self.divergence -= other.divergence
            self.temporalBoundaries -= other.temporalBoundaries
            return self
        else:
            self.divergence -= other
            self.temporalBoundaries -= other
            return self

    def __imul__(self, other):
        if isinstance(other,DivergenceTemporalBoundaries):
            self.divergence *= other.divergence
            self.temporalBoundaries *= other.temporalBoundaries
            return self
        else:
            self.divergence *= other
            self.temporalBoundaries *= other
            return self

    def __idiv__(self, other):
        if isinstance(other,DivergenceTemporalBoundaries):
            self.divergence /= other.divergence
            self.temporalBoundaries /= other.temporalBoundaries
            return self
        else:
            self.divergence /= other
            self.temporalBoundaries /= other
            return self

    def __neg__(self):
        return DivergenceTemporalBoundaries( self.N , self.P ,
                                             - self.divergence , - self.temporalBoundaries )

    def __pos__(self):
        return DivergenceTemporalBoundaries( self.N , self.P ,
                                             + self.divergence , + self.temporalBoundaries )

    def __abs__(self):
        return DivergenceTemporalBoundaries( self.N , self.P ,
                                             abs ( self.divergence ) , abs ( self.temporalBoundaries ) )
    def copy(self):
        return DivergenceTemporalBoundaries( self.N , self.P ,
                                             self.divergence.copy() , self.temporalBoundaries.copy() )

#__________________________________________________

class StaggeredCenteredField( oto.OTObject ):
    '''
    class to store a staggered and a centered field
    '''

    def __init__( self ,
                  N , P ,
                  staggeredField=None , centeredField=None ):
        oto.OTObject.__init__( self ,
                               N , P )

        if staggeredField is None:
            self.staggeredField = StaggeredField( N , P )
        else:
            self.staggeredField = staggeredField

        if centeredField is None:
            self.centeredField = CenteredField( N , P )
        else:
            self.centeredField = centeredField

    def __repr__(self):
        return 'Object representing a staggered and a centered field'

    def interpolationError(self):
        return ( self.centeredField - self.staggeredField.interpolation() )

    def interpolationErrorBoundaries(self):
        centeredField = self.centeredField - self.staggeredField.interpolation()
        boundaries    = self.staggeredField.boundaries()
        return CenteredFieldBoundaries(self.N, self.P, 
                                       centeredField, boundaries) 

    def interpolationErrorReservoirBoundaries(self):
        centeredField = self.centeredField - self.staggeredField.interpolation()
        boundaries    = self.staggeredField.reservoirBoundaries()
        return CenteredFieldBoundaries(self.N, self.P, 
                                       centeredField, boundaries) 

    def interpolationErrorTemporalBoundaries(self):
        centeredField      = self.centeredField - self.staggeredField.interpolation()
        temporalBoundaries = self.staggeredField.temporalBoundaries()
        return CenteredFieldTemporalBoundaries(self.N, self.P, 
                                               centeredField, temporalBoundaries) 

    def random( N , P ):
        return StaggeredCenteredField( N , P ,
                                       StaggeredField.random(N,P) , CenteredField.random(N,P) )
    random = staticmethod(random)

    def LInftyNorm(self):
        return np.max( [ self.staggeredField.LInftyNorm() , self.centeredField.LInftyNorm() ] )

    def __add__(self, other):
        if isinstance(other,StaggeredCenteredField):
            return StaggeredCenteredField( self.N , self.P ,
                                           self.staggeredField + other.staggeredField , self.centeredField + other.centeredField )
        else:
            return StaggeredCenteredField( self.N , self.P ,
                                           self.staggeredField + other , self.centeredField + other )

    def __sub__(self, other):
        if isinstance(other,StaggeredCenteredField):
            return StaggeredCenteredField( self.N , self.P ,
                                           self.staggeredField - other.staggeredField , self.centeredField - other.centeredField )
        else:
            return StaggeredCenteredField( self.N , self.P ,
                                           self.staggeredField - other , self.centeredField - other )

    def __mul__(self, other):
        if isinstance(other,StaggeredCenteredField):
            return StaggeredCenteredField( self.N , self.P ,
                                           self.staggeredField * other.staggeredField , self.centeredField * other.centeredField )
        else:
            return StaggeredCenteredField( self.N , self.P ,
                                           self.staggeredField * other , self.centeredField * other )

    def __div__(self, other):
        if isinstance(other,StaggeredCenteredField):
            return StaggeredCenteredField( self.N , self.P ,
                                           self.staggeredField / other.staggeredField , self.centeredField / other.centeredField )
        else:
            return StaggeredCenteredField( self.N , self.P ,
                                           self.staggeredField / other , self.centeredField / other )

    def __radd__(self, other):
        return StaggeredCenteredField( self.N , self.P ,
                                       other + self.staggeredField , other + self.centeredField )

    def __rsub__(self, other):
        return StaggeredCenteredField( self.N , self.P ,
                                       other - self.staggeredField , other - self.centeredField )

    def __rmul__(self, other):
        return StaggeredCenteredField( self.N , self.P ,
                                       other * self.staggeredField , other * self.centeredField )

    def __rdiv__(self, other):
        return StaggeredCenteredField( self.N , self.P ,
                                       other / self.staggeredField , other / self.centeredField )

    def __iadd__(self, other):
        if isinstance(other,StaggeredCenteredField):
            self.staggeredField += other.staggeredField
            self.centeredField += other.centeredField
            return self
        else:
            self.staggeredField += other
            self.centeredField += other
            return self

    def __isub__(self, other):
        if isinstance(other,StaggeredCenteredField):
            self.staggeredField -= other.staggeredField
            self.centeredField -= other.centeredField
            return self
        else:
            self.staggeredField -= other
            self.centeredField -= other
            return self

    def __imul__(self, other):
        if isinstance(other,StaggeredCenteredField):
            self.staggeredField *= other.staggeredField
            self.centeredField *= other.centeredField
            return self
        else:
            self.staggeredField *= other
            self.centeredField *= other
            return self

    def __idiv__(self, other):
        if isinstance(other,StaggeredCenteredField):
            self.staggeredField /= other.staggeredField
            self.centeredField /= other.centeredField
            return self
        else:
            self.staggeredField /= other
            self.centeredField /= other
            return self

    def __neg__(self):
        return StaggeredCenteredField( self.N , self.P ,
                                       - self.staggeredField , - self.centeredField )

    def __pos__(self):
        return StaggeredCenteredField( self.N , self.P ,
                                       + self.staggeredField , + self.centeredField )

    def __abs__(self):
        return StaggeredCenteredField( self.N , self.P ,
                                       abs ( self.staggeredField ) , abs ( self.centeredField ) )
    def copy(self):
        return StaggeredCenteredField( self.N , self.P ,
                                       self.staggeredField.copy() , self.centeredField.copy() )

#__________________________________________________

class CenteredFieldBoundaries( oto.OTObject ):
    '''
    class to store a centered field and boundary conditions
    '''

    def __init__( self ,
                  N , P ,
                  centeredField=None , boundaries=None ):

        oto.OTObject.__init__( self ,
                               N , P )

        if centeredField is None:
            self.centeredField = CenteredField(N,P)
        else:
            self.centeredField = centeredField

        if boundaries is None:
            self.boundaries = Boundaries(N,P)
        else:
            self.boundaries = boundaries

    def __repr__(self):
        return 'Object representing a centered field and boundary conditions'

    def TinterpolationErrorBoundaries(self):
        scField  = self.centeredField.TinterpolationError()
        scField += StaggeredCenteredField( self.N , self.P ,
                                           self.boundaries.Tboundaries() )
        return scField

    def TinterpolationErrorReservoirBoundaries(self):
        scField  = self.centeredField.TinterpolationError()
        scField += StaggeredCenteredField( self.N , self.P ,
                                           self.boundaries.TreservoirBoundaries() )
        return scField

    def random( N , P ):
        return CenteredFieldBoundaries( N , P ,
                                        CenteredField.random(N,P) , Boundaries.random(N,P) )
    random = staticmethod(random)

    def LInftyNorm(self):
        return np.max( [ self.centeredField.LInftyNorm() , self.boundaries.LInftyNorm() ] )

    def __add__(self, other):
        if isinstance(other,CenteredFieldBoundaries):
            return CenteredFieldBoundaries( self.N , self.P ,
                                            self.centeredField + other.centeredField , self.boundaries + other.boundaries )
        else:
            return CenteredFieldBoundaries( self.N , self.P ,
                                            self.centeredField + other , self.boundaries + other )

    def __sub__(self, other):
        if isinstance(other,CenteredFieldBoundaries):
            return CenteredFieldBoundaries( self.N , self.P ,
                                            self.centeredField - other.centeredField , self.boundaries - other.boundaries )
        else:
            return CenteredFieldBoundaries( self.N , self.P ,
                                            self.centeredField - other , self.boundaries - other )

    def __mul__(self, other):
        if isinstance(other,CenteredFieldBoundaries):
            return CenteredFieldBoundaries( self.N , self.P ,
                                            self.centeredField * other.centeredField , self.boundaries * other.boundaries )
        else:
            return CenteredFieldBoundaries( self.N , self.P ,
                                            self.centeredField * other , self.boundaries * other )

    def __div__(self, other):
        if isinstance(other,CenteredFieldBoundaries):
            return CenteredFieldBoundaries( self.N , self.P ,
                                            self.centeredField / other.centeredField , self.boundaries / other.boundaries )
        else:
            return CenteredFieldBoundaries( self.N , self.P ,
                                            self.centeredField / other , self.boundaries / other )

    def __radd__(self, other):
        return CenteredFieldBoundaries( self.N , self.P ,
                                        other + self.centeredField , other + self.boundaries )

    def __rsub__(self, other):
        return CenteredFieldBoundaries( self.N , self.P ,
                                        other - self.centeredField , other - self.boundaries )

    def __rmul__(self, other):
        return CenteredFieldBoundaries( self.N , self.P ,
                                        other * self.centeredField , other * self.boundaries )

    def __rdiv__(self, other):
        return CenteredFieldBoundaries( self.N , self.P ,
                                        other / self.centeredField , other / self.boundaries )

    def __iadd__(self, other):
        if isinstance(other,CenteredFieldBoundaries):
            self.centeredField += other.centeredField
            self.boundaries += other.boundaries
            return self
        else:
            self.centeredField += other
            self.boundaries += other
            return self

    def __isub__(self, other):
        if isinstance(other,CenteredFieldBoundaries):
            self.centeredField -= other.centeredField
            self.boundaries -= other.boundaries
            return self
        else:
            self.centeredField -= other
            self.boundaries -= other
            return self

    def __imul__(self, other):
        if isinstance(other,CenteredFieldBoundaries):
            self.centeredField *= other.centeredField
            self.boundaries *= other.boundaries
            return self
        else:
            self.centeredField *= other
            self.boundaries *= other
            return self

    def __idiv__(self, other):
        if isinstance(other,CenteredFieldBoundaries):
            self.centeredField /= other.centeredField
            self.boundaries /= other.boundaries
            return self
        else:
            self.centeredField /= other
            self.boundaries /= other
            return self

    def __neg__(self):
        return CenteredFieldBoundaries( self.N , self.P ,
                                        - self.centeredField , - self.boundaries )

    def __pos__(self):
        return CenteredFieldBoundaries( self.N , self.P ,
                                        + self.centeredField , + self.boundaries )

    def __abs__(self):
        return CenteredFieldBoundaries( self.N , self.P ,
                                        abs ( self.centeredField ) , abs ( self.boundaries ) )
    def copy(self):
        return CenteredFieldBoundaries( self.N , self.P ,
                                        self.centeredField.copy() , self.boundaries.copy() )

#__________________________________________________

class CenteredFieldTemporalBoundaries( oto.OTObject ):
    '''
    class to store a centered field and temporal boundary conditions
    '''

    def __init__( self ,
                  N , P ,
                  centeredField=None , temporalBoundaries=None ):
        oto.OTObject.__init__( self ,
                               N , P )
        if centeredField is None:
            self.centeredField = CenteredField( N , P )
        else:
            self.centeredField = centeredField

        if temporalBoundaries is None:
            self.temporalBoundaries = TemporalBoundaries( N , P )
        else:
            self.temporalBoundaries = temporalBoundaries

    def __repr__(self):
        return 'Object representing a centered field and temporal boundary conditions'

    def TinterpolationErrorTemporalBoundaries(self):
        scField  = self.centeredField.TinterpolationError()
        scField += StaggeredCenteredField( self.N , self.P ,
                                           self.temporalBoundaries.TtemporalBoundaries() )
        return scField

    def random( N , P ):
        return CenteredFieldTemporalBoundaries( N , P ,
                                                CenteredField.random(N,P) , TemporalBoundaries.random(N,P) )
    random = staticmethod(random)

    def LInftyNorm(self):
        return np.max( [ self.centeredField.LInftyNorm() , self.temporalBoundaries.LInftyNorm() ] )

    def __add__(self, other):
        if isinstance(other,CenteredFieldTemporalBoundaries):
            return CenteredFieldTemporalBoundaries( self.N , self.P ,
                                                    self.centeredField + other.centeredField , self.temporalBoundaries + other.temporalBoundaries )
        else:
            return CenteredFieldTemporalBoundaries( self.N , self.P ,
                                                    self.centeredField + other , self.temporalBoundaries + other )

    def __sub__(self, other):
        if isinstance(other,CenteredFieldTemporalBoundaries):
            return CenteredFieldTemporalBoundaries( self.N , self.P ,
                                                    self.centeredField - other.centeredField , self.temporalBoundaries - other.temporalBoundaries )
        else:
            return CenteredFieldTemporalBoundaries( self.N , self.P ,
                                                    self.centeredField - other , self.temporalBoundaries - other )

    def __mul__(self, other):
        if isinstance(other,CenteredFieldTemporalBoundaries):
            return CenteredFieldTemporalBoundaries( self.N , self.P ,
                                                    self.centeredField * other.centeredField , self.temporalBoundaries * other.temporalBoundaries )
        else:
            return CenteredFieldTemporalBoundaries( self.N , self.P ,
                                                    self.centeredField * other , self.temporalBoundaries * other )

    def __div__(self, other):
        if isinstance(other,CenteredFieldTemporalBoundaries):
            return CenteredFieldTemporalBoundaries( self.N , self.P ,
                                                    self.centeredField / other.centeredField , self.temporalBoundaries / other.temporalBoundaries )
        else:
            return CenteredFieldTemporalBoundaries( self.N , self.P ,
                                                    self.centeredField / other , self.temporalBoundaries / other )

    def __radd__(self, other):
        return CenteredFieldTemporalBoundaries( self.N , self.P ,
                                                other + self.centeredField , other + self.temporalBoundaries )

    def __rsub__(self, other):
        return CenteredFieldTemporalBoundaries( self.N , self.P ,
                                                other - self.centeredField , other - self.temporalBoundaries )

    def __rmul__(self, other):
        return CenteredFieldTemporalBoundaries( self.N , self.P ,
                                                other * self.centeredField , other * self.temporalBoundaries )

    def __rdiv__(self, other):
        return CenteredFieldTemporalBoundaries( self.N , self.P ,
                                                other / self.centeredField , other / self.temporalBoundaries )

    def __iadd__(self, other):
        if isinstance(other,CenteredFieldTemporalBoundaries):
            self.centeredField += other.centeredField
            self.temporalBoundaries += other.temporalBoundaries
            return self
        else:
            self.centeredField += other
            self.temporalBoundaries += other
            return self

    def __isub__(self, other):
        if isinstance(other,CenteredFieldTemporalBoundaries):
            self.centeredField -= other.centeredField
            self.temporalBoundaries -= other.temporalBoundaries
            return self
        else:
            self.centeredField -= other
            self.temporalBoundaries -= other
            return self

    def __imul__(self, other):
        if isinstance(other,CenteredFieldTemporalBoundaries):
            self.centeredField *= other.centeredField
            self.temporalBoundaries *= other.temporalBoundaries
            return self
        else:
            self.centeredField *= other
            self.temporalBoundaries *= other
            return self

    def __idiv__(self, other):
        if isinstance(other,CenteredFieldTemporalBoundaries):
            self.centeredField /= other.centeredField
            self.temporalBoundaries /= other.temporalBoundaries
            return self
        else:
            self.centeredField /= other
            self.temporalBoundaries /= other
            return self

    def __neg__(self):
        return CenteredFieldTemporalBoundaries( self.N , self.P ,
                                                - self.centeredField , - self.temporalBoundaries )

    def __pos__(self):
        return CenteredFieldTemporalBoundaries( self.N , self.P ,
                                                + self.centeredField , + self.temporalBoundaries )

    def __abs__(self):
        return CenteredFieldTemporalBoundaries( self.N , self.P ,
                                                abs ( self.centeredField ) , abs ( self.temporalBoundaries ) )
    def copy(self):
        return CenteredFieldTemporalBoundaries( self.N , self.P ,
                                                self.centeredField.copy() , self.temporalBoundaries.copy() )

