############
# plotter.py
############

from plotAnalyse.analysePlotter       import AnalysePlotter
from plotFinalState.finalStatePlotter import FinalStatePlotter

class Plotter:
    
    def __init__(self, plottingConfig):
        self.analysePlotter    = AnalysePlotter(plottingConfig)
        self.finalStatePlotter = FinalStatePlotter(plottingConfig)

    def plot(self):
        self.analysePlotter.plot()
        self.finalStatePlotter.plot()
