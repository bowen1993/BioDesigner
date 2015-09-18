import os
import django
import sys
import traceback
pro_dir = os.getcwd()
sys.path.append(pro_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BioDesigner.settings")

from design.models import parts

if __name__ == '__main__':
    django.setup()
    f = open('ans.txt', 'r')
    for line in f:
        infos = line.split('\t')
        name = infos[0][:-4]
        score = float(infos[1])
        print name
        try:
            part_obj = parts.objects.get(part_name=name)
            if score == 0:
                part_obj.score = 0
            else:
                part_obj.score = float(score / float(part_obj.sequence_length))
                print part_obj.score
            part_obj.save()
        except:
            traceback.print_exc()
            pass
