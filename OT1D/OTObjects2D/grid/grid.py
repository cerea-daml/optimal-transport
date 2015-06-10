#########
# grid.py
#########
#
# Contains all the classes related to the grid
#

import numpy as np
from ..OTObject import OTObject
from ...utils   import cardan

#__________________________________________________

class Field( OTObject ):
    '''
    Default class to handle a field (mx,my,f)
    '''

    def __init__( self ,
                  M , N , P ,
                  mx , my , f ):
        OTObject.__init__( self ,
                           M , N , P )
        self.mx = mx
        self.my = my
        self.f = f

    def __repr__(self):
        return 'Object representing a field (mx,my,f)'

    def LInftyNorm(self):
        return np.max( [ np.abs(self.mx).max() ,
                         np.abs(self.my).max() ,
                         np.abs(self.f ).max() ] )

    def __add__(self, other):
        if isinstance(other,Field):
            return Field( self.M , self.N , self.P ,
                          self.mx + other.mx , self.my + other.my , self.f + other.f )
        else:
            return Field( self.M , self.N , self.P ,
                          self.mx + other , self.my + other , self.f + other )

    def __sub__(self, other):
        if isinstance(other,Field):
            return Field( self.M , self.N , self.P ,
                          self.mx - other.mx , self.my - other.my , self.f - other.f )
        else:
            return Field( self.M , self.N , self.P ,
                          self.mx - other , self.my - other , self.f - other )

    def __mul__(self, other):
        if isinstance(other,Field):
            return Field( self.M , self.N , self.P ,
                          self.mx * other.mx , self.my * other.my , self.f * other.f )
        else:
            return Field( self.M , self.N , self.P ,
                          self.mx * other , self.my * other , self.f * other )

    def __div__(self, other):
        if isinstance(other,Field):
            return Field( self.M , self.N , self.P ,
                          self.mx / other.mx , self.my / other.my , self.f / other.f )
        else:
            return Field( self.M , self.N , self.P ,
                          self.mx / other , self.my / other , self.f / other )

    def __radd__(self, other):
        return Field( self.M , self.N , self.P ,
                      other + self.mx , other + self.my , other + self.f )

    def __rsub__(self, other):
        return Field( self.M , self.N , self.P ,
                      other - self.mx , other - self.my , other - self.f )

    def __rmul__(self, other):
        return Field( self.M , self.N , self.P ,
                      other * self.mx , other * self.my , other * self.f )

    def __rdiv__(self, other):
        return Field( self.M , self.N , self.P ,
                      other / self.mx , other / self.my , other / self.f )

    def __iadd__(self, other):
        if isinstance(other,Field):
            self.mx += other.mx
            self.my += other.my
            self.f += other.f
            return self
        else:
            self.mx += other
            self.my += other
            self.f += other
            return self

    def __isub__(self, other):
        if isinstance(other,Field):
            self.mx -= other.mx
            self.my -= other.my
            self.f -= other.f
            return self
        else:
            self.mx -= other
            self.my -= other
            self.f -= other
            return self

    def __imul__(self, other):
        if isinstance(other,Field):
            self.mx *= other.mx
            self.my *= other.my
            self.f *= other.f
            return self
        else:
            self.mx *= other
            self.my *= other
            self.f *= other
            return self

    def __idiv__(self, other):
        if isinstance(other,Field):
            self.mx /= other.mx
            self.my /= other.my
            self.f /= other.f
            return self
        else:
            self.mx /= other
            self.my /= other
            self.f /= other
            return self

    def __neg__(self):
        return Field( self.M , self.N , self.P ,
                      - self.mx , - self.my , - self.f )

    def __pos__(self):
        return Field( self.M , self.N , self.P ,
                      + self.mx , + self.my , + self.f )

    def __abs__(self):
        return Field( self.M , self.N , self.P ,
                      abs ( self.mx ) , abs ( self.my ) , abs ( self.f ) )
    def copy(self):
        return Field( self.M , self.N , self.P ,
                      self.mx.copy() , self.my.copy() , self.f.copy() )

#__________________________________________________

class StaggeredField( Field ):
    '''
    Class to handle a field defined on a staggered grid
    '''

    def __init__( self ,
                  M , N , P ,
                  mx=None , my=None , f=None ):

        if mx is None:
            mx = np.zeros(shape=(M+2,N+1,P+1))
        if my is None:
            my = np.zeros(shape=(M+1,N+2,P+1))
        if f is None:
            f  = np.zeros(shape=(M+1,N+1,P+2))
        
        Field.__init__( self ,
                        M , N , P ,
                        mx , my , f )

    def __repr__(self):
        return 'Object representing a field (mx,my,f) on a staggered grid'

    def random(M, N, P):
        return StaggeredField( M , N , P ,
                               np.random.rand(M+2,N+1,P+1) , 
                               np.random.rand(M+1,N+2,P+1) ,
                               np.random.rand(M+1,N+1,P+2) )
    random = staticmethod(random)

    def interpolation(self):
        mx = np.zeros(shape=(self.M+1,self.N+1,self.P+1))
        mx[:,:,:]           = 0.5*self.mx[0:self.M+1,:,:]
        mx[0:self.M+1,:,:] += 0.5*self.mx[1:self.M+2,:,:]

        my = np.zeros(shape=(self.M+1,self.N+1,self.P+1))
        my[:,:,:]           = 0.5*self.my[:,0:self.N+1,:]
        my[:,0:self.N+1,:] += 0.5*self.my[:,1:self.N+2,:]

        f  = np.zeros(shape=(self.M+1,self.N+1,self.P+1))
        f[:,:,:]            = 0.5*self.f[:,:,0:self.P+1]
        f[:,:,0:self.P+1]  += 0.5*self.f[:,:,1:self.P+2]

        return CenteredField( self.M, self.N, self.P,
                              mx, my, f )

    def divergence(self):
        div = ( self.M*( self.mx[1:self.M+2,:,:] - self.mx[0:self.M+1,:,:] ) +
                self.N*( self.my[:,1:self.N+2,:] - self.my[:,0:self.N+1,:] ) +
                self.P*( self.f[:,:,1:self.P+2]  - self.f[:,:,0:self.P+1]  ) )
        return Divergence( self.M , self.N , self.P , div )

    def temporalBoundaries(self):
        return TemporalBoundaries( self.M , self.N, self.P,
                                   self.f[:,:,0].copy(), self.f[:,:,self.P+1].copy() )

    def temporalReservoirBoundaries(self):
        trb = self.temporalBoundaries()
        trb.bt1[0,:]      = 0.
        trb.bt1[self.M,:] = 0.
        trb.bt1[:,0]      = 0.
        trb.bt1[:,self.N] = 0.
        return trb

    def spatialBoundaries(self):
        return SpatialBoundaries( self.M, self.N, self.P,
                                  self.mx[0,:,:].copy(), self.mx[self.M+1,:,:].copy(),
                                  self.my[:,0,:].copy(), self.my[:,self.N+1,:].copy() )

    def boundaries(self):
        return Boundaries( self.M, self.N, self.P,
                           self.temporalBoundaries(), self.spatialBoundaries() )

    def reservoirBoundaries(self):
        return Boundaries( self.M, self.N, self.P,
                           self.temporalReservoirBoundaries(), self.spatialBoundaries() )

    def divergenceBoundaries(self):
        return DivergenceBoundaries( self.M, self.N, self.P,
                                     self.divergence(), self.boundaries() )

    def divergenceTemporalBoundaries(self):
        return DivergenceTemporalBoundaries( self.M, self.N, self.P,
                                             self.divergence(), self.temporalBoundaries() )

    def __add__(self, other):
        if isinstance(other,StaggeredField):
            return StaggeredField( self.M , self.N , self.P ,
                                   self.mx + other.mx , self.my + other.my , self.f + other.f )
        else:
            return StaggeredField( self.M , self.N , self.P ,
                                   self.mx + other , self.my + other , self.f + other )

    def __sub__(self, other):
        if isinstance(other,StaggeredField):
            return StaggeredField( self.M , self.N , self.P ,
                                   self.mx - other.mx , self.my - other.my , self.f - other.f )
        else:
            return Field( self.M , self.N , self.P ,
                          self.mx - other , self.my - other , self.f - other )

    def __mul__(self, other):
        if isinstance(other,StaggeredField):
            return StaggeredField( self.M , self.N , self.P ,
                                   self.mx * other.mx , self.my * other.my , self.f * other.f )
        else:
            return StaggeredField( self.M , self.N , self.P ,
                                   self.mx * other , self.my * other , self.f * other )

    def __div__(self, other):
        if isinstance(other,StaggeredField):
            return StaggeredField( self.M , self.N , self.P ,
                                   self.mx / other.mx , self.my / other.my , self.f / other.f )
        else:
            return StaggeredField( self.M , self.N , self.P ,
                                   self.mx / other , self.my / other , self.f / other )

    def __radd__(self, other):
        return StaggeredField( self.M , self.N , self.P ,
                               other + self.mx , other + self.my , other + self.f )

    def __rsub__(self, other):
        return StaggeredField( self.M , self.N , self.P ,
                               other - self.mx , other - self.my , other - self.f )

    def __rmul__(self, other):
        return StaggeredField( self.M , self.N , self.P ,
                               other * self.mx , other * self.my , other * self.f )

    def __rdiv__(self, other):
        return StaggeredField( self.M , self.N , self.P ,
                               other / self.mx , other / self.my , other / self.f )

    def __iadd__(self, other):
        if isinstance(other,StaggeredField):
            self.mx += other.mx
            self.my += other.my
            self.f += other.f
            return self
        else:
            self.mx += other
            self.my += other
            self.f += other
            return self

    def __isub__(self, other):
        if isinstance(other,StaggeredField):
            self.mx -= other.mx
            self.my -= other.my
            self.f -= other.f
            return self
        else:
            self.mx -= other
            self.my -= other
            self.f -= other
            return self

    def __imul__(self, other):
        if isinstance(other,StaggeredField):
            self.mx *= other.mx
            self.my *= other.my
            self.f *= other.f
            return self
        else:
            self.mx *= other
            self.my *= other
            self.f *= other
            return self

    def __idiv__(self, other):
        if isinstance(other,StaggeredField):
            self.mx /= other.mx
            self.my /= other.my
            self.f /= other.f
            return self
        else:
            self.mx /= other
            self.my /= other
            self.f /= other
            return self

    def __neg__(self):
        return StaggeredField( self.M , self.N , self.P ,
                               - self.mx , - self.my , - self.f )

    def __pos__(self):
        return StaggeredField( self.M , self.N , self.P ,
                               + self.mx , + self.my , + self.f )

    def __abs__(self):
        return StaggeredField( self.M , self.N , self.P ,
                               abs ( self.mx ) , abs ( self.my ) , abs ( self.f ) )
    def copy(self):
        return StaggeredField( self.M , self.N , self.P ,
                               self.mx.copy() , self.my.copy() , self.f.copy() )

