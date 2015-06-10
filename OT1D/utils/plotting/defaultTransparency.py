#_______________________
# defaultTransparency.py
#_______________________

#__________________________________________________

def getTransparencyFunction(name):

    def defaultTransparency(t):
        return t

    #_________________________
    
    def fastVanishingTransparency(t):
        if t < 0.6:
            return 0.0
        else:
            return 1. + ( 1.0 / 0.4 ) * ( t - 1.0 )

    #_________________________
        
    def customTransparency(t):
        return min(max(t, 0.25), 0.8)

    #_________________________

    if name == 'fastVanishingTransparency':
        return fastVanishingTransparency
    elif name == 'customTransparency':
        return customTransparency
    else:
        return defaultTransparency

#__________________________________________________
