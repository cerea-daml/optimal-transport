#!/usr/bin/env python

from OT.utils.sys.run                              import runCommand
from OT.utils.sys.argv                             import extractArgv
from OT.OTObjects1D.plotting.plottingConfiguration import PlottingConfiguration

# Extract Arguments
arguments   = extractArgv()
configFile  = arguments['CONFIG_FILE']

try:
    printIO = ( arguments['PRINT_IO'] == 'True' )
except:
    printIO = False

# Builds configuration
config      = PlottingConfiguration(configFile)

# Creates figDir
runCommand('mkdir -p '+config.figDir, printIO)

# Plots
plotter     = config.plotter()
plotter.plot()
