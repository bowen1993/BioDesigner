import urllib2
import os.path

baseGetUrl = 'http://rest.kegg.jp/get/'
baseGeneFindUrl = 'http://rest.kegg.jp/find/genes/'


def getInfoFile(id, t):
    filepath = 'datas/%s_%s' % (id, t)
    if os.path.exists(filepath):
        return
    newFile = open(filepath, 'w')
    try:
        req = urllib2.Request(baseGetUrl + id)
        response = urllib2.urlopen(req)
        newFile.write(response.read())
    except:
        print '%s failed' % id
        pass
    finally:
        newFile.close()

def getGeneByCompounds(cList):
    for cn in cList:
        try:
            req = urllib2.Request(baseGeneFindUrl + cn)
            response = urllib2.urlopen(req)
            resStr = response.read()
        except:
            pass
        geneList = resStr.split('\n')
        geneIdList = list()
        for g in geneList:
            gene_id = g.split('\t')[0]
            if gene_id.endswith('\n'):
                gene_id = gene_id[:-1]
            geneIdList.append(gene_id)
        for gid in geneIdList:
            print 'geting %s' % gid
            getInfoFile(gid, 'Gene')

def getReactionData(cId_list):
    for cid in cId_list:
        filepath = 'datas/compound/%s_Compound'  % cid
        f = open(filepath, 'r')
        isReaction = False
        for l in f.readlines():
            if l.startswith('/'):
                continue
            if not l.startswith(' '):
                if l.startswith('REACTION'):
                    isReaction = True
            if isReaction:
                rList = l.split(' ')
                for item in rList:
                    if item == None or item == '' or item == 'REACTION':
                        continue
                    print item
                    getInfoFile(item, 'Reaction')

def getCompounds(id_file):
    f = open(id_file, 'r')
    cId_list = list()
    cName_list = list()
    print 'geting compound data'
    for l in f.readlines():
        c_id = l.split('\t')[0]
        c_name = l.split('\t')[1].split(';')[0]
        if c_name.endswith('\n'):
            c_name = c_name[:-1]
        #print c_name
        cId_list.append(c_id)
        cName_list.append(c_name)
        print 'geting data for %s ' % c_id
        getInfoFile(c_id, 'Compound')
    print 'compound process ended'
    print 'geting gene data'
    #getGeneByCompounds(cName_list)
    print 'gene data ended'
    print 'geting reaction data'
    #getReactionData(cId_list)
    print 'reaction data ended'

if __name__ == '__main__':
    getCompounds('compound.1')
