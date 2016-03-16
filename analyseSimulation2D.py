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

from OT.utils.sys.argv                       import extractArgv
from OT.OTObjects2D.configuration            import Configuration
from OT.OTObjects2D.analyse.computeOperators import applyAllOperators

# Extract Arguments
arguments      = extractArgv()

try:
    configFile = arguments['CONFIG_FILE']
    config     = Configuration(configFile)
    outputDir  = config.outputDir
except:
    outputDir  = arguments['OUTPUT_DIR']

# Analyse
applyAllOperators(outputDir)
