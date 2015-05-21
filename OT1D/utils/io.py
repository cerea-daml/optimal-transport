#######
# io.py
#######

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
