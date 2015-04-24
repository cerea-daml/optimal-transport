import numpy as np
import pickle as pck
import time as tm
from utils_grid import *
import utils_proximals as proximals

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

    def functionalJ(self):
        return self.z.centGrid.functionalJ()

###############
# I/O functions
###############

    def tofile(self,fileName):
        f = open(fileName,'wb')
        p = pck.Pickler(f)
        p.dump(self)
        f.close()
        return 0
    
    def fromfile(fileName):
        f = open(fileName, 'rb')
        p = pck.Unpickler(f)
        state = p.load()
        f.close()
        return state
    fromfile = staticmethod(fromfile)

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

class AdrConfig:
    '''
    Stores confiuration for the Adr algorithm
    '''
    def __init__(self, M, N, P, gamma, alpha, dynamics, outputDir):
        self.M = M
        self.N = N
        self.P = P

        self.gamma = gamma
        self.alpha = alpha

        self.dynamics = dynamics

        self.nModPrint
        self.nModWrite
        self.iterTarget = 0
        self.outputDir = outputDir

    def printConfig(self):
        print( 'Number of iterations : ' + str(self.iterTarget) )
        print( 'dynamics : ' + str(self.dynamics) )
        print( 'alpha = ' + str(self.alpha) )
        print( 'gamma = ' + str(self.gamma) )
        print( 'output to : ' + outputDir )

    def tofile(self, fileName):
        f = open(fileName,'wb')
        p = pck.Pickler(f)
        p.dump(self)
        f.close()
        return 0

class AdrAlgorithm:
    '''
    Adr algorithm
    '''
    def __init__(self, config, boundary):
        self.config = config
        self.boundary = boundary
        
        proxCdiv,proxCsc,proxJ,proxCb = proximals.proximalForDynamics(config, boundary)

        self.prox1 = Prox1Adr(config.M, config.N, config.P, proxCdiv, proxJ)
        self.prox2 = proxCsc

        self.stepFunction = AdrStep(config.M, config.N, config.P, self.prox1, self.prox2, config.alpha)

        self.stateN = AdrState( config.M, config.N, config.P, 
                                StaggeredCenteredGrid(config.M, config.N, config.P),
                                StaggeredCenteredGrid(config.M, config.N, config.P) )
        self.stateNP1 = self.stateN.copy()
        self.iterCount = 0

    def __repr__(self):
        return ( 'Adr algorithm on a grid with shape :' +
                 str(self.config.M) + ' x ' +
                 str(self.config.N) + ' x ' +
                 str(self.config.P) )

    def __delattr__(self, nom_attr):
        raise AttributeError('You can not delete any attribute from this class : AdrAlgorithm')

    def saveState(self, outputDir=None):
        if outputDir is None:
            outputDir = self.config.outputDir

        fileConfig   = outputDir + 'config.bin'
        fileBoundary = outputDir + 'boundary.init'
        fileState    = outputDir + 'finalState.bin'
        
        f = open(fileConfig, 'ab')
        p = pck.Pickler(f)
        p.dump(self.config)
        f.close()

        f = open(fileBoundary, 'wb')
        p = pck.Pickler(f)
        p.dump(self.boundary)
        f.close()

        f = open(fileState, 'wb')
        p = pck.Pickler(f)
        p.dump(self.stateN)
        f.close()

    def setState(self, newState):
        self.stateN = newState
        self.stateNP1 = self.stateN.copy()

    def initialize(self, fileName=None):
        if fileName is None:
            mxu = np.zeros(shape=(self.M+2,self.N+1,self.P+1))
            myu = np.zeros(shape=(self.M+1,self.N+2,self.P+1))
            fu  = np.zeros(shape=(self.M+1,self.N+1,self.P+2))

            if self.config.dynamics == 0:
                for i in xrange(self.P+2):
                    t = float(i)/(self.P+1.)
                    fu[:,:,i] = self.boundary.bt0[:,:]*(1-t) + self.boundary.bt1[:,:]*t

                massIncomingX = 1.0*(self.M/self.P)*np.cumsum(self.boundary.bx0-self.boundary.bx1,1)
                for j in xrange(self.N+1):
                    for i in xrange(self.P+1):
                        fu[:,j,i+1] = fu[:,j,i+1] + massIncomingX[j,i]/(self.M+1)

                massIncomingY = 1.0*(self.N/self.P)*np.cumsum(self.boundary.by0-self.boundary.by1,1)
                for j in xrange(self.M+1):
                    for i in xrange(self.P+1):
                        fu[j,:,i+1] = fu[j,:,i+1] + massIncomingY[j,i]/(self.N+1)

            else:
                for i in xrange(self.P+2):
                    t = float(i)/(self.P+1.)
                    fu[:,:,i] = self.boundary.bt0[:,:]*(1-t) + self.boundary.bt1[:,:]*t


            stagGrid = self.prox1.proxCdiv(StaggeredGrid(self.M, self.N, self.P,
                                                         mxu, myu, fu))
            centGrid = stagGrid.interpolation()
            z = StaggeredCenteredGrid(self.M, self.N, self.P, stagGrid, centGrid)
            w = z.copy()

            self.stateN = AdrState( M, N, P, z, w) 

        else:
            self.stateN = AdrState.fromfile(fileName)

        self.stateNP1 = self.stateN.copy()


    def run(self, iterTarget=1000):
        self.config.iterTarget = iterTarget
        self.iterCount = 0

        fileCurrentState = outputDir + 'states.bin'

        f = open(fileCurrentState, 'ab')
        p = pck.Pickler(f)
        
        print('__________________________________________________')
        print('Starting Adr algorithm...')
        print('__________________________________________________')
        self.config.printConfig()
        print('__________________________________________________')
        timeStart = tm.time()

        while self.iterCount < iterTarget:
            self.stepFunction(self.stateN,self.stateNP1)
            self.stepFunction(self.stateNP1,self.stateNP)

            if np.mod(self.iterCount, self.config.nModPrint) == 0:
                print('_________________________')
                print('iteration   : '+str(self.iterCount)+'/'+str(iterTarget))
                print('elpsed time : '+str(tm.time-timeStart))
                print('J = ',str(self.stateN.functionalJ()))

            if np.mod(self.iterCount, self.config.nModWrite) == 0:
                p.dump(self.stateN)
            self.iterCount += 2

        timeAlgo = tm.time() - timeStart
        f.close()

        print('__________________________________________________')
        print('Adr algorithm finished')
        print('Number of iterations run : '+str(iterTarget))
        print('Final J = '+str(self.stateN.functionalJ()))
        print('Time taken : '+str(timeAlgo))
        print('Mean time per iteration : '+str(timeAlgo/iterTarget))
        print('__________________________________________________')

        self.saveState()
