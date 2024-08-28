import numpy as np

def drawTable(arrName:list, arrValue):
    outputString = '┌'

    if len(arrName) != arrValue.shape[1]:
        return 'the size of the names does not match the size of the array of values'

    lenArrName = []
    for y in range(arrValue.shape[1]):
        lenght = len(str(arrName[y]))
        for x in range(arrValue.shape[0]):
            lenght = lenght if (a := len(str(arrValue[x][y]))) < lenght else a
        lenArrName.append(lenght)


    # drawing headlines
    for itemLen in lenArrName:
        outputString += '─' * (itemLen + 1) + '─┬'
    outputString = outputString[:-1] + '┐\n│'

    for nameIndex in range(len(arrName)):
        space = (lenArrName[nameIndex] + 2 - len(str(arrName[nameIndex]))) // 2
        outputString += ' ' * (space 
                               if (lenArrName[nameIndex] - len(str(arrName[nameIndex]))) % 2 == 0 else 
                               space + 1) + str(arrName[nameIndex]) + ' ' * space + '│'

    outputString += '\n├'

    for itemLen in lenArrName:
        outputString += '─' * (itemLen + 1) + '─┼'
    outputString = outputString[:-1] + '┤\n│'


    # filling in the table
    for x in range(arrValue.shape[0]):
        for y in range(arrValue.shape[1]):
            item=arrValue[x][y]
            space = (lenArrName[y] + 2 - len(str(item))) // 2
            outputString+= ' ' * (space 
                               if (lenArrName[y] - len(str(item))) % 2 == 0 else 
                               space + 1) + str(item) + ' ' * space + '│'
        outputString+='\n│'


    # drawing footer
    outputString=outputString[:-1]+'└'
    for itemLen in lenArrName:
        outputString += '─' * (itemLen + 1) + '─┴'
    outputString = outputString[:-1] + '┘'

        
    return outputString