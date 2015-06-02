###################
# analysePlotter.py
###################

from definePlotSubplots  import defaultPlotSubplots
from definePlotSubplots  import customPlotSubplots

from plotAnalyseMultiSim import plotAnalyseMultiSim

class AnalysePlotter:

    def __init__(self, plottingConfig):
        self.plottingConfig = plottingConfig

    def plot(self):
        if self.plottingConfig.plotAnalyse:
            return

        if self.plottingConfig.plotAnalyse_plotSubplotsFunction == 'customPlotSubplots':
            plotSubplotsFunction = customPlotSubplots
        elif self.plottingConfig.plotAnalyse_plotSubplotsFunction == 'defaultPlotSubplots':
            plotSubplotsFunction = defaultPlotSubplots

        plotSubplots = plotSubplotsFunction(self.plottingConfig.plotAnalyse_plotSubplots_iterOrTime,
                                            self.plottingConfig.plotAnalyse_plotSubplots_xScale,
                                            self.plottingConfig.plotAnalyse_plotSubplots_yScale,
                                            self.plottingConfig.plotAnalyse_plotSubplots_grid)

        
        if self.plottingConfig.singleOrMulti == 0:
            outputDirList = [self.plottingConfig.outputDir[0]]
            labelList     = [self.plottingConfig.label[0]]
        elif self.plottingConfig.singleOrMulti == 1:
            outputDirList = self.plottingConfig.outputDir
            labelList     = self.plottingConfig.label

        plotAnalyseMultiSim(outputDirList,
                            self.plottingConfig.figDir,
                            self.plottingConfig.plotAnalyse_prefixFigName, 
                            labelList,
                            plotSubplots,
                            self.plottingConfig.extension)