#__________________________________________________

class CenteredField( Field ):
    '''
    Class to handle a field defined on a centered grid
    '''

    def __init__( self ,
                  M , N , P ,
                  mx=None , my=None , f=None ):
        OTObject.__init__( self ,
                           M , N , P )
        
        if mx is None:
            mx = np.zeros(shape=(M+1,N+1,P+1))
        if my is None:
            my = np.zeros(shape=(M+1,N+1,P+1))
        if f is None:
            f  = np.zeros(shape=(M+1,N+1,P+1))

        Field.__init__( self ,
                        M , N , P ,
                        mx , my , f )

    def __repr__(self):
        return 'Object representing a field (m,f) on a centered grid'

    def random(M, N, P):
        return CenteredField( M , N , P ,
                              np.random.rand(M+1,N+1,P+1) ,
                              np.random.rand(M+1,N+1,P+1) ,
                              np.random.rand(M+1,N+1,P+1) )
    random = staticmethod(random)

    def functionalJ(self):
        return ( ( self.mx * self.mx +
                   self.my * self.my ) *
                 ( self.f > 0 ) / 
                 ( self.f * ( self.f > 0 ) + 1. * ( 1. - ( self.f > 0 ) ) ) ).sum()

    def proximalJ(self, gamma):
        unity = np.ones(shape=self.f.shape)
        fstar = cardan.maxRoot( unity,
                                2*gamma-self.f,
                                gamma**2-2*gamma*self.f,
                                -(gamma**2*self.f+0.5*gamma*( self.mx*self.mx + self.my*self.my )) )

        fstar = np.maximum( fstar, 0. )
        mx = ( fstar * self.mx ) / ( fstar + gamma )
        my = ( fstar * self.my ) / ( fstar + gamma )
        return CenteredField(self.M, self.N, self.P, mx, my, fstar)

    def Tinterpolation(self):
        mx = np.zeros(shape=(self.M+2,self.N+1,self.P+1))
        mx[0:self.M+1,:,:]  = 0.5*self.mx[:,:,:]
        mx[1:self.M+2,:,:] += 0.5*self.mx[:,:,:]

        my = np.zeros(shape=(self.M+1,self.N+2,self.P+1))
        my[:,0:self.N+1,:]  = 0.5*self.my[:,:,:]
        my[:,1:self.N+2,:] += 0.5*self.my[:,:,:]

        f  = np.zeros(shape=(self.M+1,self.N+1,self.P+2))
        f[:,:,0:self.P+1]   = 0.5*self.f[:,:,:]
        f[:,:,1:self.P+2]  += 0.5*self.f[:,:,:]

        return StaggeredField( self.M, self.N, self.P,
                               mx, my, f )

    def TinterpolationError(self):
        mxu = np.zeros(shape=(self.M+2,self.N+1,self.P+1))
        myu = np.zeros(shape=(self.M+1,self.N+2,self.P+1))
        fu  = np.zeros(shape=(self.M+1,self.N+1,self.P+2))

        mxu[0:self.M+1,:,:] = -0.5*self.mx[:,:,:]
        mxu[1:self.M+2,:,:] -= 0.5*self.mx[:,:,:]

        myu[:,0:self.N+1,:] = -0.5*self.my[:,:,:]
        myu[:,1:self.N+2,:] -= 0.5*self.my[:,:,:]

        fu[:,:,0:self.P+1]  = -0.5*self.f[:,:,:]
        fu[:,:,1:self.P+2]  -= 0.5*self.f[:,:,:]

        staggeredField = StaggeredField( self.M , self.N , self.P , mxu , myu , fu )

        return StaggeredCenteredField( self.M, self.N , self.P , staggeredField , self )

    def __add__(self, other):
        if isinstance(other,CenteredField):
            return CenteredField( self.M , self.N , self.P ,
                                  self.mx + other.mx , self.my + other.my , self.f + other.f )
        else:
            return CenteredField( self.M , self.N , self.P ,
                                  self.mx + other , self.my + other , self.f + other )

    def __sub__(self, other):
        if isinstance(other,CenteredField):
            return CenteredField( self.M , self.N , self.P ,
                                  self.mx - other.mx , self.my - other.my , self.f - other.f )
        else:
            return CenteredField( self.M , self.N , self.P ,
                                  self.mx - other , self.my - other , self.f - other )

    def __mul__(self, other):
        if isinstance(other,CenteredField):
            return CenteredField( self.M , self.N , self.P ,
                                  self.mx * other.mx , self.my * other.my , self.f * other.f )
        else:
            return CenteredField( self.M , self.N , self.P ,
                                  self.mx * other , self.my * other , self.f * other )

    def __div__(self, other):
        if isinstance(other,CenteredField):
            return CenteredField( self.M , self.N , self.P ,
                                  self.mx / other.mx , self.my / other.my , self.f / other.f )
        else:
            return CenteredField( self.M , self.N , self.P ,
                                  self.mx / other , self.my / other , self.f / other )

    def __radd__(self, other):
        return CenteredField( self.M , self.N , self.P ,
                              other + self.mx , other + self.my , other + self.f )

    def __rsub__(self, other):
        return CenteredField( self.M , self.N , self.P ,
                              other - self.mx , other - self.my , other - self.f )

    def __rmul__(self, other):
        return CenteredField( self.M , self.N , self.P ,
                              other * self.mx , other * self.my , other * self.f )

    def __rdiv__(self, other):
        return CenteredField( self.M , self.N , self.P ,
                              other / self.mx , other / self.my , other / self.f )

    def __iadd__(self, other):
        if isinstance(other,CenteredField):
            self.mx += other.mx
            self.my += other.my
            self.f += other.f
            return self
        else:
            self.mx += other
            self.my += other
            self.f += other
            return self

    def __isub__(self, other):
        if isinstance(other,CenteredField):
            self.mx -= other.mx
            self.my -= other.my
            self.f -= other.f
            return self
        else:
            self.mx -= other
            self.my -= other
            self.f -= other
            return self

    def __imul__(self, other):
        if isinstance(other,CenteredField):
            self.mx *= other.mx
            self.my *= other.my
            self.f *= other.f
            return self
        else:
            self.mx *= other
            self.my *= other
            self.f *= other
            return self

    def __idiv__(self, other):
        if isinstance(other,CenteredField):
            self.mx /= other.mx
            self.my /= other.my
            self.f /= other.f
            return self
        else:
            self.mx /= other
            self.my /= other
            self.f /= other
            return self

    def __neg__(self):
        return CenteredField( self.M , self.N , self.P ,
                              - self.mx , - self.my , - self.f )

    def __pos__(self):
        return CenteredField( self.M , self.N , self.P ,
                              + self.mx , + self.my , + self.f )

    def __abs__(self):
        return CenteredField( self.M , self.N , self.P ,
                              abs ( self.mx ) , abs ( self.my ) , abs ( self.f ) )
    def copy(self):
        return CenteredField( self.M , self.N , self.P ,
                              self.mx.copy() , self.my.copy() , self.f.copy() )

