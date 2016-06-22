import os
import django
import sys
import csv

pro_dir = os.getcwd()
sys.path.append(pro_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BioDesigner.settings")

from design.models import parts

def export_info(res_filename):
    res_csv = csv.writer(open(res_filename, 'w'))
    res_csv.writerow(['id', 'part_name', 'nickname', 'type'])
    all_parts = parts.objects.all()
    for part_obj in all_parts:
        new_line = [part_obj.part_id, part_obj.part_name, part_obj.nickname, part_obj.part_type]
        res_csv.writerow(new_line)
    del res_csv

if __name__ == '__main__':
    django.setup()
    export_info('BioBrick_Names.csv')