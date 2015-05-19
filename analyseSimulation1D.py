#!/usr/bin/env python 
import sys
from OT1D.OTObjects1D.analyse.computeOperators import applyAllOperators
from OT1D.OTObjects1D.configuration            import Configuration

sys.argv.pop(0)
arguments = dict()
for arg in sys.argv:
    members               = arg.split('=')
    arguments[members[0]] = members[1]

try:
    configFile = arguments['CONFIG_FILE']
    config     = Configuration(configFile)
    outputDir  = config.outputDir
except:
    outputDir  = arguments['OUTPUT_DIR']

applyAllOperators(outputDir)
