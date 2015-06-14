# -*- coding: cp936 -*-

def analyseData(dataList,dataLength):#nn组合
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
        
def getResult(currentList,dataList):#currentList用户正在操作的List,dataList关联项集列表
    dataLength = 2
    resultList = []
    if len(currentList) == 0:
        return resultList
    if len(currentList) <= dataLength:
        for item in dataList:
            if set(currentList).issubset(item):
                resultList.append(item^set(currentList))
        return resultList
    tempData = analyseData(currentList,dataLength)
    for item in tempData:
        for item2 in dataList:
            if item.issubset(item2):
                if item2 not in resultList:
                    resultList.append(item2^item)
    return resultList

    
