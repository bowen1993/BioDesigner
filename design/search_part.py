"""
search_part.py realize the part search

@author: Bowen
"""

from elasticsearch import Elasticsearch
from design.models import parts, teams, team_parts, part_papers, paper
import traceback

def getPart(partName):
    """
    find the part with part name

    @param partName: name of a part
    @type partName: str
    @return : part information
    @rtype: dict
    """
    try:
        partObj = parts.objects.get(part_name=partName)
        papers = part_papers.objects.filter(part=partObj)
        result = {
                'isSuccessful': True,
                'isEmpty': False,
                'part_id': partObj.part_id,
                'ok': partObj.ok,
                'part_name': partObj.part_name,
                'nickname' : partObj.nickname,
                'short_desc': partObj.short_desc,
                'description': partObj.description,
                'part_type': partObj.part_type,
                'author': partObj.author,
                'status': partObj.status,
                'dominant': partObj.dominant,
                'discontinued': partObj.discontinued,
                'part_status': partObj.part_status,
                'sample_status': partObj.sample_status,
                'p_status_cache': partObj.p_status_cache,
                's_status_cache': partObj.s_status_cache,
                'in_stock': partObj.in_stock,
                'results': partObj.results,
                'favorite': partObj.favorite,
                'ps_string': partObj.ps_string,
                'scars' : partObj.scars,
                'barcode' : partObj.barcode,
                'notes' : partObj.notes,
                'source' : partObj.source,
                'premium' : partObj.premium,
                'categories' : partObj.categories,
                'sequence' : partObj.sequence,
                'sequence_length' : partObj.sequence_length,
                'part_url' : partObj.part_url,
                'score' : str(partObj.score)
            }
        paper_list = list()
        for paper in papers:
            paper_info = {
                'name': paper.paper.paper_name,
                'url' : paper.paper.paper_url
            }
            paper_list.append(paper_info)
        result['paper'] = paper_list
    except:
        traceback.print_exc()
        result = {
            'isSuccessful': False
        }
    return result

def ambiguousSearch(keyword, funcs):
    """
    ambiguous search parts with the keyword, and adjust result with the functions

    @param keyword: search keyword
    @type keyword: str
    @param funcs: functions
    @type: str
    @return: search result
    @rtype: list
    """
    es = Elasticsearch()
    result = format_fuzzy_result(sort_result(fuzzy_search_parts(es, keyword), funcs))
    return result

def fuzzy_search_parts(es, keyword):
    """
    fuzzy search part with elasticsearch

    @param es: elasticsearch object
    @type es: Elasticsearch
    @param keyword: search keyword
    @type keyword: str
    @return: elasticsearch search result
    @rtype: dict
    """
    query_body = {
        "from" : 0,
        "size" : 80,
        "query" : {
            "fuzzy_like_this" : {
                "fields" : ["part_name", "part_type", "short_desc"],
                "like_text" : keyword,
                "max_query_terms" : 80
            }
        }
    }
    result = es.search(index="biodesigners", doc_type="parts", body=query_body)
    return result

def get_func_parts(func_list):
    """
    get parts related to functions

    @param func_list: functions
    @type func_list: list
    @return : parts related to functions
    @rtype: list
    """
    part_list = list()
    for func_id in func_list:
        team_list = teams.objects.filter(function_id=func_id)
        for team_obj in team_list:
            part_list.extend(team_parts.objects.filter(team=team_obj))
    result = list()
    for part_obj in part_list:
        result.append(part_obj.part_id)
    return result


def sort_result(es_result, funcs):
    """
    sort result according to the functions

    @param funcs: functions
    @type funcs : list
    @return : sorted result
    @rtype: list
    """
    if funcs == None:
        func_parts = list()
    else:
        if funcs.endswith('_'):
            funcs = funcs[:-1]
        if funcs.startswith('_'):
            funcs = funcs[1:]
        func_parts = get_func_parts(funcs.split('_'))
    hits = es_result['hits']['hits']
    for item in hits:
        if item['_source']['part_id'] in func_parts:
            item['_score'] += 1.5
    hits = sorted(hits, key = lambda x:x['_score'], reverse = True)
    return hits[:40]

def format_fuzzy_result(hits):
    """
    format search result

    @param hits: searched parts
    @type hists: list
    @return part informaions
    @rtype: list
    """
    part_list = list()
    for item in hits:
        info = item['_source']
        part_info = {
            'part_name' : info['part_name'],
            'part_id' : info['part_id'],
            'part_type' : info['part_type'],
        }
        part_list.append(part_info)
    return part_list
