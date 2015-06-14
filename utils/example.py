import os
import django
import sys

pro_dir = os.getcwd()
sys.path.append(pro_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BioDesigner.settings")

import fpTree
import igemRecomdData

from design.models import team_parts

def getPartData():
    result = list()
    tList = team_parts.objects.all().distinct().values_list('team_id', flat=True)[:200]
    for t in tList:
        pList = team_parts.objects.filter(team_id=t).values_list('part_id', flat=True)
        result.append(pList)
    for r in result:
        print r
    return result


def finallyResult(currentList,simpDat):
    data= fpTree.createInitSet(simpDat)
    myFPtree,myHeaderTab = fpTree.createTree(data,2)
    freqItems = []
    fpTree.mineTree(myFPtree,myHeaderTab,2,set([]),freqItems)
    result = []
    temp = igemRecomdData.getResult(currentList,freqItems)
    for item in temp:
        t = list(item)
        if (len(t) > 0):
            for item2 in t:
                if (item2 not in result):
                    result.append(item2)
    return result
    
    
if __name__ == '__main__':
    django.setup()
    cList = [16990]
    r = finallyResult(cList,getPartData())
    print len(r)
    for i in r:
        print i
