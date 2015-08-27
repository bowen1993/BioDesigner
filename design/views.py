from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response
from django.template import RequestContext, loader
from django.core.mail import send_mail
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import hashlib
import json
import datetime
import random
import traceback
from search_part import ambiguousSearch, getPart
from accounts.models import User
from design.models import project, functions, tracks, user_project, tracks, chain, track_functions
from design.project import searchProject, getUserProject, getChain, getChainList
from design.recommend import getApriorRecommend, getMarkovRecommend
from design.file import getSequenceResultImage

@csrf_exempt
def searchParts(request):
    keyword = request.GET.get('keyword')
    try:
        funcs = request.GET.get('funcs')
    except:
        funcs = ''
    results = ambiguousSearch(keyword, funcs)
    return HttpResponse(json.dumps(results), content_type="text/json")

@csrf_exempt
def getParts(request):
    partName = request.GET.get('partname')
    results = getPart(partName)
    return HttpResponse(json.dumps(results), content_type="text/json")

@csrf_exempt
def dashboardView(request):
    try:
        isLoggedIn = request.session['isLoggedIn']
        if isLoggedIn:
            chainId = int(request.GET.get('id'))
            template = loader.get_template('home/dashboard.html')
            context = RequestContext(request, {
                'username':str(request.session['username']),
                'id' : chainId
                })
            return HttpResponse(template.render(context))
        else:
            return HttpResponseRedirect('/')
    except KeyError:
        return HttpResponseRedirect('/')

@csrf_exempt
def projectView(request):
    try:
        isLoggedIn = request.session['isLoggedIn']
        if isLoggedIn:
            template = loader.get_template('home/project.html')
            context = RequestContext(request, {
                'username':request.session['username']
                })
            return HttpResponse(template.render(context))
        else:
            return HttpResponseRedirect('/')
    except KeyError:
        return HttpResponseRedirect('/')

def isAccountActive(request):
    try:
        username = request.session['username']
        return User.objects.get(username=username).is_confirmed
    except KeyError:
        return False

def isLoggedIn(request):
    try:
        isLoggedIn = request.session['isLoggedIn']
        return isLoggedIn
    except KeyError:
        return False

def getCurrentUserObj(request):
    try:
        username = request.session['username']
        userObj = User.objects.get(username=username)
        return userObj
    except:
        return None

def newProject(name, user, track):
    try:
        projectObj = project(project_name=name, creator=user, track_id=track)
        projectObj.save()
        userPjctObj = user_project(user=user, project=projectObj)
        userPjctObj.save()
        return True, projectObj
    except:
        return False, null

@csrf_exempt
def createProject(request):
    result = {
        'isSuccessful': False,
    }
    if not isLoggedIn(request):
        return HttpResponse(json.dumps(result), content_type="application/json")
    name = request.POST.get('name', '')
    userObj = getCurrentUserObj(request)
    #function_id = int(request.POST.get('function', ''))
    track_id = int(request.POST.get('track', ''))
    createResult = newProject(name, userObj, track_id)
    result['isSuccessful'] = createResult[0]
    result['project_name'] = name
    result['id'] = createResult[1].id
    result['track'] = createResult[1].track.track
    result['creator'] = userObj.username
    return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def getProjectChain(request):
    result = {
        'isSuccessful' : False,
    }
    if not isLoggedIn(request):
        return HttpResponse(json.dumps(result), content_type="application/json")
    project_id = request.GET.get('id', '')
    chainResult = getChain(project_id)
    result['isSuccessful'] = chainResult[0]
    result['chain'] = chainResult[1]
    return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def getProject(request):
    keyword = request.GET.get('keyword')
    userObj = getCurrentUserObj(request)
    if not userObj:
        result = {'isSuccessful' : False}
        return HttpResponse(json.dumps(result), content_type="application/json")
    result = searchProject(keyword, userObj)
    return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def getUserProjects(request):
    userObj = getCurrentUserObj(request)
    if not userObj:
        result = {'isSuccessful' : False}
        return HttpResponse(json.dumps(result), content_type="application/json")
    result = getUserProject(userObj)
    return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def getProjectChains(request):
    projectId = request.GET.get('id','')
    result = getChainList(int(projectId))
    return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def createNewDevice(request):
    result = {
        'isSuccessful': False,
    }
    if not isLoggedIn(request):
        return HttpResponse(json.dumps(result), content_type="application/json")
    name = request.POST.get('name', '')
    projectId = request.POST.get('id', '')
    newChain = chain(name=name, project_id=int(projectId))
    try:
        newChain.save()
        result['isSuccessful'] = True
        result['name'] = name
        result['id'] = projectId
    except:
        pass
    return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def saveChain(request):
    result = {'isSuccessful':True,}
    chainContent = request.POST.get('chain','')
    chainId = int(request.POST.get('id',''))
    try:
        chainObj = chain.objects.get(id=chainId)
        chainObj.sequence = chainContent
        chainObj.isModified = True
        chainObj.save()
    except:
        result['isSuccessful'] = False

    return HttpResponse(json.dumps(result),content_type="application/json")

