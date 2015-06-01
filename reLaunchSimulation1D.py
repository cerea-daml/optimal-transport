#!/usr/bin/env python

from OT1D.utils.sys.run                        import runCommand
from OT1D.utils.sys.argv                       import extractArgv
from OT1D.utils.io.extractConfig               import extractConfig
from OT1D.utils.io.saveResult                  import saveResult
from OT1D.OTObjects1D.configuration            import Configuration
from OT1D.OTObjects1D.analyse.computeOperators import applyAllOperators

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
