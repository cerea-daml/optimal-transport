#__________________________________________________
#__________________________________________________

# Copyrigth 2016 A. Farchi and M. Bocquet
# CEREA, joint laboratory Ecole des Ponts ParisTech and EDF R&D

# Code for the paper: Using the Wasserstein distance to compare fields of pollutants:
# Application to the radionuclide atmospheric dispersion of the Fukushima-Daiichi accident
# by A. Farchi, M. Bocquet, Y. Roustan, A. Mathieu and A. Querel

#__________________________________________________

#__________________________________________________
#________________________
# Class ProjectAlgorithm
#________________________

import cPickle as pck
import time    as tm
import numpy   as np

from ...proximals.defineProximals      import proximalForConfig
from ...OTObject                       import OTObject
from ...grid                           import grid
from ....utils.io                      import files

#__________________________________________________

class ProjectState( OTObject ):
    '''
    class to store the state of an projection Algorithm
    '''

    def __init__(self, state):
        self.state = state

    #_________________________

    def convergingStaggeredField(self):
        return self.state

#__________________________________________________

class ProjectAlgorithm( OTObject ):
    '''
    class to handle an projection Algorithm
    '''

    def __init__(self, config):
        OTObject.__init__(self, config.N , config.P)
        self.config                        = config
        self.config.dynamics               = 1
        (proxCdiv, proxCsc, proxJ, proxCb) = proximalForConfig(self.config)
        self.prox                          = proxCdiv
        self.state                         = None

    #_________________________
        
    def __repr__(self):
        return ( 'Projection Algorithm' )

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
            finalState = ProjectState(self.state)
            p.dump(finalState)
            f.close()

            f          = open(fileTmap, 'wb')
            (X, T)     = self.state.interpolation().Tmap(self.config.fineResolution)
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

    #_________________________

    def run(self):
        self.config.iterTarget = 1
        fileCurrentState = files.fileStates(self.config.outputDir)

        f                = open(fileCurrentState, 'ab')
        p                = pck.Pickler(f,protocol=-1)

        print('__________________________________________________')
        print('Starting algorithm...')
        print('__________________________________________________')
        self.config.printConfig()
        print('__________________________________________________')
        timeStart              = tm.time()
        self.state             = self.prox(grid.StaggeredField(self.N, self.P))
        self.config.iterCount  = 1
        self.config.iterTarget = 1

        p.dump(self.state)
        p.dump(tm.time()-timeStart)
        f.close()

        finalJ   = self.state.interpolation().functionalJ()
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

#__________________________________________________
