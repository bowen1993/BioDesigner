import os
import django
import sys
import json

pro_dir = os.getcwd()
sys.path.append(pro_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BioDesigner.settings")

from design.models import parts
from design.recommend import predict

numberOfChain = 1

def getChainData():
    partList = list()
    partInList = parts.objects.all()
    for p in partInList:
        subStr = p.deep_u_list
        if not subStr or len(subStr) == 0:
            continue
        if subStr.startswith('_'):
            subStr = subStr[1:]
        if subStr.endswith('_'):
            subStr = subStr[:-1]
        subList = subStr.split('_')
        newSubList = list()
        for s in subList:
            newSubList.append(s.encode())
        partList.append(newSubList)
    return partList

def readA():
    f = open('./tran.json', 'r')
    A = json.loads(f.read())
    return A

def testIndivChainCorrection(chains, A):
    correctCount = 0
    for chain in chains:
        chainCorrect = 0
        for i, p in enumerate(chain):
            partCorrect = 0
            m = len(chain) - (i + 1)
            if m == 0:
                break
            pChains = predict(m, numberOfChain, p, A)


def testWholeChainCorrection(chains, A):
    correctCount = 0
    for chain in chains:
        p1 = chain[0]
        m = len(chain) - 1
        pChains = predict(m, numberOfChain, p1, A)
        flag = False
        for pChain in pChains:
            if len(pChain) == len(chain):
                flag = True
                for i in range(1, len(pChain)):
                    if pChain[i] != chain[i]:
                        flag = False
                        break
        if flag:
            correctCount += 1
            print "Chain %s correct" % chain
    print "Correct count : %d" % correctCount
    print "Total count : %d" % len(chains)
    print "Rate: %f" % float(correctCount) / float(len(chains))      


def mainFunc():
    chainData = getChainData()
    A = readA()
    testWholeChainCorrection(chainData, A)



if __name__ == '__main__':
    django.setup()
    mainFunc()