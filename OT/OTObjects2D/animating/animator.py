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
