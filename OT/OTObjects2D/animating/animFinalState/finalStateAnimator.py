#==================================================
#__________________________________________________

# Copyrigth 2016 A. Farchi and M. Bocquet
# CEREA, joint laboratory Ecole des Ponts ParisTech and EDF R&D

# Code for the paper: Using the Wasserstein distance to compare fields of pollutants:
# Application to the radionuclide atmospheric dispersion of the Fukushima-Daiichi accident
# by A. Farchi, M. Bocquet, Y. Roustan, A. Mathieu and A. Querel

#__________________________________________________
#==================================================

#______________________
# finalStateAnimator.py
#______________________

from ....utils.plotting.defaultTransparency import getTransparencyFunction
from ....utils.plotting.plotting            import makeOutputDirLabelPrefixFigNameList
from ....utils.animating.saveAnimation      import makeMovieWriter
from ....utils.animating.saveAnimation      import saveAnimation
from animFinalStateMultiSim                 import makeAnimFinalStateMultiSim

#__________________________________________________

class FinalStateAnimator:

    def __init__(self, config):
        self.config = config

    #_________________________

    def animate(self):
        if not self.config.animFinalState:
            return

        MovieWriter = makeMovieWriter(self.config.writerName, 
                                      self.config.writerFPS,
                                      self.config.writerCodec, 
                                      self.config.writerBitrate, 
                                      self.config.writerExtraArgs)

        transparencyFunction = getTransparencyFunction(self.config.animFinalState_transparencyFunction)

        ( outputDirListList,
          labelListList,
          prefixFigNameList) = makeOutputDirLabelPrefixFigNameList(self.config.singleOrMulti,
                                                                   self.config.outputDirList,
                                                                   self.config.labelList,
                                                                   self.config.animFinalState_prefixFigName)

        for (outputDirList,
             labelList,
             prefixFigName) in zip(outputDirListList,
                                   labelListList,
                                   prefixFigNameList):
        
            animation = makeAnimFinalStateMultiSim(self.config.funcAnimArgs,
                                                   outputDirList,
                                                   self.config.figDir,
                                                   labelList,
                                                   transparencyFunction,
                                                   self.config.animFinalState_plotter,
                                                   self.config.animFinalState_args,
                                                   self.config.animFinalState_argsInit,
                                                   self.config.animFinalState_argsFinal,
                                                   self.config.animFinalState_colorBar,
                                                   self.config.animFinalState_cmapName,
                                                   self.config.animFinalState_timeTextPBar,
                                                   self.config.animFinalState_xLabel,
                                                   self.config.animFinalState_yLabel,
                                                   self.config.animFinalState_cLabel,
                                                   self.config.animFinalState_extendX,
                                                   self.config.animFinalState_extendY,
                                                   self.config.animFinalState_nbrXTicks,
                                                   self.config.animFinalState_nbrYTicks,
                                                   self.config.animFinalState_nbrCTicks,
                                                   self.config.animFinalState_xTicksDecimals,
                                                   self.config.animFinalState_yTicksDecimals,
                                                   self.config.animFinalState_cTicksDecimals,
                                                   self.config.animFinalState_order,
                                                   self.config.animFinalState_extendDirection,
                                                   self.config.EPSILON)

            saveAnimation(animation, 
                          self.config.figDir, 
                          prefixFigName, 
                          self.config.extensions, 
                          MovieWriter)

#__________________________________________________
