import os
import django
import sys
import traceback
pro_dir = os.getcwd()
sys.path.append(pro_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BioDesigner.settings")

from system.models import gene
from design.models import parts

def gene_FASTA_file(db_name):
    part_obj_list = parts.objects.all()
    part_fasta_file = open(db_name+'.fsa', 'w')
    for part_obj in part_obj_list:
        print 'processing %s' % part_obj.part_name
        part_id = part_obj.part_id
        sequence = part_obj.sequence
        if sequence == None or len(sequence) == 0:
            continue
        part_fasta_file.write('>%s\n' % part_id)
        sequence = sequence.replace('\n', '')
        sequence = sequence.replace(' ', '')
        for i in range(0, len(sequence), 80):
            part_fasta_file.write('%s\n' % sequence[i:i+80])
    part_fasta_file.flush()
    part_fasta_file.close()



if __name__ == '__main__':
    django.setup()
    gene_FASTA_file('parts')