@csrf_exempt
def getARecommend(request):
    chainStr = request.GET.get('seq', '')
    if chainStr.startswith('_'):
        chainStr = chainStr[1:]
    if chainStr.endswith('_'):
        chainStr = chainStr[:-1]
    getApriorRecommend(chainStr)
    return HttpResponse(json.dumps(getApriorRecommend(chainStr)), content_type="application/json")

@csrf_exempt
def getMRecommend(request):
    part_id = request.GET.get('part')
    return HttpResponse(json.dumps(getMarkovRecommend(part_id)), content_type="application/json")

@csrf_exempt
def getTracks(request):
    trackList = tracks.objects.all().order_by('id');
    result = {
        'isSuccessful' : False,
    }
    trackInfos = list()
    for t in trackList:
        tmp = {
            'id' : t.id,
            'track' : t.track
        }
        trackInfos.append(tmp)
    result['isSuccessful'] = True
    result['tracks'] = trackInfos
    return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def getChainLength(request):
    chainId = request.GET.get('id')
    result = {
        'isSuccessful' : True,
    }
    try:
        chainObj = chain.objects.get(id=chainId)
        se = chainObj.sequence
        if se.startswith('_'):
            se = se[1:]
        chainLength = len(se.split('_'))
        result['length'] = chainLength
    except:
        result['isSuccessful'] = False
    return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def changeProjectName(request):
    projectId = request.POST.get('id','')
    newName = request.POST.get('name','')
    result = {
        'isSuccessful': True,
    }
    try:
        projectObj = project.objects.get(id=projectId)
        projectObj.project_name = newName
        projectObj.save()
    except:
        result['isSuccessful'] = False
    return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def changeProjectTrack(request):
    projectId = request.POST.get('id', '')
    newTrackId = request.POST.get('track_id', '')
    result = {
        'isSuccessful': True,
    }
    try:
        projectObj = project.objects.get(id=projectId)
        trackObj = tracks.objects.get(id=newTrackId)
        projectObj.track = trackObj
        projectObj.save()
    except:
        result['isSuccessful'] = False
    return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def deleteProject(request):
    projectId = request.POST.get('id', '')
    result = {
        'isSuccessful' : True,
    }
    try:
        projectObj = project.objects.get(id=projectId)
        projectObj.is_deleted = 1
        projectObj.save()
    except:
        result['isSuccessful'] = False
    return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def getTrackFunctions(request):
    track_id = request.GET.get('track_id')
    result = {
        'isSuccessful' : True
    }
    try:
        tf_list = track_functions.objects.filter(track_id=track_id)
        function_list = list()
        for tf_obj in tf_list:
            function_info = {
                'id': tf_obj.function.id,
                'name': tf_obj.function.function,
            }
            function_list.append(function_info)
        result['functions'] = function_list
    except:
        result['isSuccessful'] = False
        traceback.print_exc()
    return HttpResponse(json.dumps(result), content_type='application/json')

@csrf_exempt
def getResultImage(request):
    result = {
        'isSuccessful': True,
    }
    chainId = request.GET.get('id')
    try:
        chainObj = chain.objects.get(id=chainId)
        if not chainObj.isModified:
            result['filepath'] = chainObj.image_file_path
        else:
            chainStr = chainObj.sequence
            if chainStr.startswith('_'):
                chainStr = chainStr[1:]
            if chainStr == "" or chainStr == None:
                result['isSuccessful'] = False
            else:
                chainName = chainObj.name
                width = 80 * len(chainStr.split('_'))
                height = 100
                if width > 800:
                    width = 800
                    height = 100 * (len(chainStr.split('_')) / 10);
                result['filepath'] = getSequenceResultImage(chainStr, width, height, chainName)
                chainObj.isModified = False
                chainObj.image_file_path = result['filepath']
                chainObj.save()
    except:
        result['isSuccessful'] = False
    return HttpResponse(json.dumps(result), content_type="application/json")