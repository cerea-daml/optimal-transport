#___________
# plotter.py
#___________

from plotAnalyse.analysePlotter             import AnalysePlotter
from plotFinalState.finalStatePlotter       import FinalStatePlotter
from triplotFinalState.finalStateTriplotter import FinalStateTriplotter

#__________________________________________________

class Plotter:
    
    def __init__(self, config):
        self.analysePlotter       = AnalysePlotter(config)
        self.finalStatePlotter    = FinalStatePlotter(config)
        self.finalStateTriplotter = FinalStateTriplotter(config)

    #_________________________

    def plot(self):
        self.analysePlotter.plot()
        self.finalStatePlotter.plot()
        self.finalStateTriplotter.plot()

#__________________________________________________
