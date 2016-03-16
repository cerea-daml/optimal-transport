#==================================================
#__________________________________________________

# Copyrigth 2016 A. Farchi and M. Bocquet
# CEREA, joint laboratory Ecole des Ponts ParisTech and EDF R&D

# Code for the paper: Using the Wasserstein distance to compare fields of pollutants:
# Application to the radionuclide atmospheric dispersion of the Fukushima-Daiichi accident
# by A. Farchi, M. Bocquet, Y. Roustan, A. Mathieu and A. Querel

#__________________________________________________
#==================================================

#_____________________
# finalStatePlotter.py
#_____________________

from ....utils.plotting.defaultTransparency import getTransparencyFunction
from ....utils.plotting.plotting            import makeOutputDirLabelPrefixFigNameList
from .plotFinalStateMultiSim                 import plotFinalStateMultiSim

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
                                   self.config.plotFinalState_plotter,
                                   self.config.plotFinalState_args,
                                   self.config.plotFinalState_argsInit,
                                   self.config.plotFinalState_argsFinal,
                                   self.config.plotFinalState_colorBar,
                                   self.config.plotFinalState_cmapName,
                                   self.config.plotFinalState_timeTextPBar,
                                   self.config.plotFinalState_xLabel,
                                   self.config.plotFinalState_yLabel,
                                   self.config.plotFinalState_cLabel,
                                   self.config.plotFinalState_extendX,
                                   self.config.plotFinalState_extendY,
                                   self.config.plotFinalState_nbrXTicks,
                                   self.config.plotFinalState_nbrYTicks,
                                   self.config.plotFinalState_nbrCTicks,
                                   self.config.plotFinalState_xTicksDecimals,
                                   self.config.plotFinalState_yTicksDecimals,
                                   self.config.plotFinalState_cTicksDecimals,
                                   self.config.plotFinalState_order,
                                   self.config.plotFinalState_extendDirection,
                                   self.config.extensions,
                                   self.config.EPSILON)

#__________________________________________________
