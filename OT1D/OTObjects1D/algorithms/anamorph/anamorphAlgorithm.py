#________________________
# Class anamorphAlgorithm
#________________________
#
# defines the algorithm compute the anamorphose
#

import cPickle as pck
import time    as tm
import numpy   as np

from scipy.interpolate import interp1d
from scipy.integrate   import cumtrapz

from ...OTObject       import OTObject
from ...grid           import grid
from ....utils.io      import files

#__________________________________________________

def makeiT_t_map(t, CDFInit_map, iCDFFinal_map):
    def T_t_map(x):
        return ( ( 1.0 - t ) * x + t * iCDFFinal_map(CDFInit_map(x)) )
    return T_t_map

#__________________________________________________

def makeInterpolatorPP(X, Y, copy=True):
    if copy:
        return makeInterpolatorPP(X.copy(), Y.copy(), copy=False)

    XPP       = np.zeros(X.size+2)
    XPP[1:-1] = X[:]
    XPP[0]    = X[0] - 1.0
    XPP[-1]   = X[-1] + 1.0

    YPP       = np.zeros(Y.size+2)
    YPP[1:-1] = Y[:]
    YPP[0]    = Y[0] 
    YPP[-1]   = Y[-1]

    return interp1d(XPP, YPP, copy=False, bounds_error=False, fill_value=0.0)

#__________________________________________________

class AnamorphState( OTObject ):
    '''
    class to store the state of an anamorphose Algorithm
    '''

    def __init__(self, state):
        self.state = state

    #_________________________

    def convergingStaggeredField(self):
        return self.state

#__________________________________________________

