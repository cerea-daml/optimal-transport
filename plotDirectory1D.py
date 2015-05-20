#!/usr/bin/env python
import sys

from OT1D.utils.run                           import runCommand
from OT1D.OTObjects1D.configuration           import Configuration
from OT1D.OTObjects1D.plotting.plotAnalyse    import plotAnalyseDefaultSubplots
from OT1D.OTObjects1D.plotting.plotFinalState import plotFinalState
from OT1D.OTObjects1D.plotting.plotFinalState import defaultTransparency
from OT1D.OTObjects1D.plotting.plotFinalState import fastVanishingTransparency
from OT1D.OTObjects1D.plotting.plotFinalState import customTransparency

sys.argv.pop(0)
arguments = dict()
for arg in sys.argv:
    members               = arg.split('=')
    arguments[members[0]] = members[1]

try:
    printIO = ( arguments['PRINT_IO'] == 'True' )
except:
    printIO = False

try:
    configFile = arguments['CONFIG_FILE']
    config     = Configuration(configFile)
except:
    outputDir  = arguments['OUTPUT_DIR']
    configFile = outputDir + 'config.bin'
    f          = open(configFile, 'rb')
    p          = pck.Unpickler(f)
    try:
        while True:
            config = p.load()
    except:
        pass

try:
    figDir = arguments['FIG_DIR']
except:
    figDir = outputDir

try:
    prefixFigName = arguments['PREFIX_FIG_NAME']
except:
    prefixFigName = 'finalState'

try:
    transpFunName = arguments['TRANSP_FUN_NAME']
    if transpFunName == 'default':
        transpFun = defaultTransparency
    elif transpFunName == 'fastVanishing':
        transpFun = fastVanishingTransparency
    elif transpFunName == 'custom':
        transpFun = customTransparency
except:
    transpFun = None

try:
    swapInitFinal = ( arguments['SWAP_INIT_FINAL'] == 'True' )
except:
    swapInitFinal = False

try:
    optCurrent = arguments['OPT_CURRENT']
    optInit    = arguments['OPT_INIT']
    optFinal   = arguments['OPT_FINAL']
    opt        = [optInit, optFinal, optCurrent]
except:
    opt        = None

if config.swappedInitFinal:
    swapInitFinal = not swapInitFinal

runCommand('mkdir -p '+figDir, printIO)
plotAnalyseDefaultSubplots(config.outputDir, figDir, 'analyseIter')
plotAnalyseDefaultSubplots(config.outputDir, figDir, 'analyseTime', 'time')
plotFinalState(config.outputDir, figDir, prefixFigName, transpFun=transpFun, options=opt, swapInitFinal=swapInitFinal)


