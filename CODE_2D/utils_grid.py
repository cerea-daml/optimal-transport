import numpy as np

####################
# Class CenteredGrid
####################

class CenteredGrid:
    '''
    Class to deals with a centered grid
    '''

#############
# Constructor
#############

    def __init__(self, M, N, P, mx=None, my=None, f=None):
        self.M = M
        self.N = N
        self.P = P

        if mx is None:
            self.mx = np.zeros(shape=(M+1,N+1,P+1))
        else:
            self.mx = mx

        if my is None:
            self.my = np.zeros(shape=(M+1,N+1,P+1))
        else:
            self.my = my

        if f is None:
            self.f = np.zeros(shape=(M+1,N+1,P+1))
        else:
            self.f = f

    def __repr__(self):
        return ( 'Centered grid with shape ' +
                 str(self.M) + ' x ' +
                 str(self.N) + ' x ' +
                 str(self.P) )
    
    def __delattr__(self, nom_attr):
        raise AttributeError('You can not delete any attribute from this class : CenteredGrid')

    def copy(self):
        return CenteredGrid( self.M, self.N, self.P,
                             self.mx.copy(), self.my.copy(), self.f.copy() )

    def LInftyNorm(self):
        return np.max( [ np.abs(self.mx).max(),
                         np.abs(self.my).max(),
                         np.abs(self.f).max() ] )

    def L2Norm(self):
        return np.sqrt( ( np.power(self.mx,2) + np.power(self.my,2) + np.power(self.f,2) ).mean() )

###############
# I/O functions
###############

    def tofile(self, fileName):
        file = open(fileName, 'w')
        np.array([self.M,self.N,self.P],dtype=float).tofile(file)
        self.mx.tofile(file)
        self.my.tofile(file)
        self.f.tofile(file)
        file.close()
        return 0

    def fromfile(fileName):
        data = np.fromfile(fileName)
        M = int(data[0])
        N = int(data[1])
        P = int(data[2])
        mx = data[3:
                      3+(M+1)*(N+1)*(P+1)].reshape((M+1,N+1,P+1))
        my = data[3+(M+1)*(N+1)*(P+1):
                      3+2*(M+1)*(N+1)*(P+1)].reshape((M+1,N+1,P+1))
        f  = data[3+2*(M+1)*(N+1)*(P+1):
                      3+3*(M+1)*(N+1)*(P+1)].reshape((M+1,N+1,P+1))
        return CenteredGrid( M, N, P,
                             mx, my, f )

    fromfile = staticmethod(fromfile)

########################################
# Interpolation and other grid functions
########################################

    def T_interpolation(self):
        M = self.M
        N = self.N
        P = self.P
        mx = np.zeros(shape=(M+2,N+1,P+1))
        mx[0:M+1,:,:] =  0.5*self.mx[:,:,:]
        mx[1:M+2,:,:] += 0.5*self.mx[:,:,:]

        my = np.zeros(shape=(M+1,N+2,P+1))
        my[:,0:N+1,:] =  0.5*self.my[:,:,:]
        my[:,1:N+2,:] += 0.5*self.my[:,:,:]

        f = np.zeros(shape=(M+1,N+1,P+2))
        f[:,:,0:P+1] =  0.5*self.f[:,:,:]
        f[:,:,1:P+2] += 0.5*self.f[:,:,:]

        return StaggeredGrid( M, N, P,
                              mx, my, f )

###############
# To acces item
###############

    def __getitem__(self, index):
        if len(index) > 1:
            if index[0] == 0:
                return self.mx[index[1:]]
            elif index[1] == 1:
                return self.my[index[1:]]
            elif index[1] == 2:
                return self.f[index[1:]]
            else:
                raise IndexError(str(index[0])+' out of range (range 3)')
        elif len(index) == 1:
            if index[0] == 0:
                return self.mx
            elif index[1] == 1:
                return self.my
            elif index[1] == 2:
                return self.f
            else:
                raise IndexError(str(index[0])+' out of range (range 3)')
        else:
            raise IndexError('No index given')
    
    def __setitem__(self, index, other):
        if len(index) > 1:
            if index[0] == 0:
                self.mx[index[1:]] = other
            elif index[1] == 1:
                self.my[index[1:]] = other
            elif index[1] == 2:
                self.f[index[1:]]  = other
            else:
                raise IndexError(str(index[0])+' out of range (range 3)')
        elif len(index) == 1:
            if index[0] == 0:
                self.mx = other
            elif index[1] == 1:
                self.my = other
            elif index[1] == 2:
                self.f  = other
            else:
                raise IndexError(str(index[0])+' out of range (range 3)')
        else:
            raise IndexError('No index given')

    def __delitem__(self, index):
        raise AttributeError('You can not delete any item from this class : CenteredGrid')

