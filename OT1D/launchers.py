#__________________________________________________
# launchers.py
#__________________________________________________
#
# defines some launchers for 1D Optimal Transport
#

from OTObjects.configuration import Configuration
from OTObjects.analyse.computeOperators import applyAllOperators
from OTObjects.plotting.plotAnalyse import plotAnalyseDefaultSubplots
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

