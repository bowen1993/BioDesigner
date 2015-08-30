import os
import django
import sys
import traceback
import urllib2
import json
pro_dir = os.getcwd()
sys.path.append(pro_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BioDesigner.settings")

from system.models import part_gene, gene
from design.models import parts
from system.gene import get_or_create_gene

def extract_info(line):
    xm_id = line.split('|')[1]
    score = ''
    index = 70
    while line[index] != ' ':
        score += line[index]
        index += 1
    return xm_id, float(score)

def search_in_ncbi(xm_id):
    print xm_id
    baseGeneFindUrl = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=nuccore&retmode=json&term='
    try:
        req = urllib2.Request(baseGeneFindUrl + xm_id)
        response = urllib2.urlopen(req)
        resStr = response.read()
    except:
        traceback.print_exc()
        return None
    if len(resStr) == 0:
        return None
    result = json.loads(resStr)
    geneIdList = result['esearchresult']['idlist']
    return geneIdList[0]

def get_gene_obj(xm_id):
    gene_id = search_in_ncbi(xm_id)
    if gene_id == None:
        return None
    return get_or_create_gene(gene_id)

def save_info_to_db(part_name, info_list):
    part_obj = None
    try:
        part_obj = parts.objects.get(part_name=part_name)
    except:
        traceback.print_exc()
        return
    if part_obj == None:
        return
    high_score = info_list[0][1]
    part_obj.score = high_score
    for item in info_list:
        gene_obj = get_gene_obj(item[0])
        if gene_obj == None:
            continue
        new_part_gene_obj = part_gene(part=part_obj)
        new_part_gene_obj.gene = gene_obj
        new_part_gene_obj.score = item[1]
        try:
            new_part_gene_obj.save()
        except:
            traceback.print_exc()
            pass

def ana_result_file(filename):
    result_file = open(filename, 'r')
    part_name = ''
    try:
        part_name = os.path.split(filename)[1].split('.')[0]
    except:
        traceback.print_exc()
        return
    print part_name
    info_list = list()
    for i, line in enumerate(result_file):
        if i == 21 and "No" in line:
            continue
        if i >= 22:
            if line.startswith(' ') or len(line) == 0 or line == None or line.startswith('\n'):
                break
            else:
                info_list.append(extract_info(line))
    info_list = sorted(info_list, key=lambda item: item[1], reverse=True)
    save_info_to_db(part_name, info_list)


if __name__ == '__main__':
    django.setup()
    ana_result_file('BBa_I5200.out')