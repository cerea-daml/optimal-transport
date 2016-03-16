#==================================================
#__________________________________________________

# Copyrigth 2016 A. Farchi and M. Bocquet
# CEREA, joint laboratory Ecole des Ponts ParisTech and EDF R&D

# Code for the paper: Using the Wasserstein distance to compare fields of pollutants:
# Application to the radionuclide atmospheric dispersion of the Fukushima-Daiichi accident
# by A. Farchi, M. Bocquet, Y. Roustan, A. Mathieu and A. Querel

#__________________________________________________
#==================================================

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
