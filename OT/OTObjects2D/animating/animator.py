#==================================================
#__________________________________________________

# Copyrigth 2016 A. Farchi and M. Bocquet
# CEREA, joint laboratory Ecole des Ponts ParisTech and EDF R&D

# Code for the paper: Using the Wasserstein distance to compare fields of pollutants:
# Application to the radionuclide atmospheric dispersion of the Fukushima-Daiichi accident
# by A. Farchi, M. Bocquet, Y. Roustan, A. Mathieu and A. Querel

#__________________________________________________
#==================================================

#____________
# animator.py
#____________

from .animFinalState.finalStateAnimator       import FinalStateAnimator
from .trianimFinalState.finalStateTrianimator import FinalStateTrianimator 

#__________________________________________________

class Animator:
    
    def __init__(self, config):
        self.finalStateAnimator    = FinalStateAnimator(config)
        self.finalStateTrianimator = FinalStateTrianimator(config)

    #_________________________

    def animate(self):
        self.finalStateAnimator.animate()
        self.finalStateTrianimator.animate()

#__________________________________________________
