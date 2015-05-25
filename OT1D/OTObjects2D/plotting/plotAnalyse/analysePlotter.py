###################
# analysePlotter.py
###################

from definePlotSubplots  import defaultPlotSubplots
from definePlotSubplots  import customPlotSubplots

from plotAnalyse         import plotAnalyse
from plotAnalyseMultiSim import plotAnalyseMultiSim

class AnalysePlotter:

    def __init__(self, plottingConfig):
        self.plottingConfig = plottingConfig

    def plot(self):
        if not self.plottingConfig.plotAnalyse == 1:
            return

        if self.plottingConfig.plotSubplotsFunctionName == 'customPlotSubplots':
            plotSubplotsFunction = customPlotSubplots
        elif self.plottingConfig.plotSubplotsFunctionName == 'defaultPlotSubplots':
            plotSubplotsFunction = defaultPlotSubplots

        plotSubplots = plotSubplotsFunction(**self.plottingConfig.plotSubplotsFunctionArgs)

        if self.plottingConfig.singleOrMulti == 0:
            plotAnalyse(self.plottingConfig.outputDir[0], self.plottingConfig.figDir, self.plottingConfig.prefixFigNameAnalyse, 
                        plotSubplots, self.plottingConfig.extension)

        elif self.plottingConfig.singleOrMulti == 1:
            plotAnalyseMultiSim(self.plottingConfig.outputDir, self.plottingConfig.figDir, self.plottingConfig.prefixFigNameAnalyse, 
                                self.plottingConfig.label, plotSubplots, self.plottingConfig.extension)
