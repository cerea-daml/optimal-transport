####################
# Class PdAlgorithm
####################
#
# defines a PD algorithm from configuration
#

import pickle as pck
import time as tm
import numpy as np

from .. import OTObject as oto
from ..grid import grid
from ..init.initialFields import initialStaggeredField
from ..init.initialFields import initialCenteredField
from ..proximals.defineProximals import proximalForConfig

from pdState import PdState
from PdStep import PdStep
from proxPd import Prox1Pd
from proxPd import Prox2Pd

class PdAlgorithm( oto.OTObject ):
    '''
    class to handle a PD Algorithm
    '''

    def __init__(self, config):
        self.config = config
        oto.OTObject.__init__(self, config.N , config.P)
        
        proxCdiv,proxCsc,proxJ,proxCb = proximalForConfig(config)
        prox1 = Prox1Pd(config, proxJ)
        prox2 = Prox2Pd(proxCdiv)
        self.stepFunction = PdStep(config, prox1, prox2)
        self.stateN = None
        self.stateNP1 = None
        
    def __repr__(self):
        return ( 'PD algorithm' )

    def saveState(self):
        fileConfig   = self.config.outputDir + 'config.bin'
        fileState    = self.config.outputDir + 'finalState.bin'
        fileRunCount = self.config.outputDir + 'runCount.bin'

        try:
            f = open(fileConfig, 'ab')
            p = pck.Pickler(f)
            p.dump(self.config)
            f.close()

            f = open(fileState, 'wb')
            p = pck.Pickler(f)
            p.dump(self.stateN)
            f.close()

            try:
                runCount = np.fromfile(fileRunCount)
                runCount += 1.
                runCount.tofile(fileRunCount)
            except:
                runCount = np.ones(1)
                runCount.tofile(fileRunCount)

            self.config.iterCount = 0
            self.config.iterTarget = 0

            print('__________________________________________________')
            print('Files written...')
            print(fileConfig)
            print(fileState)
            print(fileRunCount)
            print(self.config.outputDir+'states.bin')
            print('__________________________________________________')

        except:
            print('__________________________________________________')
            print('WARNING : could not write output')
            print('__________________________________________________')

    def setState(self, newState):
        self.stateN = newState
        self.stateNP1 = self.stateN.copy()

    def initialize(self):
        self.stateN = None

        print('Searching previous runs in '+self.config.outputDir+'...')
        fileRunCount = self.config.outputDir + 'runCount.bin'
        try:
            runCount = np.fromfile(fileRunCount)
            runCount = int(np.floor(runCount[0]))
        except:
            runCount = 0
        
        if runCount > 0:
            print('Found '+str(runCount)+' previous run[s].')
            fileState = self.config.outputDir + 'finalState.bin'
            try:
                f = open(fileState, 'rb')
                p = pck.Unpickler(f)
                self.setState( p.load() )
                f.close()
            except:
                self.stateN = None
        else:
            if self.config.initial == 1:
                print('Searching previous runs in '+self.config.initialInputDir+'...')
                fileRunCount = self.config.initialInputDir + 'runCount.bin'
                try:
                    runCount = np.fromfile(fileRunCount)
                    runCount = int(np.floor(runCount[0]))
                except:
                    runCount = 0
            else:
                runCount = 0

            if runCount > 0:
                print('Found '+str(runCount)+' previous run[s].')
                fileState = self.config.initialInputDir + 'finalState.bin'
                try:
                    f = open(fileState, 'rb')
                    p = pck.Unpickler(f)
                    self.setState( p.load() )
                    f.close()
                except:
                    self.stateN = None

        if self.stateN is None:
            u = initialStaggeredField(self.config)
            y = u.copy()
            v = u.interpolation()
            self.setState( AdrState( self.N , self.P ,
                                     u , y , v ) )

        self.config.iterCount = 0

    def run(self):
        if self.config.iterTarget == 0:
            return self.stateN.functionalJ()

        print('__________________________________________________')
        print('Initialising Pd algorithm...')
        print('__________________________________________________')
        self.initialize()

        fileCurrentState = self.config.outputDir + 'states.bin'
    
        f = open(fileCurrentState, 'ab')
        p = pck.Pickler(f)

        print('__________________________________________________')
        print('Starting Pd algorithm...')
        print('__________________________________________________')
        self.config.printConfig()
        print('__________________________________________________')
        timeStart = tm.time()
        timeCheck = timeStart

        while self.config.iterCount < self.config.iterTarget:
            self.stepFunction(self.stateN,self.stateNP1)
            self.stepFunction(self.stateNP1,self.stateN)

            if np.mod(self.config.iterCount, self.config.nModPrint) == 0:
                print('___________________________________')
                print('iteration   : '+str(self.config.iterCount)+'/'+str(self.config.iterTarget))
                print('elpsed time : '+str(tm.time()-timeStart))
                print('J = '+str(self.stateN.functionalJ()))

            if np.mod(self.config.iterCount, self.config.nModWrite) == 0:
                p.dump(self.stateN)
                p.dump(tm.time()-timeCheck)
                timeCheck = tm.time()

            self.config.iterCount += 2

        timeAlgo = tm.time() - timeStart
        f.close()
        finalJ = self.stateN.functionalJ()

        print('__________________________________________________')
        print('Pd algorithm finished')
        print('Number of iterations run : '+str(self.config.iterTarget))
        print('Final J = '+str(finalJ))
        print('Time taken : '+str(timeAlgo))
        print('Mean time per iteration : '+str(timeAlgo/self.config.iterTarget))
        print('__________________________________________________')

        self.saveState()
        return finalJ

    def rerun(self, newIterTarget):
        self.config.iterTarget = newIterTarget
        self.run()
