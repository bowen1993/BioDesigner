import os
import django
import sys
import xml.sax
import datetime
from elasticsearch import Elasticsearch

pro_dir = os.getcwd()
sys.path.append(pro_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BioDesigner.settings")

from design.models import parts

id = 1

def mainFunc():
    es = Elasticsearch()
    start_pos = 0
    step = 100
    end_pos = start_pos + step
    total = parts.objects.count()
    print 'process started'
    while total > 0:
        parts_list = parts.objects.all()[start_pos:end_pos]
        start_pos += step
        end_pos += step
        total -= step
        saveInfoToES(es, parts_list)
    print 'process end'

def saveInfoToES(es, parts_list):
    global id
    for part_info in parts_list:
        print 'processing part %s' % part_info.part_name
        part_boby = {
            "part_id" : part_info.part_id,
            "part_name" : part_info.part_name,
            "part_type" : part_info.part_type,
            "short_desc" : part_info.short_desc,
            "sequence": part_info.sequence
        }
        res = es.index(index="biodesigners", doc_type="parts", body=part_boby)
        id += 1
        if not res['created']:
            print "part %s error" % part_info.part_name


if __name__ == '__main__':
    django.setup()
    mainFunc()
