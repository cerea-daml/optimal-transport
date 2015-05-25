#############
# animator.py
#############

from animFinalState.finalStateAnimator import FinalStateAnimator

class Animator:
    
    def __init__(self, animatingConfig):
        self.finalStateAnimator = FinalStateAnimator(animatingConfig)

    def animate(self):
        self.finalStateAnimator.animate()
