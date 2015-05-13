#########################
# Class anamorphAlgorithm
#########################
#
# defines the compute the anamorphose
#
# alternative version... seems to be less accurate to compute partialXTmap
#

import cPickle as pck
import pickle 

import time as tm
import numpy as np
from scipy.interpolate import interp1d

from ...OTObject import OTObject
from ...grid import grid

class AnamorphAlgorithm( OTObject ):
    '''
    class to handle an anamorphose Algorithm
    '''

    def __init__(self, config):
        self.config = config
        OTObject.__init__(self, config.N , config.P)
        self.state = None
        
    def __repr__(self):
        return ( 'Anamorphose Algorithm' )

    def saveState(self):
        fileConfig   = self.config.outputDir + 'config.bin'
        fileState    = self.config.outputDir + 'finalState.bin'
        fileRunCount = self.config.outputDir + 'runCount.bin'
        fileTmap     = self.config.outputDir + 'Tmap.npy'

        try:
            f = open(fileConfig, 'ab')
            p = pck.Pickler(f,protocol=-1)
            p.dump(self.config)
            f.close()

            f = open(fileState, 'wb')
            p = pck.Pickler(f,protocol=-1)
            p.dump(self.state)
            f.close()

            f   = open(fileTmap, 'wb')
            X,T = self.state.interpolation().Tmap()
            np.save(f, X)
            np.save(f, T)
            f.close()

            try:
                f = open(fileRunCount, 'rb')
                p = pck.Unpickler(f)
                runCount = p.load()
                runCount += 1
                f.close()
            except:
                runCount = 1
                
            f = open(fileRunCount, 'wb')
            p = pck.Pickler(f,protocol=-1)
            p.dump(runCount)
            f.close()

            self.config.iterCount = 0
            self.config.iterTarget = 0

            print('__________________________________________________')
            print('Files written...')
            print(fileConfig)
            print(fileState)
            print(fileRunCount)
            print(fileTmap)
            print('__________________________________________________')

        except:
            print('__________________________________________________')
            print('WARNING : could not write output files')
            print('__________________________________________________')

    def run(self):
        self.config.iterTarget = 1
        fileCurrentState = self.config.outputDir + 'states.bin'
    
        f = open(fileCurrentState, 'ab')
        p = pck.Pickler(f,protocol=-1)

        print('__________________________________________________')
        print('Starting algorithm...')
        print('__________________________________________________')
        self.config.printConfig()
        print('__________________________________________________')
        timeStart = tm.time()

        # Computing CDF for initial and final states
        N = self.config.N
        P = self.config.P

        fInit  = self.config.boundaries.temporalBoundaries.bt0
        fFinal = self.config.boundaries.temporalBoundaries.bt1

        CDFInit  = np.zeros(N+1)
        CDFFinal = np.zeros(N+1)

        CDFInit[1:N+1]  = 0.5*( fInit[0:N]  + fInit[1:N+1]  )
        CDFFinal[1:N+1] = 0.5*( fFinal[0:N] + fFinal[1:N+1] )

        CDFInit  = CDFInit.cumsum()
        CDFFinal = CDFFinal.cumsum()

        # This should do nothing, but just to make sure ...
        CDFFinal *= CDFInit[N] / CDFFinal[N]

        # Computes maps associated to the CDF arrays by interpolating
        XCDF        = np.linspace( 0.0-0.001 , 1.0+0.001 , N+1 )

        FInitMap    = interp1d( XCDF , fInit    )
        CDFFinalMap = interp1d( XCDF , CDFFinal )
        iCDFInitMap = interp1d( CDFInit , XCDF  )

        # T = CDFInit^(-1) o CDFFinal
        def Tmap(x):
            return iCDFInitMap( CDFFinalMap( x ) )

        # Computes the derivative of T by finate differences
        # on a finer grid (to try and avoid infinite derivative)
        # result is stored in partialXTarray
        NN         = self.config.fineResolution
        XT         = np.zeros(NN+3)
        XT[1:NN+2] = np.linspace( 0.0 , 1.0 , NN+1 )
        XT[0]      = - XT[2]
        XT[NN+2]   = 1. + XT[2]

        Tarray         = np.zeros(NN+3)
        Tarray[1:NN+2] = Tmap(XT[1:NN+2])
        Tarray[0]      = XT[0]
        Tarray[NN+2 ]  = XT[NN+2]

        partialXTarray = NN * ( Tarray[1:] - Tarray[:NN+2] ) 
        Xpartial       = 0.5 * ( XT[1:] + XT[:NN+2] )

        # Computes maps associated to the derivative of T by interpolating         
        partialXTmap = interp1d( Xpartial , partialXTarray )

        # Approximate solution of the optimal transport
        def func(x,t):
            return ( FInitMap( ( 1. - t ) * x + t * Tmap(x) ) *
                     abs( ( 1. - t ) + t * partialXTmap(x) ) )

        # Storing solution in a staggered grid
        fu = np.zeros(shape=(N+1,P+2))
        X  = np.linspace( 0.0 , 1.0 , N+1 )
        T  = np.zeros(P+2)

        T[1:P+1] = np.linspace( 0.5/P , 1.0-0.5/P , P )
        T[0]     = 0.
        T[P+1]   = 1.

        for i in xrange(N+1):
            for j in xrange(P+2):
                fu[i,j] = func( X[i] , T[j] )

        # Now computes m to complete the solution of the optimal transport
        # We have df/dt + dm/dx = 0
        partialTfu  = fu[:,1:P+2].copy()
        partialTfu -= fu[:,0:P+1]
        partialTfu *= P

        # Corrects boundary condition
        # this produce non zero divergence to the results
        # it could be appropriate to apply proxCdivb after this algorithm
        divError = partialTfu.sum(axis=0)
        partialTfu -= divError / ( N + 1. )
        
        # Computes mu = - int( partialTfu , x )
        mu = np.zeros(shape=(N+2,P+1))
        mu[1:N+2,:] = - partialTfu[:,:] / N
        mu = mu.cumsum(axis=0)

        # Stores the whole solution in a StaggeredField
        self.state = grid.StaggeredField( N , P , mu , fu )

        self.config.iterCount = 1
        self.config.iterTarget = 1

        p.dump(self.state)
        p.dump(tm.time()-timeStart)

        timeAlgo = tm.time() - timeStart
        f.close()

        finalJ = self.state.interpolation().functionalJ()
        finalDiv = self.state.divergence().LInftyNorm()

        timeAlgo = tm.time() - timeStart
        print('__________________________________________________')
        print('Algorithm finished')
        print('J          = '+str(finalJ))
        print('div        = '+str(finalDiv))
        print('Time taken : '+str(timeAlgo))
        print('__________________________________________________')

        self.saveState()
        return finalJ
