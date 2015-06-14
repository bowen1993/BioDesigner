from accounts.models import User
from design.models import project, functions, tracks, user_project, parts

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
            p['function'] = partInfo.function.function
        except:
            p['function'] = None
        try:
            p['track'] = partInfo.track.track
        except:
            p['track'] = None
        result.append(p)
    return result

def getChain(projectId):
    try:
        projectObj = project.objects.get(id=projectId)
        chainStr = projectObj.chain
        print chainStr
        chain = list();
        if not chainStr:
            return True, chain
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
            chain.append(info)
        return True, chain
    except:
        return False, None
