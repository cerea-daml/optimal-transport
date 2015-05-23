############
# plotter.py
############

from plotAnalyse.analysePlotter import AnalysePlotter

class Plotter:
    
    def __init__(self, plottingConfig):
        self.analysePlotter = AnalysePlotter(plottingConfig)

    def plot(self):
        self.analysePlotter.plot()
