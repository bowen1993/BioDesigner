# markov algorithm
import os
import django
import sys
from elasticsearch import Elasticsearch

pro_dir = os.getcwd()
sys.path.append(pro_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BioDesigner.settings")

from design.models import parts

def cal_probability(data_set):
    '''calculate transition matrix

    calculate the probability of going from state i to state j in 1 time step

    args:
        data_set: datas use to calculate transition matrix, type is list
    return:
        a directory, record probability in transition matrix
    '''
    A = {}
    total = {}
    for data in data_set:
        count = len(data)
        for i in range(count-1):
            A[data[i]] = A.get(data[i], {})
            A[data[i]][data[i+1]] = A[data[i]].get(data[i+1], 0) + 1
            total[data[i]] = total.get(data[i], 0) + 1

    for key, value in A.items():
        for k in value.keys():
            A[key][k] = float(A[key][k])/total[key]
    return A


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
                
def getDataSet():
    partList = list()
    partInList = parts.objects.all()
    for p in partInList:
        subStr = p.deep_u_list
        if not subStr or len(subStr) == 0:
            continue
        if subStr.startswith('_'):
            subStr = subStr[1:]
        if subStr.endswith('_'):
            subStr = subStr[:-1]
        subList = subStr.split('_')
        newSubList = list()
        for s in subList:
            newSubList.append(s.encode())
        partList.append(newSubList)
    return partList
    
def saveTransToES(A):
    es = Elasticsearch()
    for key in A:
        print 'Adding %s' % key
        itemBody = dict()
        itemBody['main_id'] = key
        itemBody['probabilities'] = A[key]
        res = es.index(index="biodesigners", doc_type="transition", body=itemBody)
        if not res['created']:
            print "part %s error" % key

if __name__ == "__main__":
    django.setup()
    data_set = getDataSet()
    A = cal_probability(data_set)
    #saveTransToES(A)
    print A
    #chains = predict(3, 1, '29339', A)  #only two chains can be find
    #if chains is None:
    #    print 'No answer!'
    #else:
    #    for chain in chains:
    #        for elem in chain:
    #            print elem,
    #        print
    
            
        
