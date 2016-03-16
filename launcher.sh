#__________________________________________________
#__________________________________________________

# Copyrigth 2016 A. Farchi and M. Bocquet
# CEREA, joint laboratory Ecole des Ponts ParisTech and EDF R&D

# Code for the paper: Using the Wasserstein distance to compare fields of pollutants:
# Application to the radionuclide atmospheric dispersion of the Fukushima-Daiichi accident
# by A. Farchi, M. Bocquet, Y. Roustan, A. Mathieu and A. Querel

#__________________________________________________

#__________________________________________________
#!/bin/bash                                                                                                                                               

launcher='/Users/Alban/Desktop/Optimal-Transport/launchSimulation1D.py'

configDir=''
configSubDir=$configDir''
configFile=$configSubDir'.cfg'

logFile=''

printIO='True'

$launcher CONFIG_FILE=$configFile PRINT_IO=$printIO > $logFile