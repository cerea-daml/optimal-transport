#!/usr/bin/env python

from OT.utils.sys.run                        import runCommand
from OT.utils.sys.argv                       import extractArgv
from OT.utils.io.saveResult                  import saveResult
from OT.OTObjects2D.configuration            import Configuration
from OT.OTObjects2D.analyse.computeOperators import applyAllOperators

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
