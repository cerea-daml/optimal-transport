#!/usr/bin/env python

from OT1D.utils.run                           import runCommand
from OT1D.OTObjects1D.plotting.animFinalState import animFinalState
from OT1D.OTObjects1D.plotting.animFinalState import defaultTransparency
from OT1D.OTObjects1D.plotting.animFinalState import fastVanishingTransparency
from OT1D.OTObjects1D.plotting.animFinalState import customTransparency

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
    figName = arguments['FIG_NAME']
except:
    figName = 'finalState.mp4'

try:
    writer = arguments['WRITER']
except:
    writer = 'ffmpeg'

try:
    interval = arguments['INTERVAL']
except:
    interval = 'ffmpeg'

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

animFinalState(outputDir, figDir, figName, writer, interval, transpFun, options=opt, swapInitFinal=swapInitFinal)

