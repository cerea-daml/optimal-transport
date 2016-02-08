#####################
# computeOperators.py
#####################
#
# applies the operators defined in operators*.py on the result of a simulation
#

import numpy as np
import pickle as pck

from .operators1 import listOfOperators1 as defineListOfOperators1
from .operators2 import listOfOperators2 as defineListOfOperators2

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
        f.close()
    
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
    for run in runs:
        iterationNumbers[i:i+run.size] = run[:]
        i += run.size

    return iterationNumbers

def applyOperators(listOfOperators1, listOfOperators2, outputDir):
    '''
    Apply operators to all states of a simulation
    '''

    print('Starting analyse in '+outputDir+' ...')

    iterationNumbers = extractIterations(outputDir)
    size = iterationNumbers.size

    iterationTimes = np.zeros(size)
    values = np.zeros(shape=(size,len(listOfOperators1)+len(listOfOperators2)))

    i = 0

    fileFinalState = outputDir + 'finalState.bin'
    f = open(fileFinalState, 'rb')
    p = pck.Unpickler(f)
    finalState = p.load().convergingStaggeredField()
    f.close()

    fileStates = outputDir + 'states.bin'
    f = open(fileStates,'rb')
    p = pck.Unpickler(f)

    while i < size :
        state = p.load()
        iterationTimes[i] = p.load()
        for j in range(len(listOfOperators1)):
            values[i,j] = listOfOperators1[j][0](state)
        for j in range(len(listOfOperators2)):
            values[i,len(listOfOperators1)+j] = listOfOperators2[j][0](state,finalState)
        i += 1
    f.close()

    operatorNames = []
    for op in listOfOperators1:
        operatorNames.append(op[1])
    for op in listOfOperators2:
        operatorNames.append(op[1])

    iterationTimes = np.cumsum(iterationTimes)

    fileAnalyse = outputDir + 'analyse.bin'
    f = open(fileAnalyse, 'wb')
    p = pck.Pickler(f,protocol=-1)
    p.dump(iterationNumbers)
    p.dump(iterationTimes)
    p.dump(operatorNames)
    p.dump(values)
    f.close()

    print ('Results written in '+fileAnalyse+' ...')
    return ( iterationNumbers, iterationTimes, values )
    
def applyAllOperators(outputDir):
    listOfOperators1 = defineListOfOperators1()
    listOfOperators2 = defineListOfOperators2()
    return applyOperators(listOfOperators1, listOfOperators2, outputDir)
