#==================================================
#__________________________________________________

# Copyrigth 2016 A. Farchi and M. Bocquet
# CEREA, joint laboratory Ecole des Ponts ParisTech and EDF R&D

# Code for the paper: Using the Wasserstein distance to compare fields of pollutants:
# Application to the radionuclide atmospheric dispersion of the Fukushima-Daiichi accident
# by A. Farchi, M. Bocquet, Y. Roustan, A. Mathieu and A. Querel

#__________________________________________________
#==================================================

#!/usr/bin/env python

from OT.utils.sys.run                        import runCommand
from OT.utils.sys.argv                       import extractArgv
from OT.utils.io.saveResult                  import saveResult
from OT.OTObjects1D.configuration            import Configuration
from OT.OTObjects1D.analyse.computeOperators import applyAllOperators

# Extract Arguments
arguments   = extractArgv()
configFile  = arguments['CONFIG_FILE']

try:
    printIO = ( arguments['PRINT_IO'] == 'True' )
except:
    printIO = False

# Builds configuration
config      = Configuration(configFile)

# Creates ouputdir
runCommand('mkdir -p '+config.outputDir, printIO)

# Runs algorithm 
algorithm   = config.algorithm()
result      = algorithm.run()

# Saves results
saveResult(config.outputDir, result)

# Analyse
applyAllOperators(config.outputDir)
