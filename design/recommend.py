from design.models import parts, team_parts, teams
from elasticsearch import Elasticsearch
import json

def getApriorRecommend():
    result = {
        'isSuccessful' : True,
        'recommend_list': [
            {'part_id':98, 'part_name':'BBa_M39201', 'part_type':'T7'},
            {'part_id':144, 'part_name':'BBa_B0011', 'part_type':'T7'},
            {'part_id':145, 'part_name':'BBa_B0012', 'part_type':'T7'},
            {'part_id':146, 'part_name':'BBa_B0013', 'part_type':'T7'},
            {'part_id':147, 'part_name':'BBa_B0030', 'part_type':'T7'},
        ]
    }
    return result

def getMarkovRecommend(part_id):
    result = {
        'isSuccessful' : True,
    }
    predictChains = predict(4, 1, part_id, loadA())
    if not predictChains:
        result['isSuccessful'] = False
        return result
    chains = list()
    for predictChain in predictChains:
        chain = list()
        for part in predictChain:
            infos = getPartNameAndType(part)
            if not infos[0]:
                break
            item = {
                'part_id':part,
                'part_name': infos[0],
                'part_type' : infos[1]
            }
            chain.append(item)
        chains.append(chain)
    result['recommend_list'] = chains
    return result

def loadA():
    tranFile = open('tran.json', 'r')
    A = json.loads(tranFile.read())
    return A

def getPartNameAndType(part_id):
    try:
        partObj = parts.objects.get(part_id=int(part_id))
        return partObj.part_name, partObj.part_type
    except:
        return None, None

def get_chain(elem, num, process):
    """get chain which had predicted

    according to information in process,
    get the chain from first element to elem variable
    and save the chain in a list

    args:
        elem: the last element in chain 
        num: the line number in process 
        process: a variable record the predict process
    return:
        a chain from first to elem variable 
    """
    last_elem = process[num][elem][1]
    if last_elem is None:
        return [elem]
    else:
        chain = get_chain(last_elem, num-1, process)
        chain.append(elem)
        return chain


def predict(m, count, s, A):
    """predict the chain after s

    calculate the probability of a m-length chain,
    then return chains.
    CAUTION the number of chains maybe less then count

    args:
        m: the length of predict chain
        count: the number of predict chain
        s: the last element of the current chain
        A: transition matrix
    return:
        some chains save in list
    """
    process = []
    start = {}
    start[s] = [1, None]
    process.append(start)

    for i in range(m):
        line = process[-1]
        next_line = {}
        for key in line.keys():
            if A.get(key, None) is None:
                continue
            for k in A[key].keys():
                p = next_line.get(k, [0, None])[0]
                if p < A[key][k] * line[key][0]:
                    next_line[k] = [A[key][k] * line[key][0], key]
        process.append(next_line)

    ans = process[-1]
    # sort according to probability from high to low
    ans = sorted(ans.iteritems(), key=lambda item: item[1][0], reverse=True)

    if len(ans) == 0:
        return None     # Can't predict, because of no answer can be find
    else:
        count = min(len(ans), count) # the number of ans maybe less than count
        chains = []
        length = len(process)
        for i in range(count):
            elem = ans[i][0]
            chain = get_chain(elem, length-1, process)
            chains.append(chain[1:])
        return chains