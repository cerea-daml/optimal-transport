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
