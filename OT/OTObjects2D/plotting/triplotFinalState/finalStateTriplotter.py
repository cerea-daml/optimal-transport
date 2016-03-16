#==================================================
#__________________________________________________

# Copyrigth 2016 A. Farchi and M. Bocquet
# CEREA, joint laboratory Ecole des Ponts ParisTech and EDF R&D

# Code for the paper: Using the Wasserstein distance to compare fields of pollutants:
# Application to the radionuclide atmospheric dispersion of the Fukushima-Daiichi accident
# by A. Farchi, M. Bocquet, Y. Roustan, A. Mathieu and A. Querel

#__________________________________________________
#==================================================

#________________________
# finalStateTriplotter.py
#________________________

from ....utils.plotting.plotting            import makeOutputDirLabelPrefixFigNameList
from .triplotFinalStateMultiSim              import triplotFinalStateMultiSim

#__________________________________________________

class FinalStateTriplotter:

    def __init__(self, config):
        self.config = config

    #_________________________

    def plot(self):
        if not self.config.triplotFinalState:
            return

        ( outputDirListList, 
          labelListList, 
          prefixFigNameList) = makeOutputDirLabelPrefixFigNameList(self.config.singleOrMulti,
                                                                   self.config.outputDirList,
                                                                   self.config.labelList,
                                                                   self.config.triplotFinalState_prefixFigName)

        for (outputDirList, 
             labelList, 
             prefixFigName) in zip(outputDirListList,
                                   labelListList, 
                                   prefixFigNameList):

            triplotFinalStateMultiSim(outputDirList,
                                      self.config.figDir,
                                      prefixFigName,
                                      labelList,
                                      self.config.triplotFinalState_plotter,
                                      self.config.triplotFinalState_args,
                                      self.config.triplotFinalState_colorBar,
                                      self.config.triplotFinalState_cmapName,
                                      self.config.triplotFinalState_timeTextPBar,
                                      self.config.triplotFinalState_xLabel,
                                      self.config.triplotFinalState_yLabel,
                                      self.config.triplotFinalState_cLabel,
                                      self.config.triplotFinalState_extendX,
                                      self.config.triplotFinalState_extendY,
                                      self.config.triplotFinalState_nbrXTicks,
                                      self.config.triplotFinalState_nbrYTicks,
                                      self.config.triplotFinalState_nbrCTicks,
                                      self.config.triplotFinalState_xTicksDecimals,
                                      self.config.triplotFinalState_yTicksDecimals,
                                      self.config.triplotFinalState_cTicksDecimals,
                                      self.config.triplotFinalState_order,
                                      self.config.triplotFinalState_extendDirection,
                                      self.config.triplotFinalState_extendDirectionTriplot,
                                      self.config.extensions,
                                      self.config.EPSILON)

#__________________________________________________
