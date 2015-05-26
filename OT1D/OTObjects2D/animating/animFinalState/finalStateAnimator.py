#######################
# finalStateAnimator.py
#######################

from ....utils.plotting.defaultTransparency import defaultTransparency
from ....utils.plotting.defaultTransparency import fastVanishingTransparency
from ....utils.plotting.defaultTransparency import customTransparency

from ....utils.animating.saveAnimation      import makeMovieWriter
from ....utils.animating.saveAnimation      import saveAnimation

from animFinalState         import makeAnimFinalState
from animFinalStateMultiSim import makeAnimFinalStateMultiSim

class FinalStateAnimator:

    def __init__(self, animatingConfig):
        self.animatingConfig = animatingConfig

    def animate(self):
        if not self.animatingConfig.animFinalState == 1:
            return

        MovieWriter = makeMovieWriter(self.animatingConfig.writerName, self.animatingConfig.writerFPS, self.animatingConfig.writerCodec, 
                                      self.animatingConfig.writerBitrate, self.animatingConfig.writerExtraArgs)

        if self.animatingConfig.transparencyFunctionName == 'defaultTransparency':
            transparencyFunction = defaultTransparency
        elif self.animatingConfig.transparencyFunctionName == 'fastVanishingTransparency':
            transparencyFunction = fastVanishingTransparency
        elif self.animatingConfig.transparencyFunctionName == 'customTransparency':
            transparencyFunction = customTransparency

        if self.animatingConfig.singleOrMulti == 0:
            animation = makeAnimFinalState(self.animatingConfig.outputDir[0], self.animatingConfig.label[0], transparencyFunction, 
                                           self.animatingConfig.funcAnimArgs, self.animatingConfig.animFinalStatePlotter,
                                           self.animatingConfig.animFinalStateArgs, self.animatingConfig.animFinalStateArgsInit, 
                                           self.animatingConfig.animFinalStateArgsFinal, self.animatingConfig.EPSILON)

        elif self.plottingConfig.singleOrMulti == 1:
            animation = makeAnimFinalStateMultiSim(self.animatingConfig.outputDirList, self.animatingConfig.labelsList, transparencyFunction, 
                                                   self.animatingConfig.funcAnimArgs, self.animatingConfig.animFinalStatePlotter,
                                                   self.animatingConfig.animFinalStateArgs, self.animatingConfig.animFinalStateArgsInit,
                                                   self.animatingConfig.animFinalStateArgsFinal, self.animatingConfig.EPSILON):

        saveAnimation(animation, self.animatingConfig.figDir, self.animatingConfig.prefixFigNameFinalState, 
                      self.animatingConfig.extensionsList, MovieWriter)
