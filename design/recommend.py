"""
implement recommend for parts

@author: Bowen, Ray, Yu
"""

from design.models import parts, team_parts, teams
from elasticsearch import Elasticsearch
from operator import itemgetter
import json
import os.path
import pickle

from design.search_part import get_func_parts

BASE = os.path.dirname(os.path.abspath(__file__))

def getApriorRecommend(chainStr, funcStr=None):
    """
    get recommendations with aprior algorithm

    @param chainStr: part chain
    @type chainStr: str
    @return : recommendations
    @rytpe: dict
    """
    dataList = chainStr.split('_')
    #dataList = dataList[len(dataList)-2:len(dataList)]
    fList = list()
    with open(BASE+'/../freq.txt', 'rb') as f:
        fList = pickle.load(f)
    strResult = getResult(dataList, fList, funcStr)
    recommend_list = list()
    for partId in strResult:
        partObj = parts.objects.get(part_id=int(partId))
        partInfo = {
            'part_id': partObj.part_id,
            'part_name': partObj.part_name,
            'part_type': partObj.part_type,
        }
        recommend_list.append(partInfo)
    result = {
        'isSuccessful' : True,
        'recommend_list': recommend_list,
    }
    return result

def analyseData(dataList,dataLength = 2):
    tempData = []
    tempData1 = []
    tempData2 = []
    for item in dataList:
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
        
def getResult(currentList,dataList, funcStr):#currentList ,dataList pin fan xiang ji
    dataList = toFrozenset(dataList)
    dataLength = len(currentList)
    max_length = 4
    resultList = []
    if dataLength == 0:
        return resultList
    if dataLength > max_length:
        currentList = currentList[dataLength-4:]
        dataLength = 4
    while dataLength > 0:
        for item in dataList:
            for item1 in item:
                if frozenset(currentList).issubset(item1):
                    if (item1^frozenset(currentList)) not in resultList:
                        resultList.append(item1^frozenset(currentList))
        if len(resultList) >= 5:
            break
        currentList = currentList[1:]
        dataLength = dataLength - 1
    resultList = toBeOne(resultList)
    result_part_count = len(resultList)
    dictionary_result = {}
    for each_part in range(result_part_count):
        dictionary_result[resultList[each_part]] = 100 - (100 * each_part) / result_part_count
    if funcStr != None and funcStr != '':
        adjuct_to_func(funcStr, dictionary_result)
    final_result = list()
    for part_pair in sorted(dictionary_result.items(), key=itemgetter(1), reverse=True):
        final_result.append(part_pair[0])
    return final_result

def adjuct_to_func(funcStr, dictionary_result):
    if funcStr.startswith('_'):
        funcStr = funcStr[1:]
    if funcStr.endswith('_'):
        funcStr = funcStr[:-1]
    func_part_list = get_func_parts(funcStr.split('_'))
    for key in dictionary_result:
        if long(key) in func_part_list:
            dictionary_result[key] += 10


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

def getBetweenMarkovRecommend(part_id):
    """
    get recommendations with Markov algorithm

    @param part_id: part id
    @type part_id: str
    @return : recommendations
    @rytpe: dict
    """
    result = {
        'isSuccessful' : True,
    }
    predictChains = predict(1, 5, part_id, loadA())
    if not predictChains:
        result['isSuccessful'] = False
        return result
    chains = list()
    for predictChain in predictChains:
        chain = list()
        for part in predictChain:
            infos = getPartNameAndType(part)
            if not infos[0]:
                break
            item = {
                'part_id':part,
                'part_name': infos[0],
                'part_type' : infos[1]
            }
            chain.append(item)
        chains.append(chain)
    result['recommend_list'] = chains
    return result

def getMarkovRecommend(part_id):
    """
    get recommendations with Markov algorithm

    @param part_id: part id
    @type part_id: str
    @return : recommendations
    @rytpe: dict
    """
    result = {
        'isSuccessful' : True,
    }
    predictChains = predict(4, 5, part_id, loadA())
    if not predictChains:
        result['isSuccessful'] = False
        return result
    chains = list()
    for predictChain in predictChains:
        chain = list()
        for part in predictChain:
            infos = getPartNameAndType(part)
            if not infos[0]:
                break
            item = {
                'part_id':part,
                'part_name': infos[0],
                'part_type' : infos[1]
            }
            chain.append(item)
        chains.append(chain)
    result['recommend_list'] = chains
    return result

def loadA():
    tranFile = open(BASE+'/../tran.json', 'r')
    A = json.loads(tranFile.read())
    return A

def getPartNameAndType(part_id):
    try:
        partObj = parts.objects.get(part_id=int(part_id))
        return partObj.part_name, partObj.part_type
    except:
        return None, None

def get_chain(elem, num, process):
    """get chain which had predicted

    according to information in process,
    get the chain from first element to elem variable
    and save the chain in a list

    args:
        elem: the last element in chain 
        num: the line number in process 
        process: a variable record the predict process
    return:
        a chain from first to elem variable 
    """
    last_elem = process[num][elem][1]
    if last_elem is None:
        return [elem]
    else:
        chain = get_chain(last_elem, num-1, process)
        chain.append(elem)
        return chain



def predict(m, count, s, A):
    """predict the chain after s

    calculate the probability of a m-length chain,
    then return chains.
    CAUTION the number of chains maybe less then count

    args:
        m: the length of predict chain
        count: the number of predict chain
        s: the last element of the current chain
        A: transition matrix
    return:
        some chains save in list
    """
    process = []
    start = {}
    start[s] = [1, None]
    process.append(start)

    for i in range(m):
        line = process[-1]
        next_line = {}
        for key in line.keys():
            if A.get(key, None) is None:
                continue
            for k in A[key].keys():
                p = next_line.get(k, [0, None])[0]
                if p < A[key][k] * line[key][0]:
                    next_line[k] = [A[key][k] * line[key][0], key]
        process.append(next_line)

    ans = process[-1]
    # sort according to probability from high to low
    ans = sorted(ans.iteritems(), key=lambda item: item[1][0], reverse=True)
    
    if len(ans) == 0:
        return None     # Can't predict, because of no answer can be find
    else:
        count = min(len(ans), count) # the number of ans maybe less than count
        chains = []
        length = len(process)
        for i in range(count):
            elem = ans[i][0]
            chain = get_chain(elem, length-1, process)
            chains.append(chain[1:])
        return chains