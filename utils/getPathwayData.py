import os
import django
import csv
import sys
from BeautifulSoup import BeautifulSoup
import urllib2
import traceback

pro_dir = os.getcwd()
sys.path.append(pro_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BioDesigner.settings")

from system.models import organism, pathway, pathway_compound, compound

def save_organism_info_to_db(info_list):
    new_organism_obj = organism(organism_id=info_list[0])
    new_organism_obj.organism_short = info_list[1]
    new_organism_obj.organism_name = info_list[2]
    try:
        new_organism_obj.save()
    except:
        traceback.print_exc()

def getOrganism():
    baseUrl = 'http://rest.kegg.jp/list/organism'
    req = urllib2.Request(baseUrl)
    response = urllib2.urlopen(req)
    organism_infos = response.read().split('\n')
    for organism_info in organism_infos:
        info_list = organism_info.split('\t')
        print info_list
        print 'organism %s' % info_list[1]
        save_organism_info_to_db(info_list)

def get_compound_infos(compound_id):
    baseUrl = 'http://rest.kegg.jp/get/' + compound_id
    req = urllib2.Request(baseUrl)
    response = urllib2.urlopen(req)
    infolines = response.read().split('\n')
    current_info_type = ''
    compound_info = dict()
    for line in infolines:
        infos = line.split(' ')
        if not line.startswith(' ') and not line.startswith('/'):
            current_info_type = infos[0]
            infos = infos[1:]
        for info_item in infos:
            if info_item.endswith('\n'):
                info_item = info_item[:-1]
            if info_item == 'Compound' and current_info_type == 'ENTRY':
                continue
            try:
                compound_info[current_info_type] += info_item
            except:
                compound_info[current_info_type] = info_item
    try:
        names = compound_info['NAME'].split(';')
        compound_info['NAME'] = names[0]
        compound_info['NICKNAME'] = ''
        for i in range(1, len(names)):
            compound_info['NICKNAME'] += names[i] + '_'
        new_compound = compound(compound_id=compound_info['ENTRY'])
        new_compound.name = compound_info['NAME']
        new_compound.nicknames = compound_info['NICKNAME']
        new_compound.formula = compound_info['FORMULA']
        new_compound.exact_mass = compound_info['EXACT_MASS']
        new_compound.mol_mass = compound_info['MOL_WEIGHT']
        try:
            new_compound.save()
            return new_compound
        except:
            traceback.print_exc()
            print '%s can not be saved' % compound_info['NAME']
            return None
    except:
        pass
        return None

def get_or_create_compound(compound_id):
    try:
        compound_obj = compound.objects.get(compound_id=compound_id)
        return compound_obj
    except:
        return get_compound_infos(compound_id)

def create_pc(compound_list, pathway_obj):
    for compound_id in compound_list:
        compound_obj = get_or_create_compound(compound_id)
        if compound_obj == None:
            return
        new_pc = pathway_compound(compound=compound_obj, pathway=pathway_obj)
        try:
            new_pc.save()
        except:
            traceback.print_exc()

def get_pathway_detail(pathway_id, organism_obj):
    try:
        baseUrl = 'http://rest.kegg.jp/get/' + pathway_id
        req = urllib2.Request(baseUrl)
        response = urllib2.urlopen(req)
        pathways = response.read().split('\n')
        current_info_type = ''
        pathway_dict = dict()
        for info_list in pathways:
            if info_list.startswith('/'):
                continue
            infos = info_list.split(' ')
            if not info_list.startswith(' ') and not info_list.startswith('/'):
                current_info_type =infos[0]
                infos = infos[1:]
                if current_info_type == 'ENTRY':
                    for info_item in infos:
                        if info_item != '' :
                            pathway_dict['ENTRY'] = info_item
                            break
                if current_info_type == 'NAME':
                    for info_item in infos:
                        if info_item != '':
                            pathway_dict['NAME'] = info_item
                            break
                if current_info_type == 'COMPOUND':
                    for info_item in infos:
                        if info_item != '':
                            pathway_dict['COMPOUND'] = list()
                            pathway_dict['COMPOUND'].append(info_item)
                            break
            if current_info_type == 'COMPOUND' and info_list.startswith(' '):
                for info_item in infos:
                    if info_item != '':
                        pathway_dict['COMPOUND'].append(info_item)
                        break
        new_pathway_obj = pathway(pathway_id=pathway_dict['ENTRY'])
        new_pathway_obj.organism = organism_obj
        new_pathway_obj.pathway_name = pathway_dict['NAME']
        try:
            new_pathway_obj.save()
            create_pc(pathway_dict['COMPOUND'], new_pathway_obj)
        except:
            traceback.print_exc()
    except:
        pass

def get_organism_pathways(organism_obj):
    baseUrl = 'http://rest.kegg.jp/list/pathway/' + organism_obj.organism_short
    req = urllib2.Request(baseUrl)
    response = urllib2.urlopen(req)
    pathways = response.read().split('\n')
    for pathway_info in pathways:
        pathway_id = pathway_info.split('\t')[0]
        print 'processing %s' % pathway_id
        get_pathway_detail(pathway_id, organism_obj)

def getPathways():
    organism_list = organism.objects.all()
    for organism_obj in organism_list:
        print 'For organism %s' % organism_obj.organism_short
        get_organism_pathways(organism_obj)
    print 'process ended'


if __name__ == '__main__':
    django.setup()
    getPathways()