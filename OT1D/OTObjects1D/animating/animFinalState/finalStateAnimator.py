#______________________
# finalStateAnimator.py
#______________________

from ....utils.animating.saveAnimation      import makeMovieWriter
from ....utils.animating.saveAnimation      import saveAnimation
from ....utils.plotting.defaultTransparency import getTransparencyFunction
from ....utils.plotting.plotting            import makeOutputDirLabelPrefixFigNameList
from .animFinalStateMultiSim                 import makeAnimFinalStateMultiSim

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

            animation = makeAnimFinalStateMultiSim(outputDirList,
                                                   labelList,
                                                   transparencyFunction,
                                                   self.config.animFinalState_legend,
                                                   self.config.animFinalState_grid,
                                                   self.config.animFinalState_timeTextPBar,
                                                   self.config.animFinalState_xLabel,
                                                   self.config.animFinalState_yLabel,
                                                   self.config.animFinalState_extendX,
                                                   self.config.animFinalState_extendY,
                                                   self.config.animFinalState_nbrXTicks,
                                                   self.config.animFinalState_nbrYTicks,
                                                   self.config.animFinalState_xTicksDecimals,
                                                   self.config.animFinalState_yTicksDecimals,
                                                   self.config.animFinalState_order,
                                                   self.config.animFinalState_extendDirection,
                                                   self.config.funcAnimArgs,
                                                   self.config.EPSILON)

            saveAnimation(animation,
                          self.config.figDir,
                          prefixFigName,
                          self.config.extensions, 
                          MovieWriter)

#__________________________________________________