##########################
# Operations bewteen grids
##########################

    def __add__(self, other):
        if isinstance(other,CenteredGrid):
            return CenteredGrid(self.M, self.N, self.P, 
                                self.mx + other.mx, self.my + other.my, self.f + other.f)
        else:
            return CenteredGrid(self.M, self.N, self.P,
                                self.mx + other, self.my + other, self.f + other)

    def __sub__(self, other):
        if isinstance(other,CenteredGrid):
            return CenteredGrid(self.M, self.N, self.P, 
                                self.mx - other.mx, self.my - other.my, self.f - other.f)
        else:
            return CenteredGrid(self.M, self.N, self.P,
                                self.mx - other, self.my - other, self.f - other)

    def __mul__(self, other):
        if isinstance(other,CenteredGrid):
            return CenteredGrid(self.M, self.N, self.P, 
                                self.mx * other.mx, self.my * other.my, self.f * other.f)
        else:
            return CenteredGrid(self.M, self.N, self.P,
                                self.mx * other, self.my * other, self.f * other)

    def __div__(self, other):
        if isinstance(other,CenteredGrid):
            return CenteredGrid(self.M, self.N, self.P, 
                                self.mx / other.mx, self.my / other.my, self.f / other.f)
        else:
            return CenteredGrid(self.M, self.N, self.P,
                                self.mx / other, self.my / other, self.f / other)

    def __radd__(self, other):
        return CenteredGrid(self.M, self.N, self.P,
                            other + self.mx, other + self.my, other + self.f)

    def __rsub__(self, other):
        return CenteredGrid(self.M, self.N, self.P,
                            other - self.mx, other - self.my, other - self.f)

    def __rmul__(self, other):
        return CenteredGrid(self.M, self.N, self.P,
                            other * self.mx, other * self.my, other * self.f)

    def __rdiv__(self, other):
        return CenteredGrid(self.M, self.N, self.P,
                            other / self.mx, other / self.my, other / self.f)

    def __iadd__(self, other):
        if isinstance(other,CenteredGrid):
            self.mx += other.mx
            self.my += other.my
            self.f  += other.f
            return self
        else:
            self.mx += other
            self.my += other
            self.f  += other
            return self

    def __isub__(self, other):
        if isinstance(other,CenteredGrid):
            self.mx -= other.mx
            self.my -= other.my
            self.f  -= other.f
            return self
        else:
            self.mx -= other
            self.my -= other
            self.f  -= other
            return self

    def __imul__(self, other):
        if isinstance(other,CenteredGrid):
            self.mx *= other.mx
            self.my *= other.my
            self.f  *= other.f
            return self
        else:
            self.mx *= other
            self.my *= other
            self.f  *= other
            return self

    def __idiv__(self, other):
        if isinstance(other,CenteredGrid):
            self.mx /= other.mx
            self.my /= other.my
            self.f  /= other.f
            return self
        else:
            self.mx /= other
            self.my /= other
            self.f  /= other
            return self

    def __neg__(self):
        return CenteredGrid(self.M, self.N, self.P,
                            - self.mx, - self.my, - self.f)

    def __pos__(self):
        return CenteredGrid(self.M, self.N, self.P,
                            + self.mx, + self.my, + self.f)

    def __abs__(self):
        return CenteredGrid(self.M, self.N, self.P,
                            np.abs(self.mx), np.abs(self.my), np.abs(self.f) )

