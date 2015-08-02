# -*- coding: cp936 -*-

def analyseData(dataList,dataLength = 2):#nncombination,parameter 1 is the currentList,The result contents of set
    tempData = []
    tempData1 = []#保存一项集
    tempData2 = []#保存多项集
    for item in dataList:#转换为单项列表
            tempData.append(item)
            tempData1.append(tempData)
            tempData = []
    tempData1 = map(set,tempData1)
    tempData2 = tempData1
    for i in range(dataLength - 1):
        for item in tempData1:
            for j in range(len(tempData2)):
                if (item.union(tempData2[j]) not in tempData):
                    tempData.append(item.union(tempData2[j]))
        tempData2 = tempData
        tempData = []
    flag = False
    
    for item in tempData2:
        if len(item) < dataLength:
            tempData2.remove(item)
            flag = True
    while (flag == True):
        flag = False
        for item in tempData2:
            if len(item) < dataLength:
                tempData2.remove(item)
                flag = True
    return tempData2
        
def getResult(currentList,datalist):#currentList ,dataList pin fan xiang ji
    dataList = toFrozenset(datalist)
    dataLength = 2
    resultList = []
    if len(currentList) == 0:
        return resultList
    if len(currentList) <= dataLength:
        for item in dataList:
            for item1 in item:
                if frozenset(currentList).issubset(item1):
                   resultList.append(item1^frozenset(currentList))
        resultList = toBeOne(resultList)
        return resultList
    tempData = analyseData(currentList,dataLength)
    for item in tempData:
        for item2 in dataList:
            if item.issubset(item2):
                if item2 not in resultList:
                    resultList.append(item2^item)
    resultList = toBeOne(resultList)
    return resultList

def toBeOne(data):#delete chong fu xiang
    result = []
    for item in data:
        t = list(item)
        for item2 in t:
            if item2 not in result:
                result.append(item2)
    return result
def toFrozenset(data):
    result = []
    for item in data:
        temp = []
        for i in item:
            temp.append(frozenset(i))
        result.append(temp)
    return result
    
