#__________________________________________________
#__________________________________________________

# Copyrigth 2016 A. Farchi and M. Bocquet
# CEREA, joint laboratory Ecole des Ponts ParisTech and EDF R&D

# Code for the paper: Using the Wasserstein distance to compare fields of pollutants:
# Application to the radionuclide atmospheric dispersion of the Fukushima-Daiichi accident
# by A. Farchi, M. Bocquet, Y. Roustan, A. Mathieu and A. Querel

#__________________________________________________

#__________________________________________________
#___________
# saveFig.py
#___________

#__________________________________________________

def saveFig(plt, figName, extensionsList):
    for ext in extensionsList:
        try:
            print('Writing '+figName+ext+' ...')
            plt.savefig(figName+ext)
        except:
            print('Could not write file '+figName+ext+' ...')

#__________________________________________________
