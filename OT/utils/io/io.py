#__________________________________________________
#__________________________________________________

# Copyrigth 2016 A. Farchi and M. Bocquet
# CEREA, joint laboratory Ecole des Ponts ParisTech and EDF R&D

# Code for the paper: Using the Wasserstein distance to compare fields of pollutants:
# Application to the radionuclide atmospheric dispersion of the Fukushima-Daiichi accident
# by A. Farchi, M. Bocquet, Y. Roustan, A. Mathieu and A. Querel

#__________________________________________________

#__________________________________________________
#######
# io.py
#######

import numpy as np

def extensionOfFile(fileName):
    if not '.' in fileName:
        return None
    else:
        l = fileName.split('.')
        return l[len(l)-1]

def arrayFromFile(fileName):
    if fileName is None or fileName == '':
        return None

    ext = extensionOfFile(fileName)

    try:
        if ext == 'npy':
            return np.load(fileName)
        else:
            return np.fromfile(fileName)
    except:
        return None

def fileNameSuffix(i,iMaxP1):
    nDigit = np.ceil(np.log10(iMaxP1))
    s = str(int(i))
    while len(s) < nDigit:
        s = '0'+s
    return s

def readLines(fileName, strip=True, removeBlancks=True, commentChar='#', includeEmptyLines=False):
    f     = open(fileName, 'r')
    lines = f.readlines()
    f.close()

    filteredLines = []

    for line in lines:
        l = line.replace('\n','')
        if strip:
            l = l.strip()
        if removeBlancks:
            l = l.replace(' ','')
        if commentChar:
            l = l.split(commentChar)[0]
        if l == '' and includeEmptyLines:
            filteredLines.append(l)
        if not l == '':
            filteredLines.append(l)

    return filteredLines
