###################
# extractAnalyse.py
###################

import cPickle as pck

from files import fileAnalyse

def extractAnalyse(outputDir):

    f                = open(fileAnalyse(outputDir), 'rb')
    p                = pck.Unpickler(f)
    iterationNumbers = p.load()
    iterationTimes   = p.load()
    names            = p.load()
    values           = p.load()
    f.close()

    return (iterationNumbers, iterationTimes, names, values)

def extractAnalyseMultiSim(outputDirList):

    iterNumbers = []
    iterTimes   = []
    names       = []
    values      = []

    for outputDir in outputDirList:
        f = open(fileAnalyse(outputDir), 'rb')
        p = pck.Unpickler(f)
        iterNumbers.append(p.load())
        iterTimes.append(p.load())
        names.append(p.load())
        values.append(p.load())
        f.close()

    return (iterNumbers, iterTimes, names, values) 