####################
# Class CenteredGrid
####################

class StaggeredGrid:
    '''
    Class to deals with a staggered grid
    '''

#############
# Constructor
#############

    def __init__(self, M, N, P, mx=None, my=None, f=None):
        self.M = M
        self.N = N
        self.P = P

        if mx is None:
            self.mx = np.zeros(shape=(M+2,N+1,P+1))
        else:
            self.mx = mx

        if my is None:
            self.my = np.zeros(shape=(M+1,N+2,P+1))
        else:
            self.my = my

        if f is None:
            self.f = np.zeros(shape=(M+1,N+1,P+2))
        else:
            self.f = f

    def __repr__(self):
        return ( 'Staggered grid with shape ' +
                 str(self.M) + ' x ' +
                 str(self.N) + ' x ' +
                 str(self.P) )
    
    def __delattr__(self, nom_attr):
        raise AttributeError('You can not delete any attribute from this class : StaggeredGrid')

    def copy(self):
        return StaggeredGrid( self.M, self.N, self.P,
                              self.mx.copy(), self.my.copy(), self.f.copy() )

    def LInftyNorm(self):
        return np.max( [ np.abs(self.mx).max(),
                         np.abs(self.my).max(),
                         np.abs(self.f).max() ] )

    def L2Norm(self):
        return np.sqrt( ( np.power(self.mx,2) +np.power(self.my,2) + np.power(self.f,2) ).mean() )

    def random(M, N, P):
        mx = np.random.rand(M+2, N+1, P+1)
        my = np.random.rand(M+1, N+2, P+1)
        f  = np.random.rand(M+1, N+1, P+2)
        return StaggeredGrid(M, N, P, mx, my, f)
    random = staticmethod(random)

###############
# I/O functions
###############

    def tofile(self, fileName):
        file = open(fileName, 'w')
        np.array([self.M,self.N,self.P],dtype=float).tofile(file)
        self.mx.tofile(file)
        self.my.tofile(file)
        self.f.tofile(file)
        file.close()
        return 0

    def fromfile(fileName):
        data = np.fromfile(fileName)
        M = int(data[0])
        N = int(data[1])
        P = int(data[2])
        mx = data[3:
                      3+(M+2)*(N+1)*(P+1)].reshape((M+2,N+1,P+1))
        my = data[3+(M+2)*(N+1)*(P+1):
                      3+(M+2)*(N+1)*(P+1)+(M+1)*(N+2)*(P+1)].reshape((M+1,N+2,P+1))
        f  = data[3+(M+2)*(N+1)*(P+1)+(M+1)*(N+2)*(P+1):
                      3+(M+2)*(N+1)*(P+1)+(M+1)*(N+2)*(P+1)+(M+1)*(N+1)*(P+2)].reshape((M+1,N+1,P+2))
        return StaggeredGrid( M, N, P,
                              mx, my, f )

    fromfile = staticmethod(fromfile)

########################################
# Interpolation and other grid functions
########################################

    def interpolation(self):
        M = self.M
        N = self.N
        P = self.P

        mx = np.zeros(shape=(M+1,N+1,P+1))
        mx[:,:,:] = 0.5*self.mx[0:M+1,:,:]
        mx[0:M+1,:,:] += 0.5*self.mx[1:M+2,:,:]

        my = np.zeros(shape=(M+1,N+1,P+1))
        my[:,:,:] = 0.5*self.my[:,0:N+1,:]
        my[:,0:N+1,:] += 0.5*self.my[:,1:N+2,:]

        f = np.zeros(shape=(M+1,N+1,P+1))
        f[:,:,:] = 0.5*self.f[:,:,0:P+1]
        f[:,:,0:P+1] += 0.5*self.f[:,:,1:P+2]

        return CenteredGrid( M, N, P,
                             mx, my, f )

    def divergence(self):
        M = self.M
        N = self.N
        P = self.P
        div = ( M*( self.mx[1:M+2,:,:] - self.mx[0:M+1,:,:] ) +
                N*( self.my[:,1:N+2,:] - self.my[:,0:N+1,:] ) +
                P*( self.f[:,:,1:P+2]  - self.f[:,:,0:P+1]  ) )
        return Divergence(M,N,P,div)

    def bt0(self):
        return self.f[:,:,0]

    def bt1(self):
        return self.f[:,:,self.P+1]

    def bx0(self):
        return self.mx[0,:,:]

    def bx1(self):
        return self.mx[self.M+1,:,:]

    def by0(self):
        return self.my[:,0,:]

    def by1(self):
        return self.my[:,self.N+1,:]

    def divBound(self):
        M = self.M
        N = self.N
        P = self.P
        div = ( M*( self.mx[1:M+2,:,:] - self.mx[0:M+1,:,:] ) +
                N*( self.my[:,1:N+2,:] - self.my[:,0:N+1,:] ) +
                P*( self.f[:,:,1:P+2]  - self.f[:,:,0:P+1]  ) )
        return DivergenceBound(M, N, P,
                               div,
                               self.mx[0,:,:], self.mx[M+1,:,:],
                               self.my[:,0,:], self.my[:,N+1,:],
                               self.f[:,:,0],  self.f[:,:,P+1] )

