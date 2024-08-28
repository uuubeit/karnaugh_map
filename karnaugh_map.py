from drawing import drawTable

import numpy as np


def replaceFunction(func: str):
    func = func.replace("and", "&").replace("*", "&")
    func = func.replace("or", "|").replace("+", "|")
    func = func.replace("!", "~-").replace("not", "~-")
    return func

def checkLists(lst:list,Dnf:bool):
    flag=False
    for iLst in lst:
        for i in iLst:
            if i == str(int(not Dnf)):
                return False
            if i==str(int(Dnf)):
                flag=True
    return flag

# Поиск и вывод областей
def searchLakune(kTable: np.array, lakuneShape:(), Dnf:bool):
    kTableS=kTable[1:,1:]   #обрезанная карта
    func=''

    if kTableS.shape[0]< lakuneShape[0] or kTableS.shape[1]< lakuneShape[1]:
        return kTableS,func
    
    for x in range(kTableS.shape[0]-lakuneShape[0]+1):
        for y in range(kTableS.shape[1]-lakuneShape[1]+1):

            lakune=[['0' for _ in range(lakuneShape[1])] for _ in range(lakuneShape[0])] 

            for flag in range(2):
                for lx in range(lakuneShape[0]):
                    for ly in range(lakuneShape[1]):
                        lakune[lx][ly]=kTableS[x+lx if not flag else x-lx][y+ly  if not flag else y-ly] #заполнение лакуны

                if checkLists(lakune,Dnf):
                    kVar = sorted(set(v for v in kTable[0][0] if v.isalpha()))

                    dictKVarY = [[v,0] for v in kVar[len(kVar)//2:]]
                    dictKVarX = [[v,0] for v in kVar[:len(kVar)//2]]
                    for ix in range(len(dictKVarX)): dictKVarX[ix][1]=(kTable[x+1][0])[ix]
                    for iy in range(len(dictKVarY)): dictKVarY[iy][1]=(kTable[0][y+1])[iy]

                    #заполнение области '2'
                    for lx in range(lakuneShape[0]):
                        for ix in range(len(dictKVarX)): 
                            # проверка на изменения переменных x
                            if dictKVarX[ix][1] != (kTable[1:][x+lx if not flag else x-lx][0])[ix]:
                                dictKVarX[ix][1]='2'

                        for ly in range(lakuneShape[1]):
                            for iy in range(len(dictKVarY)): 
                                # проверка на изменения переменных н
                                if dictKVarY[iy][1] != (kTable[:,1:][0][y+ly if not flag else y-ly])[iy]:
                                    dictKVarY[iy][1]='2'
                            kTableS[x+lx if not flag else x-lx][y+ly  if not flag else y-ly]='2'

                    #выведение формулы
                    for ix in range(len(dictKVarX)): 
                        if dictKVarX[ix][1] != '2':
                            if Dnf:
                                func+=('*' if dictKVarX[ix][1]=='1' else '*!')+dictKVarX[ix][0]
                            else:
                                func+=('+' if dictKVarX[ix][1]=='1' else '+!')+dictKVarX[ix][0]
                    for iy in range(len(dictKVarY)): 
                        if dictKVarY[iy][1] != '2':
                            if Dnf:
                                func+=('*' if dictKVarY[iy][1]=='1' else '*!')+dictKVarY[iy][0]
                            else:
                                func+=('+' if dictKVarY[iy][1]=='1' else '+!')+dictKVarY[iy][0]

                    return kTableS,func[1:]
    return kTableS,func




# a*b+c*d   a+b*c   (a+ not b+c)*(a+c) 
DNF=False
startFunc = "a*c+b"
line=replaceFunction(input() if not bool(startFunc) else startFunc)
variables = sorted(set(v for v in line if v.isalpha()))
dictVar = {v: False for v in variables}
numberVars = len(variables)
arrValues = np.empty([2**numberVars, numberVars + 1], "uint8")

# ЗАПОЛНЕНИЕ
for x in range(arrValues.shape[0]):
    number = bin(x)[2:]
    number = "0" * (numberVars - len(number)) + number
    for y in range(arrValues.shape[1] - 1):
        arrValues[x][y] = number[y]


# ВЫЧИСЛЕНИЕ
for x in range(arrValues.shape[0]):
    for index in range(numberVars):
        dictVar[variables[index]] = arrValues[x][index]
    arrValues[x][-1] = bool(eval(line, {}, dictVar))


print(drawTable(variables + ["f"], arrValues))

kMap = np.empty([numberVars - (numberVars % 2), numberVars + (numberVars % 2)], "uint8")

# Заполнение КАРНО
for f in range(arrValues.shape[0]):
    x, y = "", ""
    for xVar in range(numberVars // 2):
        x += str(arrValues[f][xVar])
    for yVar in range(numberVars // 2, numberVars):
        y += str(arrValues[f][yVar])
    kMap[int(x, 2)][int(y, 2)] = arrValues[f][-1]


binHeader = np.hstack((
    np.array([f"{''.join(variables[:numberVars//2])}\{''.join(variables[numberVars//2:])}"]), 
    np.array([
        bin(b)[2:].zfill((numberVars + numberVars % 2) // 2)
        for b in range(numberVars + numberVars % 2)])
        ))
binColumn = np.array([[
        bin(b)[2:].zfill((numberVars - numberVars % 2) // 2)
        for b in range(numberVars - numberVars % 2)
    ]])


print(drawTable(binHeader, np.hstack((binColumn.T, kMap))))


newFunc=''
for figure in [(2,4),(4,2),(1,4),(4,1),(2,2),(1,2),(2,1),(1,1)]:
    lakuneFunc=0
    while lakuneFunc!='':
        kMap,lakuneFunc = searchLakune(np.vstack((binHeader,np.hstack((binColumn.T, kMap)))), figure, DNF)
        if DNF:
            newFunc+=('+'+lakuneFunc if lakuneFunc!='' else '')
        else:
            newFunc+=('*'+lakuneFunc if lakuneFunc!='' else '')


print('New function:',newFunc[1:])
