import os
import django
import sys
pro_dir = os.getcwd()
sys.path.append(pro_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BioDesigner.settings")

import fpTree
import igemRecomdData
import apriori

from design.models import team_parts

def getPartData():
    result = list()
    tList = team_parts.objects.all().distinct().values_list('team_id', flat=True)[:100]
    for t in tList:
        pList = team_parts.objects.filter(team_id=t).values_list('part_id', flat=True)
        result.append(pList)
    #for i in result:
        #print i
    return result

if __name__ == '__main__':
    django.setup()
    l,m = apriori.apriori(getPartData())
    print m
    print l
