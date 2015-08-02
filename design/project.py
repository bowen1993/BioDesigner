from accounts.models import User
from design.models import project, functions, tracks, user_project, parts, chain
import sys, traceback

def searchProject(keyword, userObj):
    result={
        'isSuccessful' : False
    }
    projectList = project.objects.filter(project_name__contains=keyword, creator=userObj, is_deleted=False)
    result['projects'] = formatProjectList(projectList)
    result['isSuccessful'] = True
    return result

def getUserProject(userObj):
    result = {
            'isSuccessful' : False
        }
    projectList = project.objects.filter(creator=userObj, is_deleted=False)
    result['projects'] = formatProjectList(projectList)
    result['isSuccessful'] = True
    return result

def formatProjectList(projectList):
    result = list()
    for proInfo in projectList:
        p = {
            'id' : proInfo.id,
            'name' : proInfo.project_name,
            'creator' : proInfo.creator.username,
        }
        try:
            p['function'] = proInfo.function.function
        except:
            p['function'] = None
        try:
            p['track'] = proInfo.track.track
        except:
            p['track'] = None
        result.append(p)
    return result

def getChainList(projectId):
    result = list()

    chainObjs = chain.objects.filter(project_id=projectId)
    for chainObj in chainObjs:
        c = {
            'id' : chainObj.id,
            'name' : chainObj.name,
        }
        result.append(c)

    return result

def getChain(chainId):
    try:
        chainObj = chain.objects.get(id=chainId)
        chainStr = chainObj.sequence
        #print chainStr
        chains = list()
        if not chainStr:
            return True, chains
        if chainStr.startswith('_'):
            chainStr = chainStr[1:]
        if chainStr.endswith('_'):
            chainStr = chainStr[:-1]
        chainList = chainStr.split('_')
        for partId in chainList:
            partObj = parts.objects.get(part_id=partId)
            info = {
                'part_id' : partId,
                'part_name' : partObj.part_name,
                'part_type' : partObj.part_type
            }
            chains.append(info)
        return True, chains
    except:
        return False, None