###############
# To acces item
###############

    def __getitem__(self, index):
        if len(index) > 1:
            if index[0] == 0:
                return self.mx[index[1:]]
            elif index[1] == 1:
                return self.my[index[1:]]
            elif index[1] == 2:
                return self.f[index[1:]]
            else:
                raise IndexError(str(index[0])+' out of range (range 3)')
        elif len(index) == 1:
            if index[0] == 0:
                return self.mx
            elif index[1] == 1:
                return self.my
            elif index[1] == 2:
                return self.f
            else:
                raise IndexError(str(index[0])+' out of range (range 3)')
        else:
            raise IndexError('No index given')
    
    def __setitem__(self, index, other):
        if len(index) > 1:
            if index[0] == 0:
                self.mx[index[1:]] = other
            elif index[1] == 1:
                self.my[index[1:]] = other
            elif index[1] == 2:
                self.f[index[1:]]  = other
            else:
                raise IndexError(str(index[0])+' out of range (range 3)')
        elif len(index) == 1:
            if index[0] == 0:
                self.mx = other
            elif index[1] == 1:
                self.my = other
            elif index[1] == 2:
                self.f  = other
            else:
                raise IndexError(str(index[0])+' out of range (range 3)')
        else:
            raise IndexError('No index given')

    def __delitem__(self, index):
        raise AttributeError('You can not delete any item from this class : StaggeredGrid')

