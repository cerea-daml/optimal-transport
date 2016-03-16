#==================================================
#__________________________________________________

# Copyrigth 2016 A. Farchi and M. Bocquet
# CEREA, joint laboratory Ecole des Ponts ParisTech and EDF R&D

# Code for the paper: Using the Wasserstein distance to compare fields of pollutants:
# Application to the radionuclide atmospheric dispersion of the Fukushima-Daiichi accident
# by A. Farchi, M. Bocquet, Y. Roustan, A. Mathieu and A. Querel

#__________________________________________________
#==================================================

###################
# extractAnalyse.py
###################

import pickle as pck

from .files import fileAnalyse

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
