import os
import django
import sys
pro_dir = os.getcwd()
sys.path.append(pro_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BioDesigner.settings")

from design.models import team_parts

def getPartData():
    result = list()
    tList = team_parts.objects.all().distinct().values_list('team_id', flat=True)[:]
    for t in tList:
        pList = team_parts.objects.filter(team_id=t).values_list('part_id', flat=True)
        result.append(pList)
    for row in result:
        for item in row:
            print item,
        print ''

if __name__ == '__main__':
    django.setup()
    getPartData()