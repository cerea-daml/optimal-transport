####################
# Class AdrAlgorithm
####################
#
# defines an ADR algorithm from configuration
#
# config must define :
#   * N
#   * P
#   * alpha
#   * outputDir
#
#   * iterCount
#

import pickle as pck
import time as tm

from .. import OTObject as oto
from ..grid import grid
from ..init.initialFields import initialStaggeredCenteredField
from ..proximals.defineProximals import proximalForConfig

from adrState import AdrState
from adrStep import AdrStep
from prox1Adr import Prox1Adr

class AdrAlgorithm( oto.OTObject ):
    '''
    class to handle an ADR Algorithm
    '''

    def __init__(self, config):
        self.config = config
        oto.OTObject.__init__(self, config.N , config.P)
        
        proxCdiv,proxCsc,proxJ,proxCb = proximalForConfig(self.config)
        prox1 = Prox1Adr( config.N, config.P, proxCdiv, proxJ)
        self.stepFunction = AdrStep(prox1, prosCsc, config.alpha)
        self.initialize()
        
    def __repr__(self):
            return ( 'ADR algorithm' )

    def saveState(self, outputDir=None):
        if outputDir is None:
            outputDir = self.config.outputDir

        fileConfig   = outputDir + 'config.bin'
        fileBoundary = outputDir + 'boundary.init'
        fileState    = outputDir + 'finalState.bin'
        fileRunCount = outputDir + 'runCount.bin'

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

        try:
            runCount = np.fromfile(fileRunCount)
            runCount += 1.
            runCount.tofile(fileRunCount)
        except:
            runCount = np.ones(1)
            runCount.tofile(fileRunCount)

    def setState(self, newState):
        self.stateN = newState
        self.stateNP1 = self.stateN.copy()

    def initialize(self, outputDir=None):
        if outputDir is None:
            outputDir = self.config.outputDir

        fileRunCount = outputDir + 'runCount.bin'
        try:
            runCount = np.fromfile(fileRunCount)
            runCount = int(no.floor(runCount[0]))
        except:
            runCount = 0
        
        if runCount > 0:
            fileState = outputDir + 'finalState.bin'
            f = open(fileState, 'rb')
            p = pck.Unpickler(f)
            self.setState( p.load() )
            f.close()

        else:
            self.setState( initialStaggeredCenteredField(self.config) )

        self.config.iterCount = 0

    def run(self):
        # TO WRITE ...
        pass
    
