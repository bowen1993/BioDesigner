from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response, get_list_or_404
from django.template import RequestContext, loader
from version.models import version
from design.models import project
from accounts.models import User
import hashlib
import json
import datetime

# Create your views here.
# get all version of one project
def getVersions(request):
    projectId = int(request.GET.get('project_id'))

    versionsInfo = {
        'versions':[],
        'isSuccessful':True,
    }
    try:
        GVProjectObject = project.objects.get(pk=projectId)
        #versions = get_list_or_404(version,project=projectObject)
        versions = GVProjectObject.version_set.all().order_by('modifyTime')
        index = 0
        for version in versions:
            versionId          = version.version_id
            projectObj          = version.project
            modifyTime          = version.modifyTime
            modifyPerson        = version.modifyPerson
            version_description = version.version_description
            content             = version.content
            contentList = analysisContent(content)
            halfVersionId = cutTheVersionId(versionId)
            versionsInfo['versions'].append({
                'version_id':halfVersionId,
                'project_id':projectObj.id,
                'modifyTime':str(modifyTime),
                'modifyPerson':modifyPerson.username,
                'version_description':version_description,
                'content':contentList,
            })
            index += 1

    except Exception, e:
        versionsInfo['isSuccessful'] = False
    finally:
        return HttpResponse(json.dumps(versionsInfo),content_type="application/json")

# get a version of one project
def getTheVersion(request):
    # the version_id from UI is half of real version_id
    version_id = str(request.GET.get('version_id',''))
    isSuccessful = True
    try:
        #versionObject = get_object_or_404(version,pk__startswith=halfVersionId)
        versionObject = version.objects.get(pk__startswith=version_id)
        versionId           = versionObject.version_id
        projectObj          = versionObject.project
        modifyTime          = versionObject.modifyTime
        modifyPerson        = versionObject.modifyPerson
        version_description = versionObject.version_description
        content             = versionObject.content
        contentList = analysisContent(content)
        versionInfo = {
            'version_id':version_id,
            'project':projectObj.id,
            'modifyTime':str(modifyTime),
            'modifyPerson':modifyPerson.username,
            'version_description':version_description,
            'content':contentList,
            'isSuccessful':isSuccessful,
        }
    except Exception, e:
        isSuccessful = False
        versionInfo = {
            'version_id':version_id,
            'project':"",
            'modifyTime':"",
            'modifyPerson':"",
            'version_description':"",
            'content':[],
            'isSuccessful':isSuccessful,
        }
        print e
    finally:
        return HttpResponse(json.dumps(versionInfo),content_type="application/json")

# create a version for a project
# the project information come from the current project
# user's operate only influence project table
def createVersion(request):
    # para in: project_id and version_description and username
    projectId   =  int(request.GET.get('project_id',''))
    description =  str(request.GET.get('version_description',''))
    userName = request.session['username']
    result = {
        'isSuccessful':True,
    }
    v = version()
    v.version_id = calcVersionId(projectId,description)
    v.version_description = description
    try:
        CVProjectObj = project.objects.get(pk=projectId)
        v.project = CVProjectObj
        chains = CVProjectObj.chain_set.all()
        chainString = chainsToString(chains)
        if (chainString == "" or chainString == None):
            result['isSuccessful'] = False
            return HttpResponse(json.dumps(result),content_type="application/json")
        else:
            v.content = chainString
    except Exception, e:
        result['isSuccessful'] = False
        print e
        return HttpResponse(json.dumps(result),content_type="application/json")
        # modifyPerson
    try:
        userObj = User.objects.get(username=userName)
        v.modifyPerson = userObj
    except Exception, e:
        result['isSuccessful'] = False
        print e
        return HttpResponse(json.dumps(result),content_type="application/json")
   
    v.save()
    return HttpResponse(json.dumps(result),content_type="application/json")

#split the project content
def analysisContent(chainContent):
    chainString = chainContent
    chains = chainString.split(',')
    result = []
    index = 0
    for chain in chains:
        result.append(chain.split('_'))
        index += 1   
    return result
# get half of the original version_id
def cutTheVersionId(version_id):
    return str(version_id)[:32]
# calculate the version_id
def calcVersionId(projectId,description):
    idStr = str(projectId) + description
    if (idStr == '' or idStr == None):
        return ''
    else:
        m = hashlib.md5()
        m.update(idStr)
        result = m.hexdigest()
        return result
# convert chains to a string
def chainsToString(chains):
    chainString = ""
    for chain in chains:
        chainString += str(chain.sequence)
        chainString += ","
    length = len(chainString)
    chainString = chainString[:length-1]
    return chainString

