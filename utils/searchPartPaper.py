import os
import django
import csv
import sys
from BeautifulSoup import BeautifulSoup
import urllib2
import xml.etree.ElementTree as ET
import traceback

pro_dir = os.getcwd()
sys.path.append(pro_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BioDesigner.settings")

from design.models import parts, part_papers, paper

def get_part_paper_ids(keyword):
    baseUrl = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=' + keyword
    req = urllib2.Request(baseUrl)
    response = urllib2.urlopen(req)
    xml_str = response.read()
    #ana xml
    try:
        doc = ET.fromstring(xml_str)
    except:
        traceback.print_exc()
        return []
    id_nodes = doc.findall('IdList/Id')
    result = list()
    for id_node in id_nodes:
        result.append(id_node.text)
    return result

def save_to_db(paper_id_list, part_obj):
    base_paper_url = 'http://www.ncbi.nlm.nih.gov/pubmed/'
    for paper_id in paper_id_list:
        new_paper_obj = paper(paper_id=paper_id)
        new_paper_obj.paper_url = base_paper_url + paper_id + '/'
        try:
            new_paper_obj.save()
        except:
            traceback.print_exc()
            continue
        new_pp_obj = part_papers(paper=new_paper_obj)
        new_pp_obj.part = part_obj
        try:
            new_pp_obj.save()
        except:
            traceback.print_exc()
        print 'part %s with %s saved' % (part_obj.part_name, paper_id)

def main_func():
    part_list = parts.objects.all()
    for part_obj in part_list:
        print 'processing part %s' % part_obj.part_name
        keyword = part_obj.nickname
        if keyword == None or len(keyword) == 0:
            keyword = part_obj.short_desc
        if keyword == None or len(keyword) == 0:
            continue
        paper_id_list = get_part_paper_ids(keyword)
        save_to_db(paper_id_list, part_obj)

if __name__ == '__main__':
    django.setup()
    main_func()