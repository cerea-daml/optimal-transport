import numpy as np

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

        if mx is None or not mx.shape == (M+2,N+1,P+1):
            self.mx = np.zeros(shape=(M+2,N+1,P+1))
        else:
            self.mx = mx

        if my is None or not my.shape == (M+1,N+2,P+1):
            self.my = np.zeros(shape=(M+1,N+2,P+1))
        else:
            self.my = my

        if f is None or not f.shape == (M+1,N+1,P+2):
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
        mx[0:M+1,:,:] = mx[0:M+1,:,:] + 0.5*self.mx[1:M+2,:,:]

        my = np.zeros(shape=(M+1,N+1,P+1))
        my[:,:,:] = 0.5*self.my[:,0:N+1,:]
        my[:,0:N+1,:] = my[:,0:N+1,:] + 0.5*self.my[:,1:N+2,:]

        f = np.zeros(shape=(M+1,N+1,P+1))
        f[:,:,:] = 0.5*self.f[:,:,0:P+1]
        f[:,:,0:P+1] = f[:,:,0:P+1] + 0.5*self.f[:,:,1:P+2]

        return CenteredGrid( M, N, P,
                             mx, my, f )

    def divergence(self):
        M = self.M
        N = self.N
        P = self.P
        return ( M*( self.mx[1:M+2,:,:] - self.mx[0:M+1,:,:] ) +
                 N*( self.my[:,1:N+2,:] - self.my[:,0:N+1,:] ) +
                 P*( self.f[:,:,1:P+2]  - self.f[:,:,0:P+1]  ) )

    def T_divergence(div):
        (m,n,p) = div.shape
        M = m-1
        N = n-1
        P = p-1

        mx = np.zeros(shape=(M+2,N+1,P+1))
        mx[0:M+1,:,:] = -M*div[0:M+1,:,:]
        mx[1:M+2,:,:] = mx[1:M+2,:,:] + M*div[0:M+1,:,:]

        my = np.zeros(shape=(M+1,N+2,P+1))
        my[:,0:N+1,:] = -N*div[:,0:N+1,:]
        my[:,1:N+2,:] = my[:,1:N+2,:] + N*div[:,0:N+1,:]

        f = np.zeros(shape=(M+1,N+1,P+2))
        f[:,:,0:P+1] = -P*div[:,:,0:P+1]
        f[:,:,1:P+2] = f[:,:,1:P+2] + P*div[:,:,0:P+1]

        return StaggeredGrid( M, N, P,
                              mx, my, f )

    T_divergence = staticmethod(T_divergence)

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
            if ( other.M == self.M and
                 other.N == self.N and
                 other.P == self.P ):
                return StaggeredGrid(self.M, self.N, self.P, 
                                     self.mx + other.mx, self.my + other.my, self.f + other.f)

            else:
                raise AttributeError('Shapes are not compatible')
        else:
            return StaggeredGrid(self.M, self.N, self.P,
                                 self.mx + other, self.my + other, self.f + other)

    def __sub__(self, other):
        if isinstance(other,StaggeredGrid):
            if ( other.M == self.M and
                 other.N == self.N and
                 other.P == self.P ):
                return StaggeredGrid(self.M, self.N, self.P, 
                                     self.mx - other.mx, self.my - other.my, self.f - other.f)

            else:
                raise AttributeError('Shapes are not compatible')
        else:
            return StaggeredGrid(self.M, self.N, self.P,
                                 self.mx - other, self.my - other, self.f - other)

    def __mul__(self, other):
        if isinstance(other,StaggeredGrid):
            if ( other.M == self.M and
                 other.N == self.N and
                 other.P == self.P ):
                return StaggeredGrid(self.M, self.N, self.P, 
                                     self.mx * other.mx, self.my * other.my, self.f * other.f)

            else:
                raise AttributeError('Shapes are not compatible')
        else:
            return StaggeredGrid(self.M, self.N, self.P,
                                 self.mx * other, self.my * other, self.f * other)

    def __div__(self, other):
        if isinstance(other,StaggeredGrid):
            if ( other.M == self.M and
                 other.N == self.N and
                 other.P == self.P ):
                return StaggeredGrid(self.M, self.N, self.P, 
                                     self.mx / other.mx, self.my / other.my, self.f / other.f)

            else:
                raise AttributeError('Shapes are not compatible')
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
            if ( other.M == self.M and
                 other.N == self.N and
                 other.P == self.P ):
                self.mx += other.mx
                self.my += other.my
                self.f  += other.f
                return self
            else:
                raise AttributeError('Shapes are not compatible')
        else:
            self.mx += other
            self.my += other
            self.f  += other
            return self

    def __isub__(self, other):
        if isinstance(other,StaggeredGrid):
            if ( other.M == self.M and
                 other.N == self.N and
                 other.P == self.P ):
                self.mx -= other.mx
                self.my -= other.my
                self.f  -= other.f
                return self
            else:
                raise AttributeError('Shapes are not compatible')
        else:
            self.mx -= other
            self.my -= other
            self.f  -= other
            return self

    def __imul__(self, other):
        if isinstance(other,StaggeredGrid):
            if ( other.M == self.M and
                 other.N == self.N and
                 other.P == self.P ):
                self.mx *= other.mx
                self.my *= other.my
                self.f  *= other.f
                return self
            else:
                raise AttributeError('Shapes are not compatible')
        else:
            self.mx *= other
            self.my *= other
            self.f  *= other
            return self

    def __idiv__(self, other):
        if isinstance(other,StaggeredGrid):
            if ( other.M == self.M and
                 other.N == self.N and
                 other.P == self.P ):
                self.mx /= other.mx
                self.my /= other.my
                self.f  /= other.f
                return self
            else:
                raise AttributeError('Shapes are not compatible')
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
                             self.mx.abs(), self.my.abs(), self.f.abs())
