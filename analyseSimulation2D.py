#!/usr/bin/env python 

from .OT1D.utils.sys.argv                       import extractArgv
from .OT1D.OTObjects2D.configuration            import Configuration
from .OT1D.OTObjects2D.analyse.computeOperators import applyAllOperators

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
