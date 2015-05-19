#################
# Class Algorithm
#################
#
# defines the default class for an algorithm
#
# a real algorithm must also define :
#   * stepFunction [attribute]
#   * setState     [method]
#   * initialize   [method]
#

import cPickle as pck
import time as tm
import numpy as np

from ..OTObject import OTObject

class Algorithm( OTObject ):
    '''
    class to handle an Algorithm
    '''

    def __init__(self, config):
        self.config = config
        OTObject.__init__(self, config.N , config.P)
        self.stateN = None
        self.stateNP1 = None
        
    def __repr__(self):
        return ( 'Algorithm' )

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
            p.dump(self.stateN.convergingStaggeredField())
            f.close()

            f   = open(fileTmap, 'wb')
            X,T = self.stateN.convergingStaggeredField().interpolation().Tmap(self.config.fineResolution)
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
            print(self.config.outputDir+'states.bin')
            print('__________________________________________________')

        except:
            print('__________________________________________________')
            print('WARNING : could not write output files')
            print('__________________________________________________')

    def initialize(self):
        self.stateN = None

        print('Searching for previous runs in '+self.config.outputDir+'...')
        fileRunCount = self.config.outputDir + 'runCount.bin'
        try:
            f = open(fileRunCount, 'rb')
            p = pck.Unpickler(f)
            runCount = p.load()
            f.close()
        except:
            runCount = 0
        
        if runCount > 0:
            print('Found '+str(runCount)+' previous run(s).')
            fileState = self.config.outputDir + 'finalState.bin'
            try:
                f = open(fileState, 'rb')
                p = pck.Unpickler(f)
                self.setState( p.load() )
                f.close()
                print ( 'State loaded from '+fileState )
            except:
                self.stateN = None
        else:
            if self.config.initial == 1:
                print('Searching for previous runs in '+self.config.initialInputDir+'...')
                fileRunCount = self.config.initialInputDir + 'runCount.bin'
                try:
                    f = open(fileRunCount, 'rb')
                    p = pck.Unpickler(f)
                    runCount = p.load()
                    f.close()
                except:
                    runCount = 0
            else:
                runCount = 0

            if runCount > 0:
                print('Found '+str(runCount)+' previous run(s).')
                fileState = self.config.initialInputDir + 'finalState.bin'
                try:
                    f = open(fileState, 'rb')
                    p = pck.Unpickler(f)
                    self.setState( p.load() )
                    f.close()
                    print ( 'State loaded from '+fileState )
                except:
                    self.stateN = None

        self.config.iterCount = 0

    def run(self):
        if self.config.iterTarget == 0:
            return self.stateN.functionalJ()

        print('__________________________________________________')
        print('Initialising algorithm...')
        print('__________________________________________________')
        self.initialize()

        fileCurrentState = self.config.outputDir + 'states.bin'
    
        f = open(fileCurrentState, 'ab')
        p = pck.Pickler(f,protocol=-1)

        print('__________________________________________________')
        print('Starting algorithm...')
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
                print('J           = '+str(self.stateN.functionalJ()))

            if np.mod(self.config.iterCount, self.config.nModWrite) == 0:
                p.clear_memo()
                p.dump(self.stateN.convergingStaggeredField())
                p.dump(tm.time()-timeCheck)
                timeCheck = tm.time()

            self.config.iterCount += 2

        timeAlgo = tm.time() - timeStart
        f.close()
        finalJ = self.stateN.functionalJ()

        print('__________________________________________________')
        print('Algorithm finished')
        print('Number of iterations run : '+str(self.config.iterTarget))
        print('Final J                  = '+str(finalJ))
        print('Time taken               : '+str(timeAlgo))
        print('Mean time per iteration  : '+str(timeAlgo/self.config.iterTarget))
        print('__________________________________________________')

        self.saveState()
        return finalJ

    def rerun(self, newIterTarget):
        self.config.iterTarget = newIterTarget
        return self.run()