##########################
# Operations bewteen grids
##########################

    def __add__(self, other):
        if isinstance(other,StaggeredGrid):
            return StaggeredGrid(self.M, self.N, self.P, 
                                 self.mx + other.mx, self.my + other.my, self.f + other.f)
        else:
            return StaggeredGrid(self.M, self.N, self.P,
                                 self.mx + other, self.my + other, self.f + other)

    def __sub__(self, other):
        if isinstance(other,StaggeredGrid):
            return StaggeredGrid(self.M, self.N, self.P, 
                                 self.mx - other.mx, self.my - other.my, self.f - other.f)
        else:
            return StaggeredGrid(self.M, self.N, self.P,
                                 self.mx - other, self.my - other, self.f - other)

    def __mul__(self, other):
        if isinstance(other,StaggeredGrid):
            return StaggeredGrid(self.M, self.N, self.P, 
                                 self.mx * other.mx, self.my * other.my, self.f * other.f)
        else:
            return StaggeredGrid(self.M, self.N, self.P,
                                 self.mx * other, self.my * other, self.f * other)

    def __div__(self, other):
        if isinstance(other,StaggeredGrid):
            return StaggeredGrid(self.M, self.N, self.P, 
                                 self.mx / other.mx, self.my / other.my, self.f / other.f)
        else:
            return StaggeredGrid(self.M, self.N, self.P,
                                 self.mx / other, self.my / other, self.f / other)

    def __radd__(self, other):
        return StaggeredGrid(self.M, self.N, self.P,
                             other + self.mx, other + self.my, other + self.f)

    def __rsub__(self, other):
        return StaggeredGrid(self.M, self.N, self.P,
                             other - self.mx, other - self.my, other - self.f)

    def __rmul__(self, other):
        return StaggeredGrid(self.M, self.N, self.P,
                             other * self.mx, other * self.my, other * self.f)

    def __rdiv__(self, other):
        return StaggeredGrid(self.M, self.N, self.P,
                             other / self.mx, other / self.my, other / self.f)

    def __iadd__(self, other):
        if isinstance(other,StaggeredGrid):
            self.mx += other.mx
            self.my += other.my
            self.f  += other.f
            return self
        else:
            self.mx += other
            self.my += other
            self.f  += other
            return self

    def __isub__(self, other):
        if isinstance(other,StaggeredGrid):
            self.mx -= other.mx
            self.my -= other.my
            self.f  -= other.f
            return self
        else:
            self.mx -= other
            self.my -= other
            self.f  -= other
            return self

    def __imul__(self, other):
        if isinstance(other,StaggeredGrid):
            self.mx *= other.mx
            self.my *= other.my
            self.f  *= other.f
            return self
        else:
            self.mx *= other
            self.my *= other
            self.f  *= other
            return self

    def __idiv__(self, other):
        if isinstance(other,StaggeredGrid):
            self.mx /= other.mx
            self.my /= other.my
            self.f  /= other.f
            return self
        else:
            self.mx /= other
            self.my /= other
            self.f  /= other
            return self

    def __neg__(self):
        return StaggeredGrid(self.M, self.N, self.P,
                             - self.mx, - self.my, - self.f)

    def __pos__(self):
        return StaggeredGrid(self.M, self.N, self.P,
                             + self.mx, + self.my, + self.f)

    def __abs__(self):
        return StaggeredGrid(self.M, self.N, self.P,
                             np.abs(self.mx), np.abs(self.my), np.abs(self.f))

##################
# Class Divergence
##################

class Divergence:
    '''
    Class to deals with a divergence field defined on a centered grid
    '''

#############
# Constructor
#############

    def __init__(self, M, N, P, div=None):
        self.M = M
        self.N = N
        self.P = P

        if div is None:
            self.div = np.zeros(shape=(M+1,N+1,P+1))
        else:
            self.div = div

    def __repr__(self):
        return ( 'Divergence on a centered grid with shape ' +
                 str(self.M) + ' x ' +
                 str(self.N) + ' x ' +
                 str(self.P) )
    
    def __delattr__(self, nom_attr):
        raise AttributeError('You can not delete any attribute from this class : Divergence')

    def copy(self):
        return Divergence( self.M, self.N, self.P,
                           self.div.copy() )

    def LInftyNorm(self):
        return np.abs(self.div).max()

    def L2Norm(self):
        return np.sqrt( np.power(self.div,2).mean() )

    def random(M, N, P):
        div = np.random.rand(M+1,N+1,P+1)
        return Divergence(M, N, P, div)
    random = staticmethod(random)

############
# Divergence
############

    def T_divergence(self):
        M = self.M
        N = self.N
        P = self.P

        mx = np.zeros(shape=(M+2,N+1,P+1))
        mx[0:M+1,:,:] = -M*self.div[0:M+1,:,:]
        mx[1:M+2,:,:] += M*self.div[0:M+1,:,:]

        my = np.zeros(shape=(M+1,N+2,P+1))
        my[:,0:N+1,:] = -N*self.div[:,0:N+1,:]
        my[:,1:N+2,:] += N*self.div[:,0:N+1,:]

        f = np.zeros(shape=(M+1,N+1,P+2))
        f[:,:,0:P+1] = -P*self.div[:,:,0:P+1]
        f[:,:,1:P+2] += P*self.div[:,:,0:P+1]
        
        return StaggeredGrid( M, N, P,
                              mx, my, f )

###############
# To acces item
###############

    def __getitem__(self, index):
        return self.div[index]
    
    def __setitem__(self, index, other):
        self.div[index] = other

    def __delitem__(self, index):
        raise AttributeError('You can not delete any item from this class : Divergence')

