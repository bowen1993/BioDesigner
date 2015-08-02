import os
import django
import sys
import pickle

pro_dir = os.getcwd()
sys.path.append(pro_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BioDesigner.settings")

from design.models import teams, team_parts, parts
from igemRecomdData import getResult

def loadDataSet():
    dataList = list()
    allTeam = teams.objects.all()
    for t in allTeam:
        team_list = list()
        p_list = team_parts.objects.filter(team_id=t.team_id)
        if len(p_list) == 0:
            continue
        for p in p_list:
            team_list.append(str(p.part_id))
        dataList.append(team_list)
    allParts = parts.objects.all()
    for po in allParts:
        se = po.deep_u_list
        if se == None or se == "":
            continue
        if se.startswith('_'):
            se = se[1:]
        if se.endswith('_'):
            se = se[:-1]
        dataList.append(se.split('_'))
    return dataList

def createC1(dataSet):
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])
    C1.sort()
    return map(frozenset,C1)

def scanD(D,Ck,minSupport):
    ssCnt = {}
    for tid in D:
        for can in Ck:
            if can.issubset(tid):
                if not ssCnt.has_key(can):ssCnt[can] = 1
                else:ssCnt[can] += 1
    numItems = float(len(D))
    retList = []
    #supportData = {}
    for key in ssCnt:
        support = ssCnt[key]/numItems
        if support >= minSupport:
            retList.insert(0,key)
        #supportData[key] = support
    return retList#,supportData

def aprioriGen(Lk,k):
    retList = []
    lenLk = len(Lk);
    for i in range(lenLk):
        for j in range(i+1,lenLk):
            L1 = list(Lk[i])[:k-2];L2 = list(Lk[j])[:k-2]
            L1.sort();L2.sort()
            if L1==L2:
                retList.append(Lk[i] | Lk[j])
    return retList

def apriori(dataSet,minSupport = 0.003):
    C1 = createC1(dataSet)
    D = map(set,dataSet)
    L1 = scanD(D,C1,minSupport)
    L = [L1]
    k = 2
    while (len(L[k-2]) > 0 and (k-1) < 3):#parameter 2 controls the number of xiangji,and there is 3
        Ck = aprioriGen(L[k-2],k)
        Lk = scanD(D,Ck,minSupport)
        #supportData.update(supk)
        L.append(Lk)
        k += 1
    return toList(L)#,supportData

def generateRules(L,supportData,minConf = 0.1):
    bigRuleList = []
    for i in range(1,len(L)):
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]
            if (i > 1):
                ruleFromConseq(freqSet,H1,supportData,bigRuleList,minConf)
            else:
                calcConf(freqSet,H1,supportData,bigRuleList,minConf)
    return bigRuleList

def calcConf(freqSet,H,supportData,brl,minConf = 0.1):
    prunedH = []
    for conseq in H:
        conf = supportData[freqSet]/supportData[freqSet-conseq]
        if conf >= minConf:
            print freqSet-conseq,'-->',conseq,'conf:',conf
            brl.append((freqSet-conseq,conseq,conf))
            prunedH.append(conseq)
    return prunedH

def ruleFromConseq(freqSet,H,supportData,brl,minConf = 0.1):
    m = len(H[0])
    if (len(freqSet) > (m + 1)):
        Hmpl = aprioriGen(H,m + 1)
        Hmpl = calcConf(freqSet,Hmpl,supportData,brl,minConf)
        if (len(Hmpl) > 1):
            rulesFromConseq(freqSet,Hmpl,supportData,brl,minConf)

def toList(data):
    result = []
    for item in data:
        temp = []
        for i in item:
            temp.append(list(i))
        result.append(temp)
    return result

def mainFunc():
    django.setup()
    fList = list()
    with open('freq.txt', 'rb') as f:
        fList = pickle.load(f)
    print 'recommending'
    print getResult(['162', '151'], fList)

if __name__ =='__main__':
    mainFunc()
