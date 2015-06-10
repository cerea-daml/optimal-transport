#_____________________
# finalStatePlotter.py
#_____________________

from ....utils.plotting.defaultTransparency import getTransparencyFunction
from ....utils.plotting.plotting            import makeOutputDirLabelPrefixFigNameList
from plotFinalStateMultiSim                 import plotFinalStateMultiSim

#__________________________________________________

class FinalStatePlotter:

    def __init__(self, config):
        self.config = config

    #_________________________

    def plot(self):
        if not self.config.plotFinalState:
            return

        transparencyFunction = getTransparencyFunction(self.config.plotFinalState_transparencyFunction)

        ( outputDirListList,
          labelListList,
          prefixFigNameList) = makeOutputDirLabelPrefixFigNameList(self.config.singleOrMulti,
                                                                   self.config.outputDirList,
                                                                   self.config.labelList,
                                                                   self.config.plotFinalState_prefixFigName)

        for (outputDirList,
             labelList,
             prefixFigName) in zip(outputDirListList,
                                   labelListList,
                                   prefixFigNameList):
            
            plotFinalStateMultiSim(outputDirList, 
                                   self.config.figDir, 
                                   prefixFigName,
                                   labelList, 
                                   transparencyFunction, 
                                   self.config.plotFinalState_legend,
                                   self.config.plotFinalState_grid,
                                   self.config.plotFinalState_timeTextPBar,
                                   self.config.plotFinalState_xLabel, 
                                   self.config.plotFinalState_yLabel,
                                   self.config.plotFinalState_extendX,
                                   self.config.plotFinalState_extendY,
                                   self.config.plotFinalState_nbrXTicks,
                                   self.config.plotFinalState_nbrYTicks,
                                   self.config.plotFinalState_xTicksDecimals,
                                   self.config.plotFinalState_yTicksDecimals,
                                   self.config.plotFinalState_order,
                                   self.config.plotFinalState_extendDirection,
                                   self.config.extensions, 
                                   self.config.EPSILON)

#__________________________________________________