##########################
# Operations bewteen grids
##########################

    def __add__(self, other):
        if isinstance(other,Divergence):
            return Divergence(self.M, self.N, self.P, 
                              self.div + other.div)
        else:
            return Divergence(self.M, self.N, self.P,
                              self.div + other)

    def __sub__(self, other):
        if isinstance(other,Divergence):
            return Divergence(self.M, self.N, self.P, 
                              self.div - other.div)
        else:
            return Divergence(self.M, self.N, self.P,
                              self.div - other)

    def __mul__(self, other):
        if isinstance(other,Divergence):
            return Divergence(self.M, self.N, self.P, 
                              self.div * other.div)
        else:
            return Divergence(self.M, self.N, self.P,
                              self.div * other)

    def __div__(self, other):
        if isinstance(other,Divergence):
            return Divergence(self.M, self.N, self.P, 
                              self.div / other.div)
        else:
            return Divergence(self.M, self.N, self.P,
                              self.div / other)

    def __radd__(self, other):
        return Divergence(self.M, self.N, self.P,
                          other + self.div)

    def __rsub__(self, other):
        return Divergence(self.M, self.N, self.P,
                          other - self.div)

    def __rmul__(self, other):
        return Divergence(self.M, self.N, self.P,
                          other * self.div)

    def __rdiv__(self, other):
        return Divergence(self.M, self.N, self.P,
                          other / self.div)

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
        return Divergence(self.M, self.N, self.P,
                          - self.div)

    def __pos__(self):
        return Divergence(self.M, self.N, self.P,
                          + self.div)

    def __abs__(self):
        return Divergence(self.M, self.N, self.P,
                          np.abs(self.div))

#######################
# Class DivergenceBound
#######################

class DivergenceBound:
    '''
    Class to deals with a divergence field defined on a centered grid and boundary conditions
    '''

#############
# Constructor
#############

    def __init__(self, M, N, P, div=None, 
                 bx0=None, bx1=None,
                 by0=None, by1=None,
                 bt0=None, bt1=None):
        self.M = M
        self.N = N
        self.P = P

        if div is None:
            self.div = np.zeros(shape=(M+1,N+1,P+1))
        else:
            self.div = div

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

        if bt0 is None:
            self.bt0 = np.zeros(shape=(M+1,N+1))
        else:
            self.bt0 = bt0

        if bt1 is None:
            self.bt1 = np.zeros(shape=(M+1,N+1))
        else:
            self.bt1 = bt1

    def __repr__(self):
        return ( 'Divergence and boundaries on a centered grid with shape ' +
                 str(self.M) + ' x ' +
                 str(self.N) + ' x ' +
                 str(self.P) )
    
    def __delattr__(self, nom_attr):
        raise AttributeError('You can not delete any attribute from this class : DivergenceBound')

    def copy(self):
        return DivergenceBound( self.M, self.N, self.P,
                                self.div.copy(), 
                                self.bx0.copy(), self.bx1.copy(), 
                                self.by0.copy(), self.by1.copy(),
                                self.bt0.copy(), self.bt1.copy() )

    def LInftyNorm(self):
        return np.max( [ np.abs(self.div).max(),
                         np.abs(self.bx0).max(), np.abs(self.bx1).max(),
                         np.abs(self.by0).max(), np.abs(self.by1).max(),
                         np.abs(self.bt0).max(), np.abs(self.bt1).max() ] )

    def L2Norm(self):
        return np.sqrt( ( np.power(self.div,2) +
                          np.power(self.bx0,2) + np.power(self.bx1,2) +
                          np.power(self.by0,2) + np.power(self.by1,2) +
                          np.power(self.bt0,2) + np.power(self.bt1,2) ).mean() )

