#==================================================
#__________________________________________________

# Copyrigth 2016 A. Farchi and M. Bocquet
# CEREA, joint laboratory Ecole des Ponts ParisTech and EDF R&D

# Code for the paper: Using the Wasserstein distance to compare fields of pollutants:
# Application to the radionuclide atmospheric dispersion of the Fukushima-Daiichi accident
# by A. Farchi, M. Bocquet, Y. Roustan, A. Mathieu and A. Querel

#__________________________________________________
#==================================================

##########
# files.py
##########

def fileAnalyse(outputDir):
    return outputDir + 'analyse.bin'

def fileFinalState(outputDir):
    return outputDir + 'finalState.bin'

def fileConfig(outputDir):
    return outputDir + 'config.bin'

def fileResult(outputDir):
    return outputDir + 'result.bin'

def fileTMap(outputDir):
    return outputDir + 'Tmap.npy'

def fileRunCount(outputDir):
    return outputDir + 'runCount.bin'

def fileStates(outputDir):
    return outputDir + 'states.bin'
