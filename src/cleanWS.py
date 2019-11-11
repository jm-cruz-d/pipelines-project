
def subChar(DF, column, old, new):
    DF[column] = DF[column].str.replace(old, new)
    return DF

def changeType(DF, column, types):
    DF[column] = DF[column].astype(types)
    return DF

def combCol(DF, nameNew, column1, column2):
    DF[nameNew] = DF[column1]+DF[column2]
    return DF