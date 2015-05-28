#######################
# finalStateAnimator.py
#######################

from ....utils.plotting.defaultTransparency import defaultTransparency
from ....utils.plotting.defaultTransparency import fastVanishingTransparency
from ....utils.plotting.defaultTransparency import customTransparency

from ....utils.animating.saveAnimation      import makeMovieWriter
from ....utils.animating.saveAnimation      import saveAnimation

from animFinalStateMultiSim                 import makeAnimFinalStateMultiSim

class FinalStateAnimator:

    def __init__(self, animatingConfig):
        self.animatingConfig = animatingConfig

    def animate(self):
        if not self.animatingConfig.animFinalState == 1:
            return

        MovieWriter = makeMovieWriter(self.animatingConfig.writerName,
                                      self.animatingConfig.writerFPS,
                                      self.animatingConfig.writerCodec, 
                                      self.animatingConfig.writerBitrate, 
                                      self.animatingConfig.writerExtraArgs)

        if self.animatingConfig.animFinalState_transparencyFunction == 'defaultTransparency':
            transparencyFunction = defaultTransparency
        elif self.animatingConfig.animFinalState_transparencyFunction == 'fastVanishingTransparency':
            transparencyFunction = fastVanishingTransparency
        elif self.animatingConfig.animFinalState_transparencyFunction == 'customTransparency':
            transparencyFunction = customTransparency

        if self.animatingConfig.singleOrMulti == 0:
            outputDirList = [self.animatingConfig.outputDir[0]]
            labelList     = [self.animatingConfig.label[0]]
        elif self.animatingConfig.singleOrMulti == 1:
            outputDirList = self.animatingConfig.outputDir
            labelList     = self.animatingConfig.label

        animation = makeAnimFinalStateMultiSim(outputDirList,
                                               labelList,
                                               transparencyFunction,
                                               self.animatingConfig.animFinalState_legend,
                                               self.animatingConfig.animFinalState_grid,
                                               self.animatingConfig.animFinalState_timeTextPBar,
                                               self.animatingConfig.animFinalState_xLabel,
                                               self.animatingConfig.animFinalState_yLabel,
                                               self.animatingConfig.animFinalState_extendX,
                                               self.animatingConfig.animFinalState_extendY,
                                               self.animatingConfig.animFinalState_nbrXTicks,
                                               self.animatingConfig.animFinalState_nbrYTicks,
                                               self.animatingConfig.animFinalState_xTicksDecimals,
                                               self.animatingConfig.animFinalState_yTicksDecimals,
                                               self.animatingConfig.animFinalState_order,
                                               self.animatingConfig.animFinalState_extendDirection,
                                               self.animatingConfig.funcAnimArgs,
                                               self.animatingConfig.EPSILON)

        saveAnimation(animation,
                      self.animatingConfig.figDir,
                      self.animatingConfig.animFinalState_prefixFigName,
                      self.animatingConfig.extension, 
                      MovieWriter)
