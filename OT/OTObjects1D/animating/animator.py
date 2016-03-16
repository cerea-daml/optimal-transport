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

from animFinalState.finalStateAnimator import FinalStateAnimator

#__________________________________________________

class Animator:
    
    def __init__(self, animatingConfig):
        self.finalStateAnimator = FinalStateAnimator(animatingConfig)

    #_________________________

    def animate(self):
        self.finalStateAnimator.animate()

#__________________________________________________
