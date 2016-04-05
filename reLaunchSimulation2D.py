#!/usr/bin/env python

#==================================================
#__________________________________________________

# Copyrigth 2016 A. Farchi and M. Bocquet
# CEREA, joint laboratory Ecole des Ponts ParisTech and EDF R&D

# Code for the paper: Using the Wasserstein distance to compare fields of pollutants:
# Application to the radionuclide atmospheric dispersion of the Fukushima-Daiichi accident
# by A. Farchi, M. Bocquet, Y. Roustan, A. Mathieu and A. Querel

#__________________________________________________
#==================================================

from OT.utils.sys.run                        import runCommand
from OT.utils.sys.argv                       import extractArgv
from OT.utils.io.extractConfig               import extractConfig
from OT.utils.io.saveResult                  import saveResult
from OT.OTObjects2D.configuration            import Configuration
from OT.OTObjects2D.analyse.computeOperators import applyAllOperators

# Extract Arguments
arguments        = extractArgv()

try:
    configFile   = arguments['CONFIG_FILE']
    config       = Configuration(configFile)
except:
    outputDir    = arguments['OUTPUT_DIR']
    config       = extractConfig(outputDir) 

config.initial   = 1
config.iterCount = 0

try:
    printIO      = ( arguments['PRINT_IO'] == 'True' )
except:
    printIO      = False

try:
    newIterTarget     = arguments['NEW_ITER_TARGET']
    config.iterTarget = newIterTarget
except:
    pass

# Creates ouputdir
runCommand('mkdir -p '+config.outputDir, printIO)

# Runs algorithm 
algorithm  = config.algorithm()
result     = algorithm.run()

# Saves results
saveResult(config.outputDir, result)

# Analyse
applyAllOperators(config.outputDir)
