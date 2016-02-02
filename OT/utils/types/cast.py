#________
# cast.py
#________

#__________________________________________________

def castString(toType, s):
    if toType == 'str':
        return s
    elif toType == 'float':
        return float(s)
    elif toType == 'int':
        return int(s)
    elif toType == 'bool':
        return ( s == 'True' )

#__________________________________________________
