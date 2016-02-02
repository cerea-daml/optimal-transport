#__________________________________________________
# launchers.py
#__________________________________________________
#
# defines some launchers for 1D Optimal Transport
#

from .OTObjects1D.configuration import Configuration
from .OTObjects1D.analyse.computeOperators import applyAllOperators
from .OTObjects1D.plotting.plotAnalyse import plotAnalyseDefaultSubplots
from .OTObjects1D.plotting.plotAnalyseMultiSim import plotAnalysesDefaultSubplots

from .OTObjects1D.plotting.plotFinalStep import plotFinalState
from .OTObjects1D.plotting.plotFinalStep import animFinalState
from .OTObjects1D.plotting.plotFinalStepMultiSim import plotFinalStateMultiSim
from .OTObjects1D.plotting.plotFinalStepMultiSim import animFinalStateMultiSim

import pickle as pck

def launchFromConfigFile(configFile):
    '''
    Defines configuration from file configFile.
    Constructs the corresponding algorithm.
    Runs the algorithm.
    '''
    config = Configuration(configFile)
    algorithm = config.algorithm()
    return algorithm.run()

def continueFromDir(directory, newIterTarget=None):
    '''
    Assumes directory is an ouput directory from a previous run.
    Search for a configuration in file config.bin.
    Runs newIterTarget (if given or previous config.iterTarget) iterations from the last final state. 
    '''
    configsFile = directory + 'config.bin'
    f = open(configsFile, 'rb')
    p = pck.Unpickler(f)
    try:
        while True:
            config = p.load()
    except:
        pass

    if not newIterTarget is None:
        config.iterTarget = newIterTarget

    algorithm = config.algorithm()
    return algorithm.run()

def analyseFromConfigFile(configFile):
    '''
    Applies analyse operators to the state for the analyse corresponding to the given configuration file.
    '''
    
    config = Configuration(configFile)
    return applyAllOperators(config.outputDir)

def analyseFromDir(directory):
    '''
    Does the same for the result of the analyse stored in the given directory.
    '''
    return applyAllOperators(directory)

def plotAnalyseFromDir(directory):
    '''
    Plots the analyse result stored in the given directory.
    '''
    plotAnalyseDefaultSubplots(directory,directory,'analyseIter')
    plotAnalyseDefaultSubplots(directory,directory,'analyseTime','time')

def plotMultiAnalysesFromDir(directoryList,figDir):
    plotAnalysesDefaultSubplots(directoryList,figDir,'analyseIter')
    plotAnalysesDefaultSubplots(directoryList,figDir,'analyseTime','time')

def plotFinalStateFromDir(directory):
    '''
    Plots the result of a simulation stored in the given directory.
    '''
    plotFinalState(directory, directory, 'finalState', transpFun=None, options=None)

def animFinalStateFromDir(directory):
    '''
    Animates the result of a simulation stored in the given directory.
    '''
    animFinalState(directory, directory, figName='finalState.mp4', writer='ffmpeg', interval=100., transpFun=None, options=None)

def plotMultiFinalStateFromDir(directoryList,figDir):
    plotFinalStateMultiSim(directoryList, figDir, prefixFigName='finalState', transpFun=None, labelsList=None, options=None)

def animMultiFinalStateFromDir(directoryList,figDir):
    animFinalStateMultiSim(directoryList, figDir, figName='finalState.mp4', writer='ffmpeg', interval=100., transpFun=None, options=None)
