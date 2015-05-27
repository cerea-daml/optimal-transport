######################
# finalStatePlotter.py
######################

from ....utils.plotting.defaultTransparency import defaultTransparency
from ....utils.plotting.defaultTransparency import fastVanishingTransparency
from ....utils.plotting.defaultTransparency import customTransparency

from plotFinalStateMultiSim                 import plotFinalStateMultiSim

class FinalStatePlotter:

    def __init__(self, plottingConfig):
        self.plottingConfig = plottingConfig

    def plot(self):
        if not self.plottingConfig.plotFinalState == 1:
            return

        if self.plottingConfig.plotFinalState_transparencyFunction == 'defaultTransparency':
            transparencyFunction = defaultTransparency
        elif self.plottingConfig.plotFinalState_transparencyFunction == 'fastVanishingTransparency':
            transparencyFunction = fastVanishingTransparency
        elif self.plottingConfig.plotFinalState_transparencyFunction == 'customTransparency':
            transparencyFunction = customTransparency

        if self.plottingConfig.singleOrMulti == 0:
            outputDirList = [self.plottingConfig.outputDir[0]]
            labelList     = [self.plottingConfig.label[0]]
        elif self.plottingConfig.singleOrMulti == 1:
            outputDirList = self.plottingConfig.outputDir
            labelList     = self.plottingConfig.label

        plotFinalStateMultiSim(outputDirList, 
                               self.plottingConfig.figDir, 
                               self.plottingConfig.plotFinalState_prefixFigName,
                               labelList, 
                               transparencyFunction, 
                               bool(self.plottingConfig.plotFinalState_addLegend),
                               bool(self.plottingConfig.plotFinalState_grid),
                               bool(self.plottingConfig.plotFinalState_addTimeTextPbar),
                               self.plottingConfig.plotFinalState_xLabel, 
                               self.plottingConfig.plotFinalState_yLabel,
                               self.plottingConfig.plotFinalState_nbrXTicks,
                               self.plottingConfig.plotFinalState_nbrYTicks,
                               self.plottingConfig.plotFinalState_xTicksRound,
                               self.plottingConfig.plotFinalState_yTicksRound,
                               self.plottingConfig.extension, 
                               self.plottingConfig.EPSILON)
