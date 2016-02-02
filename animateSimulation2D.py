#!/usr/bin/env python

from OT.utils.sys.run                                import runCommand
from OT.utils.sys.argv                               import extractArgv
from OT.OTObjects2D.animating.animatingConfiguration import AnimatingConfiguration

# Extract Arguments
arguments   = extractArgv()
configFile  = arguments['CONFIG_FILE']

try:
    printIO = ( arguments['PRINT_IO'] == 'True' )
except:
    printIO = False

# Builds configuration
config      = AnimatingConfiguration(configFile)

# Creates figDir
runCommand('mkdir -p '+config.figDir, printIO)

# Animates
animator    = config.animator()
animator.animate()
