#####################
# computeOperators.py
#####################
#
# applies the operators defined in operators*.py on the result of a simulation
#

import numpy as np
import pickle as pck

def extractIterations(outputDir):
    '''
    Extracts the iteration numbers from config file for a simulation
    '''
    fileConfig = outputDir + 'config.bin'

    f = open(fileConfig,'rb')
    p = pck.Unpickler(f)
    data = []
    try:
        while True:
            config = p.load()
            data.append( ( config.iterTarget , config.nModWrite ) )
    except:
        pass
    
    runs = []
    iStart = 0
    size = 0
    for (iterTarget, nMod) in data:
        sizeRun = 1 + int( np.floor((iterTarget-1.)/nMod) )
        runs.append( np.arange(sizeRun)*nMod + iStart + 2. )
        iStart += iterTarget
        size += sizeRun

    iterationNumbers = np.zeros(size)
    i = 0
    for run in in runs:
        iterationNumbers[i:i+run.size] = run[:]
        i += run.size

    return iterationNumbers

def applyOperators(listOfOperators1, listOfOperators2, outputDir):
    '''
    Apply operators to all states of a simulation
    '''

    iterationNumbers = extractIterations(outputDir)
    size = iterationNumbers.size

    iterationTimes = np.zeros(size)
    values = np.zeros(shape=(size,len(listOfOperators)+len(listOfOperators2)))

    i = 0

    fileFinalState = outputDir + 'finalState.bin'
    f = open(fileFinalState, 'rb')
    p = pck.Unpickler(f)
    finalState = p.load()

    fileStates = outputDir + 'states.bin'
    f = open(fileStates,'rb')
    p = pck.Unpickler(f)

    while i < size :
        state = p.load()
        iterationTimes[i] = p.load()
        for j in xrange(len(listOfOperators1)):
            values[i,j] = listOfOperators1[j](state)
        for j in xrange(len(listOfOperators2)):
            values[i,len(listOfOperators1)+j] = listOfOperators2[j](state,finalState)
        i += 1

    return ( iterationNumbers, iterationTimes, values )
    
        