####################################
# Divergence and boundary conditions
####################################

    def T_divBound(self):
        M = self.M
        N = self.N
        P = self.P

        mx = np.zeros(shape=(M+2,N+1,P+1))
        my = np.zeros(shape=(M+1,N+2,P+1))
        f  = np.zeros(shape=(M+1,N+1,P+2))

        mx[0:M+1,:,:] = -M*self.div[0:M+1,:,:]
        mx[1:M+2,:,:] += M*self.div[0:M+1,:,:]
        mx[0,:,:]     += self.bx0[:,:]
        mx[M+1,:,:]   += self.bx1[:,:]

        my[:,0:N+1,:] = -N*self.div[:,0:N+1,:]
        my[:,1:N+2,:] += N*self.div[:,0:N+1,:]
        my[:,0,:]     += self.by0[:,:]
        my[:,N+1,:]   += self.by1[:,:]

        f[:,:,0:P+1] = -P*self.div[:,:,0:P+1]
        f[:,:,1:P+2] += P*self.div[:,:,0:P+1]
        f[:,:,0]     += self.bt0[:,:]
        f[:,:,P+1]   += self.bt1[:,:]

        return StaggeredGrid( M, N, P,
                              mx, my, f)

########################################
# Gauss operations to invert A_T_A_div_b
########################################

    def applyGaussForward(self):
        self.div[0,:,:]      += self.M*self.bx0[:,:]
        self.div[self.M,:,:] -= self.M*self.bx1[:,:]
        self.div[:,0,:]      += self.N*self.by0[:,:]
        self.div[:,self.N,:] -= self.N*self.by1[:,:]
        self.div[:,:,0]      += self.P*self.bt0[:,:]
        self.div[:,:,self.P] -= self.P*self.bt1[:,:]

    def applyGaussBackward(self):
        self.bx0 += self.M*self.div[0,:,:]
        self.bx1 -= self.M*self.div[self.M,:,:]
        self.by0 += self.N*self.div[:,0,:]
        self.by1 -= self.N*self.div[:,self.N,:]
        self.bt0 += self.P*self.div[:,:,0]
        self.bt1 -= self.P*self.div[:,:,self.P]

