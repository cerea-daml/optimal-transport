import sys
import os
import pickle

from OT1D.OTObjects.configuration import Configuration
from OT1D.OTObjects.analyse.computeOperators import applyAllOperators
from OT1D.OTObjects.plotting.plotAnalyse import plotAnalyseDefaultSubplot
from OT1D.OTObjects.plotting.plotFinalStep import animFinalState

def myrun(command):
    status = os.system(command)
    if status != 0:
        sys.exit(status)

# Builds configuration
fileName = str(sys.argv[1])
config = Configuration(fileName)

# Creates ouputdir
myrun( 'mkdir -p '+config.outputDir)

# Runs algorithm 
algorithm = config.algorithm()
res = algorithm.run()

# Saves results
fn = config.outputDir+'result.bin')
f = open(fn,'wb')
p = pickle.Pickler(f)
p.dump(res)
f.close()

# Analyse
applyAllOperators(config.outputDir)

# Plotting
plotDir = str(sys.argv[2])
plotAnalyseDefaultSubplots(config.outputDir,plotDir,'analyseIter')
plotAnalyseDefaultSubplots(config.outputDir,plotDir,'analyseTime','time')
animFinalState(config.outputDir, plotDir, figName='finalState.mp4', writer='avconv', interval=100.)
