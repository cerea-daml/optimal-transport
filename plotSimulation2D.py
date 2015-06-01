#!/usr/bin/env python

from OT1D.utils.sys.run                              import runCommand
from OT1D.utils.sys.argv                             import extractArgv
from OT1D.OTObjects2D.plotting.plottingConfiguration import PlottingConfiguration

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
