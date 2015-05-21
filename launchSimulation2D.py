#!/usr/bin/env python
import sys
import cPickle as pck

from OT1D.utils.run                            import runCommand
from OT1D.OTObjects2D.configuration            import Configuration
from OT1D.OTObjects2D.analyse.computeOperators import applyAllOperators

sys.argv.pop(0)
arguments = dict()
for arg in sys.argv:
    members               = arg.split('=')
    arguments[members[0]] = members[1]

configFile = arguments['CONFIG_FILE']

try:
    printIO = ( arguments['PRINT_IO'] == 'True' )
except:
    printIO = False


# Builds configuration
config     = Configuration(configFile)

# Creates ouputdir
runCommand('mkdir -p '+config.outputDir, printIO)

# Runs algorithm 
algorithm  = config.algorithm()
result     = algorithm.run()

# Saves results
fn         = config.outputDir + 'result.bin'
f          = open(fn,'wb')
p          = pck.Pickler(f, protocol=-1)
p.dump(result)
f.close()

# Analyse
applyAllOperators(config.outputDir)