class AnamorphAlgorithm( OTObject ):
    '''
    class to handle an anamorphose Algorithm
    '''

    def __init__(self, config):
        self.config = config
        OTObject.__init__(self, config.N , config.P)
        self.state = None

    #_________________________
        
    def __repr__(self):
        return ( 'Anamorphose Algorithm' )

    #_________________________

    def saveState(self):
        fileConfig     = files.fileConfig(self.config.outputDir)
        fileState      = files.fileFinalState(self.config.outputDir)
        fileRunCount   = files.fileRunCount(self.config.outputDir)
        fileTmap       = files.fileTMap(self.config.outputDir)

        try:
            f          = open(fileConfig, 'ab')
            p          = pck.Pickler(f,protocol=-1)
            p.dump(self.config)
            f.close()

            f          = open(fileState, 'wb')
            p          = pck.Pickler(f,protocol=-1)
            finalState = AnamorphState(self.state)
            p.dump(finalState)
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

    #_________________________

    def run(self):
        self.config.iterTarget = 1
        fileCurrentState = files.fileStates(self.config.outputDir)
        fileTmap         = files.fileTMap(self.config.outputDir)

        f                = open(fileCurrentState, 'ab')
        p                = pck.Pickler(f,protocol=-1)

        print('__________________________________________________')
        print('Starting algorithm...')
        print('__________________________________________________')
        self.config.printConfig()
        print('__________________________________________________')
        timeStart = tm.time()

        # catch boundary conditions
        f0        = self.config.boundaries.temporalBoundaries.bt0.copy()
        f1        = self.config.boundaries.temporalBoundaries.bt1.copy()

        # apply a non-zero filter to boundary conditions
        meanMass  = f0.mean()
        minValue  = meanMass * self.config.PDFError

        f0        = np.maximum(f0, minValue)
        f1        = np.maximum(f1, minValue)

        # interpolates boundary conditions
        X         = np.linspace(0.0, 1.0, self.N+1)
        f0_map    = interp1d(X.copy(), f0, copy=False, bounds_error=False, fill_value=0.0)
        f1_map    = interp1d(X       , f1, copy=False, bounds_error=False, fill_value=0.0)

        X_fine    = np.linspace(0.0, 1.0, self.config.fineResolution)
        f0_fine   = f0_map(X_fine)
        f1_fine   = f1_map(X_fine)

        # Computing CDF by integration
        CDF0      = cumtrapz(f0_fine, X_fine, initial=0.)
        CDF1      = cumtrapz(f1_fine, X_fine, initial=0.)

        # Rescale CDF1 since
        # mass default could have been produced by the non-zero filter 
        CDF1     *= CDF0[-1] / CDF1[-1]

        CDF0_map  = makeInterpolatorPP(X_fine, CDF0, copy=True)
        CDF1_map  = makeInterpolatorPP(X_fine, CDF1, copy=True)

        iCDF0_map = makeInterpolatorPP(CDF0, X_fine, copy=True)
        iCDF1_map = makeInterpolatorPP(CDF1, X_fine, copy=True)

        # Optimal transport map
        def T_map(x):
            return iCDF0_map(CDF1_map(x))

        def iT_map(x):
            return iCDF1_map(CDF0_map(x))

        # Interpolates solution on a staggered grid
        XS        = np.linspace(0.0, 1.0, self.N+1)
        TS        = np.zeros(self.P+2)
        TS[1:-1]  = np.linspace(0.5/self.P, 1.-0.5/self.P, self.P)
        TS[-1]    = 1.

        fu        = np.zeros(shape=(self.N+1, self.P+2))

        for j in xrange(self.P+2):
            t        = TS[j]
            T_t_map  = makeiT_t_map(t, CDF0_map, iCDF1_map)
            T_t_fine = T_t_map(X_fine)
            
            iT_t_map = makeInterpolatorPP(T_t_fine, X_fine, copy=True)
            
            fu[:, j] = ( ( f0_map(iT_t_map(XS)) ) /
                         ( ( 1.0 - t ) + t * ( ( f0_map(iT_t_map(XS)) ) /
                                               ( f1_map(iT_map(iT_t_map(XS))) ) ) ) )

        # Now computes m to complete the solution of the optimal transport
        # We have df/dt + dm/dx = 0
        dfu_dt       = self.P * ( fu[:,1:] - fu[:,:-1] )

        # Corrects boundary condition
        # this produce non zero divergence to the results
        # it could be appropriate to apply proxCdivb after this algorithm
        divError     = dfu_dt.sum(axis=0)
        dfu_dt      -= divError / ( self.N + 1.0 )
        
        # Computes mu = - int( partialTfu , x )
        mu           = np.zeros(shape=(self.N+2, self.P+1))
        mu[1:,:]     = - dfu_dt[:,:] / self.N
        mu           = mu.cumsum(axis=0)

        # Stores the whole solution in a StaggeredField
        self.state   = grid.StaggeredField( self.N , self.P , mu , fu )

        self.config.iterCount = 1
        self.config.iterTarget = 1

        p.dump(self.state)
        p.dump(tm.time()-timeStart)

        timeAlgo = tm.time() - timeStart
        f.close()

        # Computing final J
        iCDF0_fine   = iCDF0_map(X_fine)
        iCDF1_fine   = iCDF1_map(X_fine)

        finalJ_th    = cumtrapz(np.power(iCDF0_fine-iCDF1_fine, 2), X_fine, initial=0.0)[-1]
        finalJ_th   *= self.P * self.N
        finalJ_st    = self.state.interpolation().functionalJ()
        finalDiv     = self.state.divergence().LInftyNorm()

        timeAlgo     = tm.time() - timeStart
        print('__________________________________________________')
        print('Algorithm finished')
        print('J (th)     = '+str(finalJ_th))
        print('J          = '+str(finalJ_st))
        print('div        = '+str(finalDiv))
        print('Time taken : '+str(timeAlgo))
        print('__________________________________________________')

        # Saves Tmap
        T_fine       = T_map(X_fine)
        f            = open(fileTmap, 'wb')
        np.save(f, X_fine)
        np.save(f, T_fine)
        f.close()
        
        self.saveState()
        return finalJ_th

#__________________________________________________