##########################
# Operations bewteen grids
##########################

    def __add__(self, other):
        if isinstance(other,DivergenceBound):
            return DivergenceBound(self.M, self.N, self.P, 
                                   self.div + other.div,
                                   self.bx0 + other.bx0, self.bx1 + other.bx1,
                                   self.by0 + other.by0, self.by1 + other.by1,
                                   self.bt0 + other.bt0, self.bt1 + other.bt1 )
        else:
            return DivergenceBound(self.M, self.N, self.P,
                                   self.div + other,
                                   self.bx0 + other, self.bx1 + other,
                                   self.by0 + other, self.by1 + other,
                                   self.bt0 + other, self.bt1 + other )

    def __sub__(self, other):
        if isinstance(other,DivergenceBound):
            return DivergenceBound(self.M, self.N, self.P, 
                                   self.div - other.div,
                                   self.bx0 - other.bx0, self.bx1 - other.bx1,
                                   self.by0 - other.by0, self.by1 - other.by1,
                                   self.bt0 - other.bt0, self.bt1 - other.bt1 )
        else:
            return DivergenceBound(self.M, self.N, self.P,
                                   self.div - other,
                                   self.bx0 - other, self.bx1 - other,
                                   self.by0 - other, self.by1 - other,
                                   self.bt0 - other, self.bt1 - other )

    def __mul__(self, other):
        if isinstance(other,DivergenceBound):
            return DivergenceBound(self.M, self.N, self.P, 
                                   self.div * other.div,
                                   self.bx0 * other.bx0, self.bx1 * other.bx1,
                                   self.by0 * other.by0, self.by1 * other.by1,
                                   self.bt0 * other.bt0, self.bt1 * other.bt1 )
        else:
            return DivergenceBound(self.M, self.N, self.P,
                                   self.div * other,
                                   self.bx0 * other, self.bx1 * other,
                                   self.by0 * other, self.by1 * other,
                                   self.bt0 * other, self.bt1 * other )

    def __div__(self, other):
        if isinstance(other,DivergenceBound):
            return DivergenceBound(self.M, self.N, self.P, 
                                   self.div / other.div,
                                   self.bx0 / other.bx0, self.bx1 / other.bx1,
                                   self.by0 / other.by0, self.by1 / other.by1,
                                   self.bt0 / other.bt0, self.bt1 / other.bt1 )
        else:
            return DivergenceBound(self.M, self.N, self.P,
                                   self.div / other,
                                   self.bx0 / other, self.bx1 / other,
                                   self.by0 / other, self.by1 / other,
                                   self.bt0 / other, self.bt1 / other )

    def __radd__(self, other):
        return DivergenceBound(self.M, self.N, self.P,
                               other + self.div,
                               other + self.bx0, other + self.bx1,
                               other + self.by0, other + self.by1,
                               other + self.bt0, other + self.bt1 )

    def __rsub__(self, other):
        return DivergenceBound(self.M, self.N, self.P,
                               other - self.div,
                               other - self.bx0, other - self.bx1,
                               other - self.by0, other - self.by1,
                               other - self.bt0, other - self.bt1 )

    def __rmul__(self, other):
        return DivergenceBound(self.M, self.N, self.P,
                               other * self.div,
                               other * self.bx0, other * self.bx1,
                               other * self.by0, other * self.by1,
                               other * self.bt0, other * self.bt1 )

    def __rdiv__(self, other):
        return DivergenceBound(self.M, self.N, self.P,
                               other / self.div,
                               other / self.bx0, other / self.bx1,
                               other / self.by0, other / self.by1,
                               other / self.bt0, other / self.bt1 )

    def __iadd__(self, other):
        if isinstance(other,DivergenceBound):
            self.div += other.div
            self.bx0 += other.bx0
            self.bx1 += other.bx1
            self.by0 += other.by0
            self.by1 += other.by1
            self.bt0 += other.bt0
            self.bt1 += other.bt1
            return self
        else:
            self.div += other
            self.bx0 += other
            self.bx1 += other
            self.by0 += other
            self.by1 += other
            self.bt0 += other
            self.bt1 += other
            return self

    def __isub__(self, other):
        if isinstance(other,DivergenceBound):
            self.div -= other.div
            self.bx0 -= other.bx0
            self.bx1 -= other.bx1
            self.by0 -= other.by0
            self.by1 -= other.by1
            self.bt0 -= other.bt0
            self.bt1 -= other.bt1
            return self
        else:
            self.div -= other
            self.bx0 -= other
            self.bx1 -= other
            self.by0 -= other
            self.by1 -= other
            self.bt0 -= other
            self.bt1 -= other
            return self

    def __imul__(self, other):
        if isinstance(other,DivergenceBound):
            self.div *= other.div
            self.bx0 *= other.bx0
            self.bx1 *= other.bx1
            self.by0 *= other.by0
            self.by1 *= other.by1
            self.bt0 *= other.bt0
            self.bt1 *= other.bt1
            return self
        else:
            self.div *= other
            self.bx0 *= other
            self.bx1 *= other
            self.by0 *= other
            self.by1 *= other
            self.bt0 *= other
            self.bt1 *= other
            return self

    def __idiv__(self, other):
        if isinstance(other,DivergenceBound):
            self.div /= other.div
            self.bx0 /= other.bx0
            self.bx1 /= other.bx1
            self.by0 /= other.by0
            self.by1 /= other.by1
            self.bt0 /= other.bt0
            self.bt1 /= other.bt1
            return self
        else:
            self.div /= other
            self.bx0 /= other
            self.bx1 /= other
            self.by0 /= other
            self.by1 /= other
            self.bt0 /= other
            self.bt1 /= other
            return self

    def __neg__(self):
        return DivergenceBound(self.M, self.N, self.P,
                               - self.div,
                               - self.bx0, - self.bx1,
                               - self.by0, - self.by1,
                               - self.bt0, - self.bt1)

    def __pos__(self):
        return DivergenceBound(self.M, self.N, self.P,
                               + self.div,
                               + self.bx0, + self.bx1,
                               + self.by0, + self.by1,
                               + self.bt0, + self.bt1)

    def __abs__(self):
        return DivergenceBound(self.M, self.N, self.P,
                               np.abs(self.div),
                               np.abs(self.bx0), np.abs(self.bx1),
                               np.abs(self.by0), np.abs(self.by1),
                               np.abs(self.bt0), np.abs(self.bt1) )
