import numpy as np

from utils_grid import *

class AdrState:
    '''
    Class to deals with a state for the ADR algorithm
    '''

#############
# Constructor
#############

    def __init__(self, M, N, P, z, w):
        self.M = M
        self.N = N
        self.P = P
        self.z = z
        self.w = w

    def __repr__(self):
        return ( 'Adr state with shape ' +
                 str(self.M) + ' x ' +
                 str(self.N) + ' x ' +
                 str(self.P) )
    
    def __delattr__(self, nom_attr):
        raise AttributeError('You can not delete any attribute from this class : AdrState')

    def copy(self):
        return CenteredGrid( self.M, self.N, self.P,
                             self.z.copy(), self.w.copy() )

    def LInftyNorm(self):
        return np.max( [ self.z.LInftyNorm(),
                         self.w.LInftyNorm() ] )

    def L2Norm(self):
        return np.sqrt( ( np.power(self.z.stagGrid.mx,2) +
                          np.power(self.z.stagGrid.my,2) +
                          np.power(self.z.stagGrid.f,2)  +

                          np.power(self.z.centGrid.mx,2) +
                          np.power(self.z.centGrid.my,2) +
                          np.power(self.z.centGrid.f,2)  +

                          np.power(self.w.stagGrid.mx,2) +
                          np.power(self.w.stagGrid.my,2) +
                          np.power(self.w.stagGrid.f,2)  +

                          np.power(self.w.centGrid.mx,2) +
                          np.power(self.w.centGrid.my,2) +
                          np.power(self.w.centGrid.f,2)  ).mean() )

    def random(M, N, P):
        z = StaggeredCenteredGrid.random()
        w = StaggeredCenteredGrid.random()
        return CenteredGrid(M, N, P, z, w)
    random = staticmethod(random)

###############
# I/O functions A AJUSTER DES QUE POSSIBLE
###############
'''
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
'''

##########################
# Operations bewteen grids
##########################

    def __add__(self, other):
        if isinstance(other,AdrState):
            return AdrState(self.M, self.N, self.P,
                            self.z + other.z,
                            self.w + other.w)
        else:
            return AdrState(self.M, self.N, self.P,
                            self.z + other,
                            self.w + other)

    def __sub__(self, other):
        if isinstance(other,AdrState):
            return AdrState(self.M, self.N, self.P,
                            self.z - other.z,
                            self.w - other.w)
        else:
            return AdrState(self.M, self.N, self.P,
                            self.z - other,
                            self.w - other)

    def __mul__(self, other):
        if isinstance(other,AdrState):
            return AdrState(self.M, self.N, self.P,
                            self.z * other.z,
                            self.w * other.w)
        else:
            return AdrState(self.M, self.N, self.P,
                            self.z * other,
                            self.w * other)

    def __div__(self, other):
        if isinstance(other,AdrState):
            return AdrState(self.M, self.N, self.P,
                            self.z / other.z,
                            self.w / other.w)
        else:
            return AdrState(self.M, self.N, self.P,
                            self.z / other,
                            self.w / other)

    def __radd__(self, other):
        return AdrState(self.M, self.N, self.P,
                        other + self.z,
                        other + self.w)

    def __rsub__(self, other):
        return AdrState(self.M, self.N, self.P,
                        other - self.z,
                        other - self.w)

    def __rmul__(self, other):
        return AdrState(self.M, self.N, self.P,
                        other * self.z,
                        other * self.w)

    def __rdiv__(self, other):
        return AdrState(self.M, self.N, self.P,
                        other / self.z,
                        other / self.w)

    def __iadd__(self, other):
        if isinstance(other,AdrState):
            self.z += other.z
            self.w += other.w
            return self
        else:
            self.z += other.z
            self.w += other.w
            return self

    def __isub__(self, other):
        if isinstance(other,AdrState):
            self.z -= other.z
            self.w -= other.w
            return self
        else:
            self.z -= other.z
            self.w -= other.w
            return self

    def __imul__(self, other):
        if isinstance(other,AdrState):
            self.z *= other.z
            self.w *= other.w
            return self
        else:
            self.z *= other.z
            self.w *= other.w
            return self

    def __idiv__(self, other):
        if isinstance(other,AdrState):
            self.z /= other.z
            self.w /= other.w
            return self
        else:
            self.z /= other.z
            self.w /= other.w
            return self

    def __neg__(self):
        return AdrState(self.M, self.N, self.P,
                        - self.z, - self.w)

    def __pos__(self):
        return AdrState(self.M, self.N, self.P,
                        + self.z, + self.w)

    def __abs__(self):
        return AdrState(self.M, self.N, self.P,
                        np.abs(self.z), np.abs(self.w))


class Prox1Adr:
    '''
    First proximal operator for the Adr algorithm
    '''

    def __init__(self, M, N, P, proxCdiv, proxJ):
        self.M = M
        self.N = N
        self.P = P
        self.proxCdiv = proxCdiv
        self.proxJ    = proxJ

    def __repr__(self):
        return ( 'First proximal operator for the Adr algorithm on a grid with shape :' +
                 str(self.M) + ' x ' +
                 str(self.N) + ' x ' +
                 str(self.P) )

    def __delattr__(self, nom_attr):
        raise AttributeError('You can not delete any attribute from this class : Prox1Adr')

    def __call__(self, stagCentGrid):
        stagGrid = self.proxCdiv(stagCentGrid.stagGrid)
        centGrid = self.proxJ(stagCentGrid.centGrid)
        return StaggeredCenteredGrid(self.M, self.N, self.P, stagGrid, centGrid)

class AdrStep:
    '''
    Algorithm step for Adr algorithm
    '''
    def __init__(self, M, N, P, prox1, prox2, alpha):
        self.M = M
        self.N = N
        self.P = P
        self.prox1 = prox1
        self.prox2 = prox2
        self.alpha = alpha

    def __repr__(self):
        return ( 'Adr algorithm step on a grid with shape :' +
                 str(self.M) + ' x ' +
                 str(self.N) + ' x ' +
                 str(self.P) )

    def __delattr__(self, nom_attr):
        raise AttributeError('You can not delete any attribute from this class : AdrStep')

    def __call__(self, stateN, stateNP1):
        stateNP1.w = stateN.w + self.alpha * ( self.prox1( 2 * stateN.z - stateN.w ) - stateN.z )
        stateNP1.z = self.prox2(stateNP1.w)

"""
class AdrAlgorithm:
    '''
    Adr algorithm
    '''
    def __init__(self, M, N, P, proxCdiv, proxJ, proxCstagcent, alpha
"""
