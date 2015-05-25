######################
# finalStatePlotter.py
######################

from ....utils.plotting.defaultTransparency import defaultTransparency
from ....utils.plotting.defaultTransparency import fastVanishingTransparency
from ....utils.plotting.defaultTransparency import customTransparency

from plotFinalState         import plotFinalState
from plotFinalStateMultiSim import plotFinalStateMultiSim

class FinalStatePlotter:

    def __init__(self, plottingConfig):
        self.plottingConfig = plottingConfig

    def plot(self):
        if not self.plottingConfig.plotFinalState == 1:
            return

        if self.plottingConfig.transparencyFunctionName == 'defaultTransparency':
            transparencyFunction = defaultTransparency
        elif self.plottingConfig.transparencyFunctionName == 'fastVanishingTransparency':
            transparencyFunction = fastVanishingTransparency
        elif self.plottingConfig.transparencyFunctionName == 'customTransparency':
            transparencyFunction = customTransparency

        if self.plottingConfig.singleOrMulti == 0:
            plotFinalState(self.plottingConfig.outputDir[0], self.plottingConfig.figDir, self.plottingConfig.prefixFigNameFinalState, 
                           self.plottingConfig.label[0], transparencyFunction, self.plottingConfig.extension, self.plottingConfig.EPSILON)

        elif self.plottingConfig.singleOrMulti == 1:
            plotFinalStateMultiSim(self.plottingConfig.outputDir, self.plottingConfig.figDir, self.plottingConfig.prefixFigNameFinalState, 
                                   self.plottingConfig.label; transparencyFunction, self.plottingConfig.extension, self.plottingConfig.EPSILON)