#__________________________________________________

class Divergence( OTObject ):
    '''
    class to handle the divergence of a field
    '''

    def __init__( self ,
                  M , N , P ,
                  div=None ):
        OTObject.__init__( self ,
                           M , N , P )
        if div is None:
            self.div = np.zeros(shape=(M+1,N+1,P+1))
        else:
            self.div = div

    def __repr__(self):
        return 'Object representing the divergence of a field'

    def random(M, N, P):
        return Divergence( M, N , P ,
                           np.random.rand(M+1,N+1,P+1) )
    random = staticmethod(random)

    def Tdivergence(self):
        mx = np.zeros(shape=(self.M+2,self.N+1,self.P+1))
        mx[0:self.M+1,:,:] = -self.M*self.div[0:self.M+1,:,:]
        mx[1:self.M+2,:,:] += self.M*self.div[0:self.M+1,:,:]

        my = np.zeros(shape=(self.M+1,self.N+2,self.P+1))
        my[:,0:self.N+1,:] = -self.N*self.div[:,0:self.N+1,:]
        my[:,1:self.N+2,:] += self.N*self.div[:,0:self.N+1,:]

        f  = np.zeros(shape=(self.M+1,self.N+1,self.P+2))
        f[:,:,0:self.P+1]  = -self.P*self.div[:,:,0:self.P+1]
        f[:,:,1:self.P+2]  += self.P*self.div[:,:,0:self.P+1]

        return StaggeredField( self.M, self.N, self.P,
                               mx, my, f )

    def sum(self):
        return self.div.sum()

    def LInftyNorm(self):
        return np.abs(self.div).max()

    def __add__(self, other):
        if isinstance(other,Divergence):
            return Divergence( self.M , self.N , self.P ,
                               self.div + other.div )
        else:
            return Divergence( self.M , self.N , self.P ,
                               self.div + other )

    def __sub__(self, other):
        if isinstance(other,Divergence):
            return Divergence( self.M , self.N , self.P ,
                               self.div - other.div )
        else:
            return Divergence( self.M , self.N , self.P ,
                               self.div - other )

    def __mul__(self, other):
        if isinstance(other,Divergence):
            return Divergence( self.M , self.N , self.P ,
                               self.div * other.div )
        else:
            return Divergence( self.M , self.N , self.P ,
                               self.div * other )

    def __div__(self, other):
        if isinstance(other,Divergence):
            return Divergence( self.M , self.N , self.P ,
                               self.div / other.div )
        else:
            return Divergence( self.M , self.N , self.P ,
                               self.div / other )

    def __radd__(self, other):
        return Divergence( self.M , self.N , self.P ,
                           other + self.div )

    def __rsub__(self, other):
        return Divergence( self.M , self.N , self.P ,
                           other - self.div )

    def __rmul__(self, other):
        return Divergence( self.M , self.N , self.P ,
                           other * self.div )

    def __rdiv__(self, other):
        return Divergence( self.M , self.N , self.P ,
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
        return Divergence( self.M , self.N , self.P ,
                           - self.div )

    def __pos__(self):
        return Divergence( self.M , self.N , self.P ,
                           + self.div )

    def __abs__(self):
        return Divergence( self.M , self.N , self.P ,
                           abs ( self.div ) )
    def copy(self):
        return Divergence( self.M , self.N , self.P ,
                           self.div.copy() )

#__________________________________________________

class TemporalBoundaries( OTObject ):
    '''
    class to store the temporal boundaries of a field
    '''

    def __init__( self ,
                  M , N , P ,
                  bt0=None , bt1=None ):
        OTObject.__init__( self ,
                           M , N , P )
        if bt0 is None:
            self.bt0 = np.zeros(shape=(M+1,N+1))
        else:
            self.bt0 = bt0
        if bt1 is None:
            self.bt1 = np.zeros(shape=(M+1,N+1))
        else:
            self.bt1 = bt1


    def __repr__(self):
        return 'Object representing the temporal boundaries of a field'

    def random( M , N , P ):
        bt0 = np.random.rand(M+1,N+1)
        bt1 = np.random.rand(M+1,N+1)
        return TemporalBoundaries( M , N , P ,
                                   bt0 , bt1 )
    random = staticmethod(random)

    def TtemporalBoundaries(self):
        mx = np.zeros(shape=(self.M+2,self.N+1,self.P+1))
        my = np.zeros(shape=(self.M+1,self.N+2,self.P+1))
        f  = np.zeros(shape=(self.M+1,self.N+1,self.P+2))

        f[:,:,0]        = self.bt0[:,:]
        f[:,:,self.P+1] = self.bt1[:,:]

        return StaggeredField( self.M, self.N, self.P,
                               mx, my, f )

    def TtemporalReservoirBoundaries(self):
        mx = np.zeros(shape=(self.M+2,self.N+1,self.P+1))
        my = np.zeros(shape=(self.M+1,self.N+2,self.P+1))
        f  = np.zeros(shape=(self.M+1,self.N+1,self.P+2))

        f[:,:,0] = self.bt0[:,:]
        f[1:self.M,1:self.N,self.P+1] = self.bt1[1:self.M,1:self.N]

        return StaggeredField( self.M, self.N, self.P,
                               mx, my, f )

    def massDefault(self):
        return ( self.P * ( self.bt0.sum() - self.bt1.sum() ) )

    def scalingMassDefault(self):
        return ( self.P * ( self.bt0.sum() + self.bt1.sum() ) )

    def LInftyNorm(self):
        return np.max( [ abs(self.bt0).max() , abs(self.bt1).max() ] )

    def swap(self):
        btswap = self.bt1.copy()
        self.bt1 = self.bt0.copy()
        self.bt0 = btswap


    def __add__(self, other):
        if isinstance(other,TemporalBoundaries):
            return TemporalBoundaries( self.M , self.N , self.P ,
                                       self.bt0 + other.bt0 , self.bt1 + other.bt1 )
        else:
            return TemporalBoundaries( self.M , self.N , self.P ,
                                       self.bt0 + other , self.bt1 + other )

    def __sub__(self, other):
        if isinstance(other,TemporalBoundaries):
            return TemporalBoundaries( self.M , self.N , self.P ,
                                       self.bt0 - other.bt0 , self.bt1 - other.bt1 )
        else:
            return TemporalBoundaries( self.M , self.N , self.P ,
                                       self.bt0 - other , self.bt1 - other )

    def __mul__(self, other):
        if isinstance(other,TemporalBoundaries):
            return TemporalBoundaries( self.M , self.N , self.P ,
                                       self.bt0 * other.bt0 , self.bt1 * other.bt1 )
        else:
            return TemporalBoundaries( self.M , self.N , self.P ,
                                       self.bt0 * other , self.bt1 * other )

    def __div__(self, other):
        if isinstance(other,TemporalBoundaries):
            return TemporalBoundaries( self.M , self.N , self.P ,
                                       self.bt0 / other.bt0 , self.bt1 / other.bt1 )
        else:
            return TemporalBoundaries( self.M , self.N , self.P ,
                                       self.bt0 / other , self.bt1 / other )

    def __radd__(self, other):
        return TemporalBoundaries( self.M , self.N , self.P ,
                                   other + self.bt0 , other + self.bt1 )

    def __rsub__(self, other):
        return TemporalBoundaries( self.M , self.N , self.P ,
                                   other - self.bt0 , other - self.bt1 )

    def __rmul__(self, other):
        return TemporalBoundaries( self.M , self.N , self.P ,
                                   other * self.bt0 , other * self.bt1 )

    def __rdiv__(self, other):
        return TemporalBoundaries( self.M , self.N , self.P ,
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
        return TemporalBoundaries( self.M , self.N , self.P ,
                                   - self.bt0 , - self.bt1 )

    def __pos__(self):
        return TemporalBoundaries( self.M , self.N , self.P ,
                                   + self.bt0 , + self.bt1 )

    def __abs__(self):
        return TemporalBoundaries( self.M , self.N , self.P ,
                                   abs ( self.bt0 ) , abs ( self.bt1 ) )
    def copy(self):
        return TemporalBoundaries( self.M , self.N , self.P ,
                                   self.bt0.copy() , self.bt1.copy() )

#__________________________________________________

class SpatialBoundaries( OTObject ):
    '''
    class to store the spatial boundaries of a field
    '''

    def __init__( self ,
                  M , N , P ,
                  bx0=None , bx1=None , by0=None , by1=None ):
        OTObject.__init__( self ,
                           M , N , P )

        if bx0 is None:
            self.bx0 = np.zeros(shape=(N+1,P+1))
        else:
            self.bx0 = bx0
        if bx1 is None:
            self.bx1 = np.zeros(shape=(N+1,P+1))
        else:
            self.bx1 = bx1

        if by0 is None:
            self.by0 = np.zeros(shape=(M+1,P+1))
        else:
            self.by0 = by0
        if by1 is None:
            self.by1 = np.zeros(shape=(M+1,P+1))
        else:
            self.by1 = by1

    def __repr__(self):
        return 'Object representing the spatial boundaries of a field'

    def random( M , N , P ):
        bx0 = np.random.rand(N+1,P+1)
        bx1 = np.random.rand(N+1,P+1)
        
        by0 = np.random.rand(M+1,P+1)
        by1 = np.random.rand(M+1,P+1)
        return SpatialBoundaries( M , N , P ,
                                  bx0 , bx1 , by0 , by1 )
    random = staticmethod(random)

    def TspatialBoundaries(self):
        mx = np.zeros(shape=(self.M+2,self.N+1,self.P+1))
        my = np.zeros(shape=(self.M+1,self.N+2,self.P+1))
        f  = np.zeros(shape=(self.M+1,self.N+1,self.P+2))

        mx[0,:,:]        = self.bx0[:,:]
        mx[self.M+1,:,:] = self.bx1[:,:]

        my[:,0,:]        = self.by0[:,:]
        my[:,self.N+1,:] = self.by1[:,:]

        return StaggeredField( self.M, self.N, self.P,
                               mx, my, f )

    def massDefault(self):
        return ( self.M * ( self.bx0.sum() - self.bx1.sum() ) +
                 self.N * ( self.by0.sum() - self.by1.sum() ) )

    def scalingMassDefault(self):
        return ( self.M * ( abs(self.bx0.sum()) + abs(self.bx1.sum()) ) +
                 self.N * ( abs(self.by0.sum()) + abs(self.by1.sum()) ) )        

    def LInftyNorm(self):
        return np.max( [ abs(self.bx0).max() , abs(self.bx1).max() ,
                         abs(self.by0).max() , abs(self.by1).max() ] )

    def __add__(self, other):
        if isinstance(other,SpatialBoundaries):
            return SpatialBoundaries( self.M , self.N , self.P ,
                                      self.bx0 + other.bx0 , self.bx1 + other.bx1 , self.by0 + other.by0 , self.by1 + other.by1 )
        else:
            return SpatialBoundaries( self.M , self.N , self.P ,
                                      self.bx0 + other , self.bx1 + other , self.by0 + other , self.by1 + other )

    def __sub__(self, other):
        if isinstance(other,SpatialBoundaries):
            return SpatialBoundaries( self.M , self.N , self.P ,
                                      self.bx0 - other.bx0 , self.bx1 - other.bx1 , self.by0 - other.by0 , self.by1 - other.by1 )
        else:
            return SpatialBoundaries( self.M , self.N , self.P ,
                                      self.bx0 - other , self.bx1 - other , self.by0 - other , self.by1 - other )

    def __mul__(self, other):
        if isinstance(other,SpatialBoundaries):
            return SpatialBoundaries( self.M , self.N , self.P ,
                                      self.bx0 * other.bx0 , self.bx1 * other.bx1 , self.by0 * other.by0 , self.by1 * other.by1 )
        else:
            return SpatialBoundaries( self.M , self.N , self.P ,
                                      self.bx0 * other , self.bx1 * other , self.by0 * other , self.by1 * other )

    def __div__(self, other):
        if isinstance(other,SpatialBoundaries):
            return SpatialBoundaries( self.M , self.N , self.P ,
                                      self.bx0 / other.bx0 , self.bx1 / other.bx1 , self.by0 / other.by0 , self.by1 / other.by1 )
        else:
            return SpatialBoundaries( self.M , self.N , self.P ,
                                      self.bx0 / other , self.bx1 / other , self.by0 / other , self.by1 / other )

    def __radd__(self, other):
        return SpatialBoundaries( self.M , self.N , self.P ,
                                  other + self.bx0 , other + self.bx1 , other + self.by0 , other + self.by1 )

    def __rsub__(self, other):
        return SpatialBoundaries( self.M , self.N , self.P ,
                                  other - self.bx0 , other - self.bx1 , other - self.by0 , other - self.by1 )

    def __rmul__(self, other):
        return SpatialBoundaries( self.M , self.N , self.P ,
                                  other * self.bx0 , other * self.bx1 , other * self.by0 , other * self.by1 )

    def __rdiv__(self, other):
        return SpatialBoundaries( self.M , self.N , self.P ,
                                  other / self.bx0 , other / self.bx1 , other / self.by0 , other / self.by1 )

    def __iadd__(self, other):
        if isinstance(other,SpatialBoundaries):
            self.bx0 += other.bx0
            self.bx1 += other.bx1
            self.by0 += other.by0
            self.by1 += other.by1
            return self
        else:
            self.bx0 += other
            self.bx1 += other
            self.by0 += other
            self.by1 += other
            return self

    def __isub__(self, other):
        if isinstance(other,SpatialBoundaries):
            self.bx0 -= other.bx0
            self.bx1 -= other.bx1
            self.by0 -= other.by0
            self.by1 -= other.by1
            return self
        else:
            self.bx0 -= other
            self.bx1 -= other
            self.by0 -= other
            self.by1 -= other
            return self

    def __imul__(self, other):
        if isinstance(other,SpatialBoundaries):
            self.bx0 *= other.bx0
            self.bx1 *= other.bx1
            self.by0 *= other.by0
            self.by1 *= other.by1
            return self
        else:
            self.bx0 *= other
            self.bx1 *= other
            self.by0 *= other
            self.by1 *= other
            return self

    def __idiv__(self, other):
        if isinstance(other,SpatialBoundaries):
            self.bx0 /= other.bx0
            self.bx1 /= other.bx1
            self.by0 /= other.by0
            self.by1 /= other.by1
            return self
        else:
            self.bx0 /= other
            self.bx1 /= other
            self.by0 /= other
            self.by1 /= other
            return self

    def __neg__(self):
        return SpatialBoundaries( self.M , self.N , self.P ,
                                  - self.bx0 , - self.bx1 , - self.by0 , - self.by1 )

    def __pos__(self):
        return SpatialBoundaries( self.M , self.N , self.P ,
                                  + self.bx0 , + self.bx1 , + self.by0 , + self.by1 )

    def __abs__(self):
        return SpatialBoundaries( self.M , self.N , self.P ,
                                  abs ( self.bx0 ) , abs ( self.bx1 ) , abs ( self.by0 ) , abs ( self.by1 ) )
    def copy(self):
        return SpatialBoundaries( self.M , self.N , self.P ,
                                  self.bx0.copy() , self.bx1.copy() , self.by0.copy() , self.by1.copy() )

#__________________________________________________

class Boundaries( OTObject ):
    '''
    class to store the boundaries of a field
    '''

    def __init__( self ,
                  M , N , P ,
                  temporalBoundaries=None , spatialBoundaries=None ):
        OTObject.__init__( self ,
                           M , N , P )
        if temporalBoundaries is None:
            self.temporalBoundaries = TemporalBoundaries( M , N , P )
        else:
            self.temporalBoundaries = temporalBoundaries
        if spatialBoundaries is None:
            self.spatialBoundaries = SpatialBoundaries( M , N , P )
        else:
            self.spatialBoundaries = spatialBoundaries


    def __repr__(self):
        return 'Object representing the boundaries of a field'

    def Tboundaries(self):
        gridT = self.temporalBoundaries.TtemporalBoundaries()
        gridS = self.spatialBoundaries.TspatialBoundaries()
        return ( gridT + gridS )

    def TreservoirBoundaries(self):
        gridT = self.temporalBoundaries.TtemporalReservoirBoundaries()
        gridS = self.spatialBoundaries.TspatialBoundaries()
        return ( gridT + gridS )

    def random( M , N , P ):
        return Boundaries( M , N , P ,
                           TemporalBoundaries.random(M,N,P) , SpatialBoundaries.random(M,N,P) )
    random = staticmethod(random)

    def massDefault(self):
        return ( self.temporalBoundaries.massDefault() + self.spatialBoundaries.massDefault() )

    def scalingMassDefault(self):
        return ( self.temporalBoundaries.scalingMassDefault() + self.spatialBoundaries.scalingMassDefault() )

    def relativeMassDefault(self):
        scaling = self.scalingMassDefault()
        if scaling == 0.0:
            return 0.0
        else:
            return self.massDefault() / scaling

    def LInftyNorm(self):
        return np.max( [ self.temporalBoundaries.LInftyNorm() , self.spatialBoundaries.LInftyNorm() ] )

    def placeReservoir(self, config=None):
        self.spatialBoundaries = SpatialBoundaries(self.M,self.N,self.P)

        self.temporalBoundaries.bt0[0,:]      = 0.
        self.temporalBoundaries.bt0[self.M,:] = 0.

        self.temporalBoundaries.bt1[0,:]      = 0.
        self.temporalBoundaries.bt1[self.M,:] = 0.

        self.temporalBoundaries.bt0[:,0]      = 0.
        self.temporalBoundaries.bt0[:,self.N] = 0.

        self.temporalBoundaries.bt1[:,0]      = 0.
        self.temporalBoundaries.bt1[:,self.N] = 0.

        if self.massDefault() < 0:
            self.temporalBoundaries.swap()
            if not config is None:
                config.swappedInitFinal = True

    def normalize(self, normType):
        mInit = ( self.P * self.temporalBoundaries.bt0.sum() +
                  self.M * ( self.spatialBoundaries.bx0.sum() - self.spatialBoundaries.bx1.sum() ) +
                  self.N * ( self.spatialBoundaries.by0.sum() - self.spatialBoundaries.by1.sum() ) )

        mFinal = self.P * self.temporalBoundaries.bt1.sum()

        if normType == 0:
            # correct mass default by rescaling f1
            self.temporalBoundaries.bt1 *= ( mInit / mFinal )

        elif normType == 1:
            # correct mass default by rescaling f0 --> only compatible with zero boundary conditions !
            self.temporalBoundaries.bt0 *= ( mFinal / mInit )

        elif normType == 2:
            # mass exits on the boundaries
            self.spatialBoundaries.bx0 += 0.25 * ( mFinal - mInit ) / ( self.M * ( self.N + 1 ) * ( self.P + 1 ) )
            self.spatialBoundaries.bx1 -= 0.25 * ( mFinal - mInit ) / ( self.M * ( self.N + 1 ) * ( self.P + 1 ) )

            self.spatialBoundaries.by0 += 0.25 * ( mFinal - mInit ) / ( self.N * ( self.M + 1 ) * ( self.P + 1 ) )
            self.spatialBoundaries.by1 -= 0.25 * ( mFinal - mInit ) / ( self.N * ( self.M + 1 ) * ( self.P + 1 ) )

    def __add__(self, other):
        if isinstance(other,Boundaries):
            return Boundaries( self.M , self.N , self.P ,
                               self.temporalBoundaries + other.temporalBoundaries , self.spatialBoundaries + other.spatialBoundaries )
        else:
            return Boundaries( self.M , self.N , self.P ,
                               self.temporalBoundaries + other , self.spatialBoundaries + other )

    def __sub__(self, other):
        if isinstance(other,Boundaries):
            return Boundaries( self.M , self.N , self.P ,
                               self.temporalBoundaries - other.temporalBoundaries , self.spatialBoundaries - other.spatialBoundaries )
        else:
            return Boundaries( self.M , self.N , self.P ,
                               self.temporalBoundaries - other , self.spatialBoundaries - other )

    def __mul__(self, other):
        if isinstance(other,Boundaries):
            return Boundaries( self.M , self.N , self.P ,
                               self.temporalBoundaries * other.temporalBoundaries , self.spatialBoundaries * other.spatialBoundaries )
        else:
            return Boundaries( self.M , self.N , self.P ,
                               self.temporalBoundaries * other , self.spatialBoundaries * other )

    def __div__(self, other):
        if isinstance(other,Boundaries):
            return Boundaries( self.M , self.N , self.P ,
                               self.temporalBoundaries / other.temporalBoundaries , self.spatialBoundaries / other.spatialBoundaries )
        else:
            return Boundaries( self.M , self.N , self.P ,
                               self.temporalBoundaries / other , self.spatialBoundaries / other )

    def __radd__(self, other):
        return Boundaries( self.M , self.N , self.P ,
                           other + self.temporalBoundaries , other + self.spatialBoundaries )

    def __rsub__(self, other):
        return Boundaries( self.M , self.N , self.P ,
                           other - self.temporalBoundaries , other - self.spatialBoundaries )

    def __rmul__(self, other):
        return Boundaries( self.M , self.N , self.P ,
                           other * self.temporalBoundaries , other * self.spatialBoundaries )

    def __rdiv__(self, other):
        return Boundaries( self.M , self.N , self.P ,
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
        return Boundaries( self.M , self.N , self.P ,
                           - self.temporalBoundaries , - self.spatialBoundaries )

    def __pos__(self):
        return Boundaries( self.M , self.N , self.P ,
                           + self.temporalBoundaries , + self.spatialBoundaries )

    def __abs__(self):
        return Boundaries( self.M , self.N , self.P ,
                           abs ( self.temporalBoundaries ) , abs ( self.spatialBoundaries ) )
    def copy(self):
        return Boundaries( self.M , self.N , self.P ,
                           self.temporalBoundaries.copy() , self.spatialBoundaries.copy() )

#__________________________________________________

class DivergenceBoundaries( OTObject ):
    '''
    class to store the divergence and boundary conditions of a field
    '''

    def __init__( self ,
                  M , N , P ,
                  divergence=None , boundaries=None ):
        OTObject.__init__( self ,
                           M , N , P )

        if divergence is None:
            self.divergence = Divergence( M , N , P )
        else:
            self.divergence = divergence
        if boundaries is None:
            self.boundaries = Boundaries( M , N , P )
        else:
            self.boundaries = boundaries

    def __repr__(self):
        return 'Object representing the divergence and boundary conditions of a field'

    def TdivergenceBoundaries(self):
        gridDiv = self.divergence.Tdivergence()
        gridB   = self.boundaries.Tboundaries()
        return ( gridDiv + gridB )

    def applyGaussForward(self):
        self.divergence.div[0,:,:]      += self.M*self.boundaries.spatialBoundaries.bx0[:,:]
        self.divergence.div[self.M,:,:] -= self.M*self.boundaries.spatialBoundaries.bx1[:,:]
        self.divergence.div[:,0,:]      += self.N*self.boundaries.spatialBoundaries.by0[:,:]
        self.divergence.div[:,self.N,:] -= self.N*self.boundaries.spatialBoundaries.by1[:,:]
        self.divergence.div[:,:,0]      += self.P*self.boundaries.temporalBoundaries.bt0[:,:]
        self.divergence.div[:,:,self.P] -= self.P*self.boundaries.temporalBoundaries.bt1[:,:]

    def applyGaussBackward(self):
        self.boundaries.spatialBoundaries.bx0  += self.M*self.divergence.div[0,:,:]
        self.boundaries.spatialBoundaries.bx1  -= self.M*self.divergence.div[self.M,:,:]
        self.boundaries.spatialBoundaries.by0  += self.N*self.divergence.div[:,0,:]
        self.boundaries.spatialBoundaries.by1  -= self.N*self.divergence.div[:,self.N,:]
        self.boundaries.temporalBoundaries.bt0 += self.P*self.divergence.div[:,:,0]
        self.boundaries.temporalBoundaries.bt1 -= self.P*self.divergence.div[:,:,self.P]

    def massDefault(self):
        return ( self.divergence.sum() +
                 self.boundaries.massDefault() )

    def relativeMassDefault(self):
        scaling = abs(self.divergence.sum()) + self.boundaries.scalingMassDefault()
        if scaling == 0.0 :
            return 0.0
        else:
            return self.massDefault() / scaling

    def correctMassDefault(self, EPS):
        deltaM = self.relativeMassDefault()

        if abs(deltaM) > EPS:
            nbrPts = ( (self.M+1.)*(self.N+1.)*(self.P+1.) +
                       2.*(self.N+1.)*(self.P+1.) +
                       2.*(self.M+1.)*(self.P+1.) +
                       2.*(self.M+1.)*(self.N+1.) )

            self.divergence -= deltaM / nbrPts
            self.boundaries.spatialBoundaries.bx0  -= deltaM / ( self.M * nbrPts )
            self.boundaries.spatialBoundaries.bx1  += deltaM / ( self.M * nbrPts )
            self.boundaries.spatialBoundaries.by0  -= deltaM / ( self.N * nbrPts )
            self.boundaries.spatialBoundaries.by1  += deltaM / ( self.N * nbrPts )
            self.boundaries.temporalBoundaries.bt0 -= deltaM / ( self.P * nbrPts )
            self.boundaries.temporalBoundaries.bt1 += deltaM / ( self.P * nbrPts )

            deltaM = self.relativeMassDefault()
        return deltaM

    def random( M , N , P ):
        return DivergenceBoundaries( M , N , P ,
                                     Divergence.random(M,N,P) , Boundaries.random(M,N,P) )
    random = staticmethod(random)

    def ones( M , N , P ):
        div =  np.ones(shape=(M+1,N+1,P+1))
        bx0 =  M*np.ones(shape=(N+1,P+1))
        bx1 = -M*np.ones(shape=(N+1,P+1))
        by0 =  N*np.ones(shape=(M+1,P+1))
        by1 = -N*np.ones(shape=(M+1,P+1))
        bt0 =  P*np.ones(shape=(M+1,N+1))
        bt1 = -P*np.ones(shape=(M+1,N+1))
        return DivergenceBoundaries( M , N , P ,
                                     Divergence( M , N , P ,
                                                 div ) ,
                                     Boundaries( M , N , P ,
                                                 TemporalBoundaries( M , N , P ,
                                                                     bt0 , bt1 ) ,
                                                 SpatialBoundaries( M , N , P ,
                                                                    bx0 , bx1 , by0 , by1 ) ) )
    ones = staticmethod(ones)

    def LInftyNorm(self):
        return np.max( [ self.divergence.LInftyNorm() , self.boundaries.LInftyNorm() ] )

    def __add__(self, other):
        if isinstance(other,DivergenceBoundaries):
            return DivergenceBoundaries( self.M , self.N , self.P ,
                                         self.divergence + other.divergence , self.boundaries + other.boundaries )
        else:
            return DivergenceBoundaries( self.M , self.N , self.P ,
                                         self.divergence + other , self.boundaries + other )

    def __sub__(self, other):
        if isinstance(other,DivergenceBoundaries):
            return DivergenceBoundaries( self.M , self.N , self.P ,
                                         self.divergence - other.divergence , self.boundaries - other.boundaries )
        else:
            return DivergenceBoundaries( self.M , self.N , self.P ,
                                         self.divergence - other , self.boundaries - other )

    def __mul__(self, other):
        if isinstance(other,DivergenceBoundaries):
            return DivergenceBoundaries( self.M , self.N , self.P ,
                                         self.divergence * other.divergence , self.boundaries * other.boundaries )
        else:
            return DivergenceBoundaries( self.M , self.N , self.P ,
                                         self.divergence * other , self.boundaries * other )

    def __div__(self, other):
        if isinstance(other,DivergenceBoundaries):
            return DivergenceBoundaries( self.M , self.N , self.P ,
                                         self.divergence / other.divergence , self.boundaries / other.boundaries )
        else:
            return DivergenceBoundaries( self.M , self.N , self.P ,
                                         self.divergence / other , self.boundaries / other )

    def __radd__(self, other):
        return DivergenceBoundaries( self.M , self.N , self.P ,
                                     other + self.divergence , other + self.boundaries )

    def __rsub__(self, other):
        return DivergenceBoundaries( self.M , self.N , self.P ,
                                     other - self.divergence , other - self.boundaries )

    def __rmul__(self, other):
        return DivergenceBoundaries( self.M , self.N , self.P ,
                                     other * self.divergence , other * self.boundaries )

    def __rdiv__(self, other):
        return DivergenceBoundaries( self.M , self.N , self.P ,
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
        return DivergenceBoundaries( self.M , self.N , self.P ,
                                     - self.divergence , - self.boundaries )

    def __pos__(self):
        return DivergenceBoundaries( self.M , self.N , self.P ,
                                     + self.divergence , + self.boundaries )

    def __abs__(self):
        return DivergenceBoundaries( self.M , self.N , self.P ,
                                     abs ( self.divergence ) , abs ( self.boundaries ) )
    def copy(self):
        return DivergenceBoundaries( self.M , self.N , self.P ,
                                     self.divergence.copy() , self.boundaries.copy() )

#__________________________________________________

class DivergenceTemporalBoundaries( OTObject ):
    '''
    class to store the divergence and temporal boundary conditions of a field
    '''

    def __init__( self ,
                  M , N , P ,
                  divergence=None , temporalBoundaries=None ):
        OTObject.__init__( self ,
                           M , N , P )
        if divergence is None:
            self.divergence = Divergence( M , N , P )
        else:
            self.divergence = divergence
        if temporalBoundaries is None:
            self.temporalBoundaries = TemporalBoundaries( M , N , P )
        else:
            self.temporalBoundaries = temporalBoundaries

    def __repr__(self):
        return 'Object representing the divergence and temporal boundary conditions of a field'

    def TdivergenceTemporalBoundaries(self):
        gridDiv = self.divergence.Tdivergence()
        gridB   = self.temporalBoundaries.TtemporalBoundaries()
        return ( gridDiv + gridB )

    def applyGaussForward(self):
        self.divergence.div[:,:,0]      += self.P*self.temporalBoundaries.bt0[:,:]
        self.divergence.div[:,:,self.P] -= self.P*self.temporalBoundaries.bt1[:,:]

    def applyGaussBackward(self):
        self.temporalBoundaries.bt0 += self.P*self.divergence.div[:,:,0]
        self.temporalBoundaries.bt1 -= self.P*self.divergence.div[:,:,self.P]

    def random( M , N , P ):
        return DivergenceTemporalBoundaries( M , N , P ,
                                             Divergence.random(M,N,P) , TemporalBoundaries.random(M,N,P) )
    random = staticmethod(random)

    def LInftyNorm(self):
        return np.max( [ self.divergence.LInftyNorm() , self.temporalBoundaries.LInftyNorm() ] )

    def __add__(self, other):
        if isinstance(other,DivergenceTemporalBoundaries):
            return DivergenceTemporalBoundaries( self.M , self.N , self.P ,
                                                 self.divergence + other.divergence , self.temporalBoundaries + other.temporalBoundaries )
        else:
            return DivergenceTemporalBoundaries( self.M , self.N , self.P ,
                                                 self.divergence + other , self.temporalBoundaries + other )

    def __sub__(self, other):
        if isinstance(other,DivergenceTemporalBoundaries):
            return DivergenceTemporalBoundaries( self.M , self.N , self.P ,
                                                 self.divergence - other.divergence , self.temporalBoundaries - other.temporalBoundaries )
        else:
            return DivergenceTemporalBoundaries( self.M , self.N , self.P ,
                                                 self.divergence - other , self.temporalBoundaries - other )

    def __mul__(self, other):
        if isinstance(other,DivergenceTemporalBoundaries):
            return DivergenceTemporalBoundaries( self.M , self.N , self.P ,
                                                 self.divergence * other.divergence , self.temporalBoundaries * other.temporalBoundaries )
        else:
            return DivergenceTemporalBoundaries( self.M , self.N , self.P ,
                                                 self.divergence * other , self.temporalBoundaries * other )

    def __div__(self, other):
        if isinstance(other,DivergenceTemporalBoundaries):
            return DivergenceTemporalBoundaries( self.M , self.N , self.P ,
                                                 self.divergence / other.divergence , self.temporalBoundaries / other.temporalBoundaries )
        else:
            return DivergenceTemporalBoundaries( self.M , self.N , self.P ,
                                                 self.divergence / other , self.temporalBoundaries / other )

    def __radd__(self, other):
        return DivergenceTemporalBoundaries( self.M , self.N , self.P ,
                                             other + self.divergence , other + self.temporalBoundaries )

    def __rsub__(self, other):
        return DivergenceTemporalBoundaries( self.M , self.N , self.P ,
                                             other - self.divergence , other - self.temporalBoundaries )

    def __rmul__(self, other):
        return DivergenceTemporalBoundaries( self.M , self.N , self.P ,
                                             other * self.divergence , other * self.temporalBoundaries )

    def __rdiv__(self, other):
        return DivergenceTemporalBoundaries( self.M , self.N , self.P ,
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
        return DivergenceTemporalBoundaries( self.M , self.N , self.P ,
                                             - self.divergence , - self.temporalBoundaries )

    def __pos__(self):
        return DivergenceTemporalBoundaries( self.M , self.N , self.P ,
                                             + self.divergence , + self.temporalBoundaries )

    def __abs__(self):
        return DivergenceTemporalBoundaries( self.M , self.N , self.P ,
                                             abs ( self.divergence ) , abs ( self.temporalBoundaries ) )
    def copy(self):
        return DivergenceTemporalBoundaries( self.M , self.N , self.P ,
                                             self.divergence.copy() , self.temporalBoundaries.copy() )

#__________________________________________________

class StaggeredCenteredField( OTObject ):
    '''
    class to store a staggered and a centered field
    '''

    def __init__( self ,
                  M , N , P ,
                  staggeredField=None , centeredField=None ):
        OTObject.__init__( self ,
                           M , N , P )
        if staggeredField is None:
            self.staggeredField = StaggeredField( M , N , P )
        else:
            self.staggeredField = staggeredField
            
        if centeredField is None:
            self.centeredField = CenteredField( M , N , P )
        else:
            self.centeredField = centeredField

    def __repr__(self):
        return 'Object representing a staggered and a centered field'

    def interpolationError(self):
        return ( self.centeredField - self.staggeredField.interpolation() )

    def interpolationErrorBoundaries(self):
        centeredField = self.centeredField - self.staggeredField.interpolation()
        boundaries    = self.staggeredField.boundaries()
        return CenteredFieldBoundaries(self.M, self.N, self.P,
                                       centeredField, boundaries)

    def interpolationErrorReservoirBoundaries(self):
        centeredField = self.centeredField - self.staggeredField.interpolation()
        boundaries    = self.staggeredField.reservoirBoundaries()
        return CenteredFieldBoundaries(self.M, self.N, self.P,
                                       centeredField, boundaries)

    def interpolationErrorTemporalBoundaries(self):
        centeredField      = self.centeredField - self.staggeredField.interpolation()
        temporalBoundaries = self.staggeredField.temporalBoundaries()
        return CenteredFieldTemporalBoundaries(self.M, self.N, self.P,
                                               centeredField, temporalBoundaries)

    def random( M , N , P ):
        return StaggeredCenteredField( M , N , P ,
                                       StaggeredField.random(M,N,P) , CenteredField.random(M,N,P) )
    random = staticmethod(random)

    def LInftyNorm(self):
        return np.max( [ self.staggeredField.LInftyNorm() , self.centeredField.LInftyNorm() ] )

    def __add__(self, other):
        if isinstance(other,StaggeredCenteredField):
            return StaggeredCenteredField( self.M , self.N , self.P ,
                                           self.staggeredField + other.staggeredField , self.centeredField + other.centeredField )
        else:
            return StaggeredCenteredField( self.M , self.N , self.P ,
                                           self.staggeredField + other , self.centeredField + other )

    def __sub__(self, other):
        if isinstance(other,StaggeredCenteredField):
            return StaggeredCenteredField( self.M , self.N , self.P ,
                                           self.staggeredField - other.staggeredField , self.centeredField - other.centeredField )
        else:
            return StaggeredCenteredField( self.M , self.N , self.P ,
                                           self.staggeredField - other , self.centeredField - other )

    def __mul__(self, other):
        if isinstance(other,StaggeredCenteredField):
            return StaggeredCenteredField( self.M , self.N , self.P ,
                                           self.staggeredField * other.staggeredField , self.centeredField * other.centeredField )
        else:
            return StaggeredCenteredField( self.M , self.N , self.P ,
                                           self.staggeredField * other , self.centeredField * other )

    def __div__(self, other):
        if isinstance(other,StaggeredCenteredField):
            return StaggeredCenteredField( self.M , self.N , self.P ,
                                           self.staggeredField / other.staggeredField , self.centeredField / other.centeredField )
        else:
            return StaggeredCenteredField( self.M , self.N , self.P ,
                                           self.staggeredField / other , self.centeredField / other )

    def __radd__(self, other):
        return StaggeredCenteredField( self.M , self.N , self.P ,
                                       other + self.staggeredField , other + self.centeredField )

    def __rsub__(self, other):
        return StaggeredCenteredField( self.M , self.N , self.P ,
                                       other - self.staggeredField , other - self.centeredField )

    def __rmul__(self, other):
        return StaggeredCenteredField( self.M , self.N , self.P ,
                                       other * self.staggeredField , other * self.centeredField )

    def __rdiv__(self, other):
        return StaggeredCenteredField( self.M , self.N , self.P ,
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
        return StaggeredCenteredField( self.M , self.N , self.P ,
                                       - self.staggeredField , - self.centeredField )

    def __pos__(self):
        return StaggeredCenteredField( self.M , self.N , self.P ,
                                       + self.staggeredField , + self.centeredField )

    def __abs__(self):
        return StaggeredCenteredField( self.M , self.N , self.P ,
                                       abs ( self.staggeredField ) , abs ( self.centeredField ) )
    def copy(self):
        return StaggeredCenteredField( self.M , self.N , self.P ,
                                       self.staggeredField.copy() , self.centeredField.copy() )

#__________________________________________________

class CenteredFieldBoundaries( OTObject ):
    '''
    class to store a centered field and boundary conditions
    '''

    def __init__( self ,
                  M , N , P ,
                  centeredField=None , boundaries=None ):
        OTObject.__init__( self ,
                           M , N , P )

        if centeredField is None:
            self.centeredField = CenteredField(M,N,P)
        else:
            self.centeredField = centeredField

        if boundaries is None:
            self.boundaries = Boundaries(M,N,P)
        else:
            self.boundaries = boundaries

    def __repr__(self):
        return 'Object representing a centered field and boundary conditions'

    def TinterpolationErrorBoundaries(self):
        scField  = self.centeredField.TinterpolationError()
        scField += StaggeredCenteredField( self.M, self.N , self.P ,
                                           self.boundaries.Tboundaries() )
        return scField

    def TinterpolationErrorReservoirBoundaries(self):
        scField  = self.centeredField.TinterpolationError()
        scField += StaggeredCenteredField( self.M, self.N , self.P ,
                                           self.boundaries.TreservoirBoundaries() )
        return scField

    def random( M , N , P ):
        return CenteredFieldBoundaries( M , N , P ,
                                        CenteredField.random(M,N,P) , Boundaries.random(M,N,P) )
    random = staticmethod(random)

    def LInftyNorm(self):
        return np.max( [ self.centeredField.LInftyNorm() , self.boundaries.LInftyNorm() ] )

    def __add__(self, other):
        if isinstance(other,CenteredFieldBoundaries):
            return CenteredFieldBoundaries( self.M , self.N , self.P ,
                                            self.centeredField + other.centeredField , self.boundaries + other.boundaries )
        else:
            return CenteredFieldBoundaries( self.M , self.N , self.P ,
                                            self.centeredField + other , self.boundaries + other )

    def __sub__(self, other):
        if isinstance(other,CenteredFieldBoundaries):
            return CenteredFieldBoundaries( self.M , self.N , self.P ,
                                            self.centeredField - other.centeredField , self.boundaries - other.boundaries )
        else:
            return CenteredFieldBoundaries( self.M , self.N , self.P ,
                                            self.centeredField - other , self.boundaries - other )

    def __mul__(self, other):
        if isinstance(other,CenteredFieldBoundaries):
            return CenteredFieldBoundaries( self.M , self.N , self.P ,
                                            self.centeredField * other.centeredField , self.boundaries * other.boundaries )
        else:
            return CenteredFieldBoundaries( self.M , self.N , self.P ,
                                            self.centeredField * other , self.boundaries * other )

    def __div__(self, other):
        if isinstance(other,CenteredFieldBoundaries):
            return CenteredFieldBoundaries( self.M , self.N , self.P ,
                                            self.centeredField / other.centeredField , self.boundaries / other.boundaries )
        else:
            return CenteredFieldBoundaries( self.M , self.N , self.P ,
                                            self.centeredField / other , self.boundaries / other )

    def __radd__(self, other):
        return CenteredFieldBoundaries( self.M , self.N , self.P ,
                                        other + self.centeredField , other + self.boundaries )

    def __rsub__(self, other):
        return CenteredFieldBoundaries( self.M , self.N , self.P ,
                                        other - self.centeredField , other - self.boundaries )

    def __rmul__(self, other):
        return CenteredFieldBoundaries( self.M , self.N , self.P ,
                                        other * self.centeredField , other * self.boundaries )

    def __rdiv__(self, other):
        return CenteredFieldBoundaries( self.M , self.N , self.P ,
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
        return CenteredFieldBoundaries( self.M , self.N , self.P ,
                                        - self.centeredField , - self.boundaries )

    def __pos__(self):
        return CenteredFieldBoundaries( self.M , self.N , self.P ,
                                        + self.centeredField , + self.boundaries )

    def __abs__(self):
        return CenteredFieldBoundaries( self.M , self.N , self.P ,
                                        abs ( self.centeredField ) , abs ( self.boundaries ) )
    def copy(self):
        return CenteredFieldBoundaries( self.M , self.N , self.P ,
                                        self.centeredField.copy() , self.boundaries.copy() )

#__________________________________________________

class CenteredFieldTemporalBoundaries( OTObject ):
    '''
    class to store a centered field and temporal boundary conditions
    '''

    def __init__( self ,
                  M , N , P ,
                  centeredField=None , temporalBoundaries=None ):
        OTObject.__init__( self ,
                           M , N , P )
        if centeredField is None:
            self.centeredField = CenteredField( M , N , P )
        else:
            self.centeredField = centeredField

        if temporalBoundaries is None:
            self.temporalBoundaries = TemporalBoundaries( M , N , P )
        else:
            self.temporalBoundaries = temporalBoundaries

    def __repr__(self):
        return 'Object representing a centered field and temporal boundary conditions'

    def TinterpolationErrorTemporalBoundaries(self):
        scField  = self.centeredField.TinterpolationError()
        scField += StaggeredCenteredField( self.M , self.N , self.P ,
                                           self.temporalBoundaries.TtemporalBoundaries() )
        return scField

    def random( M , N , P ):
        return CenteredFieldTemporalBoundaries( M , N , P ,
                                                CenteredField.random(M,N,P) , TemporalBoundaries.random(M,N,P) )
    random = staticmethod(random)

    def LInftyNorm(self):
        return np.max( [ self.centeredField.LInftyNorm() , self.temporalBoundaries.LInftyNorm() ] )

    def __add__(self, other):
        if isinstance(other,CenteredFieldTemporalBoundaries):
            return CenteredFieldTemporalBoundaries( self.M , self.N , self.P ,
                                                    self.centeredField + other.centeredField , self.temporalBoundaries + other.temporalBoundaries )
        else:
            return CenteredFieldTemporalBoundaries( self.M , self.N , self.P ,
                                                    self.centeredField + other , self.temporalBoundaries + other )

    def __sub__(self, other):
        if isinstance(other,CenteredFieldTemporalBoundaries):
            return CenteredFieldTemporalBoundaries( self.M , self.N , self.P ,
                                                    self.centeredField - other.centeredField , self.temporalBoundaries - other.temporalBoundaries )
        else:
            return CenteredFieldTemporalBoundaries( self.M , self.N , self.P ,
                                                    self.centeredField - other , self.temporalBoundaries - other )

    def __mul__(self, other):
        if isinstance(other,CenteredFieldTemporalBoundaries):
            return CenteredFieldTemporalBoundaries( self.M , self.N , self.P ,
                                                    self.centeredField * other.centeredField , self.temporalBoundaries * other.temporalBoundaries )
        else:
            return CenteredFieldTemporalBoundaries( self.M , self.N , self.P ,
                                                    self.centeredField * other , self.temporalBoundaries * other )

    def __div__(self, other):
        if isinstance(other,CenteredFieldTemporalBoundaries):
            return CenteredFieldTemporalBoundaries( self.M , self.N , self.P ,
                                                    self.centeredField / other.centeredField , self.temporalBoundaries / other.temporalBoundaries )
        else:
            return CenteredFieldTemporalBoundaries( self.M , self.N , self.P ,
                                                    self.centeredField / other , self.temporalBoundaries / other )

    def __radd__(self, other):
        return CenteredFieldTemporalBoundaries( self.M , self.N , self.P ,
                                                other + self.centeredField , other + self.temporalBoundaries )

    def __rsub__(self, other):
        return CenteredFieldTemporalBoundaries( self.M , self.N , self.P ,
                                                other - self.centeredField , other - self.temporalBoundaries )

    def __rmul__(self, other):
        return CenteredFieldTemporalBoundaries( self.M , self.N , self.P ,
                                                other * self.centeredField , other * self.temporalBoundaries )

    def __rdiv__(self, other):
        return CenteredFieldTemporalBoundaries( self.M , self.N , self.P ,
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
        return CenteredFieldTemporalBoundaries( self.M , self.N , self.P ,
                                                - self.centeredField , - self.temporalBoundaries )

    def __pos__(self):
        return CenteredFieldTemporalBoundaries( self.M , self.N , self.P ,
                                                + self.centeredField , + self.temporalBoundaries )

    def __abs__(self):
        return CenteredFieldTemporalBoundaries( self.M , self.N , self.P ,
                                                abs ( self.centeredField ) , abs ( self.temporalBoundaries ) )
    def copy(self):
        return CenteredFieldTemporalBoundaries( self.M , self.N , self.P ,
                                                self.centeredField.copy() , self.temporalBoundaries.copy() )

