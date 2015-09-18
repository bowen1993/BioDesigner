import os
import django
import sys
import traceback
from multiprocessing import Pool 

pro_dir = os.getcwd()
sys.path.append(pro_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BioDesigner.settings")

from design.models import parts

basepath = 'part_fsa/'
result_basepath = 'part_gene_result/'

def blast_search(name, filepath):
    out_filename = result_basepath + name + '.out'
    command_str = 'blastn -db nt -query %s -out %s -remote' % (filepath, out_filename)
    os.system(command_str)

def gene_part_fsa(part_obj):
    name = part_obj.part_name
    print 'processing %s' % name
    sequence = part_obj.sequence
    filename = '%s.fsa' % name
    if not os.path.exists(basepath + filename):
        fsa_file = open(basepath + filename, 'w')
        fsa_file.write('>%s\n' % name)
        sequence = sequence.replace('\n', '')
        sequence = sequence.replace(' ', '')
        for i in range(0, len(sequence), 80):
                fsa_file.write('%s\n' % sequence[i:i+80])
        fsa_file.close()
    blast_search(name, basepath + filename)

def search_part_in_gene():
    part_list = parts.objects.all()[:]
    pool = Pool()
    pool.map(gene_part_fsa, part_list)
    pool.close()
    pool.join()

if __name__ == '__main__':
    django.setup()
    search_part_in_gene()

