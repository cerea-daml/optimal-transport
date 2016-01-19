#!/bin/bash                                                                                                                                               

launcher='/Users/Alban/Desktop/Optimal-Transport/launchSimulation1D.py'

configDir=''
configSubDir=$configDir''
configFile=$configSubDir'.cfg'

logFile=''

printIO='True'

$launcher CONFIG_FILE=$configFile PRINT_IO=$printIO > $logFile