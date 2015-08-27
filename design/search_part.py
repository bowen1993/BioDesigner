from elasticsearch import Elasticsearch
from design.models import parts, teams, team_parts

def getPart(partName):
    try:
        partObj = parts.objects.get(part_name=partName)
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
                'part_url' : partObj.part_url
            }
    except:
        result = {
            'isSuccessful': False
        }
    return result

def ambiguousSearch(keyword, funcs):
    es = Elasticsearch()
    result = format_fuzzy_result(sort_result(fuzzy_search_parts(es, keyword), funcs))
    return result

def fuzzy_search_parts(es, keyword):
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

def exact_search_part(es, partName):
    query_body = {
            "from": 0,
            "size": 1,
            "query":{
                "match":{
                    "part_name": partName
                }
            }
    }
    result = es.search(index="biodesigners", doc_type="part", body=query_body)
    return result

def format_fuzzy_result(hits):
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

def format_exact_result(es_res):
    part_result = es_res['hits']['hits']
    result = dict()
    if len(part_result) != 0:
        part_id = part_result[0]["_source"]["part_id"]
        partObj = parts.objects.get(part_id=part_id)
        result = {
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
            'creation_date': partObj.creation_date,
            'm_datetime': partObj.m_datetime,
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
            'part_url' : partObj.part_url
        }
    return result

