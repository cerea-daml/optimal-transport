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
        (iN, iT, n, v) = extractAnalyse(outputDir)

        iterNumbers.append(iN)
        iterTimes.append(iT)
        names.append(n)
        values.append(v)

    return (iterNumbers, iterTimes, names, values) 
