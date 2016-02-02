#____________
# animator.py
#____________

from .animFinalState.finalStateAnimator import FinalStateAnimator

#__________________________________________________

class Animator:
    
    def __init__(self, animatingConfig):
        self.finalStateAnimator = FinalStateAnimator(animatingConfig)

    #_________________________

    def animate(self):
        self.finalStateAnimator.animate()

#__________________________________________________
