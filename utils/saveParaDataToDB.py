import os
import django
import sys
import csv

pro_dir = os.getcwd()
sys.path.append(pro_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BioDesigner.settings")

from design.models import parts, part_parameters

def readDataToDB(csv_reader):
    count = 0
    for row in csv_reader:
        try:
            partObj = parts.objects.get(part_name=row[0])
        except:
            print '%s not exists' % row[0]
            continue
        name = row[1]
        value = row[2]
        newPaObj = part_parameters(part=partObj, name=name, value=value)
        newPaObj.save()
        count += 1
        print count

if __name__ == '__main__':
    django.setup()
    csv_reader = csv.reader(open('paraData6.csv', 'r'))
    readDataToDB(csv_reader)