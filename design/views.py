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
from search_part import ambiguousSearch, getPart
from accounts.models import User
from design.models import project, functions, tracks, user_project, tracks
from design.project import searchProject, getUserProject, getChain
from design.recommend import getApriorRecommend, getMarkovRecommend

@csrf_exempt
def searchParts(request):
    keyword = request.GET.get('keyword')
    results = ambiguousSearch(keyword)
    return HttpResponse(json.dumps(results), content_type="application/json")

@csrf_exempt
def getParts(request):
    partName = request.GET.get('partname')
    results = getPart(partName)
    return HttpResponse(json.dumps(results), content_type="application/json")

@csrf_exempt
def dashboardView(request):
    try:
        isLoggedIn = request.session['isLoggedIn']
        isAccountConfirm = isAccountActive(request)
        if isLoggedIn and isAccountConfirm:
            template = loader.get_template('home/dashboard.html')
            context = RequestContext(request, {})
            return HttpResponse(template.render(context))
        else:
            return HttpResponseRedirect('/')
    except KeyError:
        return HttpResponseRedirect('/')

@csrf_exempt
def testDashboardView(request):
    try:
        isLoggedIn = request.session['isLoggedIn']
        isAccountConfirm = isAccountActive(request)
        if isLoggedIn and isAccountConfirm:
            template = loader.get_template('home/dashboard_.html')
            context = RequestContext(request, {})
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
def saveChain(request):
    result = {'isSuccessful':True,}
    chainContent = request.POST.get('chain','')
    projectId = int(request.POST.get('id',''))
    projectObject = project.objects.get(pk=projectId)

    if projectObject == "":
        result['isSuccessful'] = False
    else:
        projectObject.chain = chainContent
        try:
            projectObject.save()
        except Exception, e:
            result['isSuccessful'] = False

    return HttpResponse(json.dumps(result),content_type="application/json")

@csrf_exempt
def getARecommend(request):
    return HttpResponse(json.dumps(getApriorRecommend()), content_type="application/json")

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