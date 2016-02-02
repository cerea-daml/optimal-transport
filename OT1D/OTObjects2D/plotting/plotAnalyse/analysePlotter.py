#__________________
# analysePlotter.py
#__________________

from .definePlotSubplots          import definePlotSubplots
from .plotAnalyseMultiSim         import plotAnalyseMultiSim
from ....utils.plotting.plotting import makeOutputDirLabelPrefixFigNameList

#__________________________________________________

class AnalysePlotter:

    def __init__(self, config):
        self.config = config

    #_________________________

    def plot(self):
        if not self.config.plotAnalyse:
            return

        plotSubplots = definePlotSubplots(self.config.plotAnalyse_plotSubplotsFunction,
                                          self.config.plotAnalyse_plotSubplots_iterOrTime,
                                          self.config.plotAnalyse_plotSubplots_xScale,
                                          self.config.plotAnalyse_plotSubplots_yScale,
                                          self.config.plotAnalyse_plotSubplots_grid)


        ( outputDirListList,
          labelListList,
          prefixFigNameList) = makeOutputDirLabelPrefixFigNameList(self.config.singleOrMulti,
                                                                   self.config.outputDirList,
                                                                   self.config.labelList,
                                                                   self.config.plotAnalyse_prefixFigName)


        for (outputDirList,
             labelList,
             prefixFigName) in zip(outputDirListList,
                                   labelListList,
                                   prefixFigNameList):

            plotAnalyseMultiSim(outputDirList,
                                self.config.figDir,
                                prefixFigName, 
                                labelList,
                                plotSubplots,
                                self.config.extensions)

#__________________________________________________
