#__________________________________________________
#__________________________________________________

# Copyrigth 2016 A. Farchi and M. Bocquet
# CEREA, joint laboratory Ecole des Ponts ParisTech and EDF R&D

# Code for the paper: Using the Wasserstein distance to compare fields of pollutants:
# Application to the radionuclide atmospheric dispersion of the Fukushima-Daiichi accident
# by A. Farchi, M. Bocquet, Y. Roustan, A. Mathieu and A. Querel

#__________________________________________________

#__________________________________________________
#_________________________
# finalStateTrianimator.py
#_________________________

from ....utils.plotting.plotting       import makeOutputDirLabelPrefixFigNameList
from ....utils.animating.saveAnimation import makeMovieWriter
from ....utils.animating.saveAnimation import saveAnimation
from trianimFinalStateMultiSim         import makeTrianimFinalStateMultiSim

#__________________________________________________

class FinalStateTrianimator:

    def __init__(self, config):
        self.config = config

    #_________________________

    def animate(self):
        if not self.config.trianimFinalState:
            return

        MovieWriter = makeMovieWriter(self.config.writerName, 
                                      self.config.writerFPS,
                                      self.config.writerCodec, 
                                      self.config.writerBitrate, 
                                      self.config.writerExtraArgs)

        ( outputDirListList,
          labelListList,
          prefixFigNameList) = makeOutputDirLabelPrefixFigNameList(self.config.singleOrMulti,
                                                                   self.config.outputDirList,
                                                                   self.config.labelList,
                                                                   self.config.trianimFinalState_prefixFigName)

        for (outputDirList,
             labelList,
             prefixFigName) in zip(outputDirListList,
                                   labelListList,
                                   prefixFigNameList):
        
            animation = makeTrianimFinalStateMultiSim(self.config.funcAnimArgs,
                                                      outputDirList,
                                                      self.config.figDir,
                                                      labelList,
                                                      self.config.trianimFinalState_plotter,
                                                      self.config.trianimFinalState_args,
                                                      self.config.trianimFinalState_colorBar,
                                                      self.config.trianimFinalState_cmapName,
                                                      self.config.trianimFinalState_timeTextPBar,
                                                      self.config.trianimFinalState_xLabel,
                                                      self.config.trianimFinalState_yLabel,
                                                      self.config.trianimFinalState_cLabel,
                                                      self.config.trianimFinalState_extendX,
                                                      self.config.trianimFinalState_extendY,
                                                      self.config.trianimFinalState_nbrXTicks,
                                                      self.config.trianimFinalState_nbrYTicks,
                                                      self.config.trianimFinalState_nbrCTicks,
                                                      self.config.trianimFinalState_xTicksDecimals,
                                                      self.config.trianimFinalState_yTicksDecimals,
                                                      self.config.trianimFinalState_cTicksDecimals,
                                                      self.config.trianimFinalState_order,
                                                      self.config.trianimFinalState_extendDirection,
                                                      self.config.trianimFinalState_extendDirectionTrianim,
                                                      self.config.EPSILON)

            saveAnimation(animation, 
                          self.config.figDir, 
                          prefixFigName, 
                          self.config.extensions, 
                          MovieWriter)

#__________________________________________________
