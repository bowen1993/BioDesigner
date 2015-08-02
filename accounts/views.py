from accounts.models import User, UserSafety, loginRecord
from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response
from django.template import RequestContext, loader
from django.core.mail import send_mail
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from EmailVery import EmailVerity
import hashlib
import json
import datetime
import random

# Create your views here.

def indexView(request):
    # check is allow auto login
    if (isAllowAutoLogin(request)):
        recordLogin(request.session['username'], get_client_ip(request), True)
        return HttpResponseRedirect('/home/project')
    # render and return the page
    template = loader.get_template('accounts/index.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))

def testIndexView(request):
    template = loader.get_template('accounts/new_index.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))

def registerSuccessView(request):
    try:
        isLoggedIn = request.session['isLoggedIn']
        if request.session['isLoggedIn']:
            template = loader.get_template('accounts/registersuccess.html')
            context = RequestContext(request, {})
            return HttpResponse(template.render(context))
        else:
            return HttpResponseRedirect('/')
    except KeyError:
        return HttpResponseRedirect('/')

def isAllowAutoLogin(request):
    try:
        isAllowAutoLogin = request.session['isAllowAutoLogin']
        return isAllowAutoLogin
    except KeyError:
        return False

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@csrf_exempt
def loginAction(request):
    """handle the login request

    handle the login request, validate and create session

    Args:
        request: the http request to be processed

    Returns: A http response which contains the json result
    """
    #get user inputs
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    isAutoLogin = request.POST.get('rememberMe', True)

    #the result to be returned
    results = {
            'isSuccessful': False,
            'isInfoEmpty': not username and not password,
            'isAccountValid': False,
    }

    # validation, create session and return result
    if not results['isInfoEmpty']:
        password = hashlib.sha1(password).hexdigest()
        results['isAccountValid'] = isAccountValid(username, password)
        results['isSuccessful'] = results['isAccountValid']
        if results['isSuccessful']:
            createSession(request, username, isAutoLogin)
    recordLogin(username, get_client_ip(request), results['isSuccessful'])

    return HttpResponse(json.dumps(results), content_type="application/json")


def createSession(request, username, isAutoLogin):
    """create session for the user who has just logged index

    Args:
        request: the http request which contains session
        username: the username of the user who has just logged index
        isAutoLogin: whether the user allow auto login or not
    """

    request.session['isLoggedIn'] = True
    request.session['username'] = username
    request.session['isAllowAutoLogin'] = isAutoLogin

def isAccountValid(username, password):
    try:
        User.objects.get(
            Q(username=username),
            Q(password=password)
        )
        return True
    except:
        return False

@csrf_exempt
def logoutAction(request):
    try:
        del request.session['isLoggedIn']
        del request.session['isAllowAutoLogin']
        del request.session['username']
    except:
        pass

    return HttpResponse()

@csrf_exempt
def registerAction(request):
    """handle the register request

    handle the register request and send confirmation email

    Args:
        request: the http request
    Returns:
        return a http response which contents the result json that indicate the register reuslt
    """
    # get user inputs
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    email = request.POST.get('email', '')
    print username
    print password
    print email
    result = {
            'isSuccessful': False,
            'errorMessage': '',
            'isInfoEmpty': not username and not password and not email,
    }

    #check whether the user or email exists
    if not isUserExists(username) and not result['isInfoEmpty']:
        saveNewUser(username, password, email)
        result['isSuccessful'] = True
        result['errorMessage'] = 'user exists or info empty'
        createSession(request, username, False)
    return HttpResponse(json.dumps(result), content_type="application/json")

def saveNewUser(username, password, email):
    password = hashlib.sha1(password).hexdigest()
    newUser = User(username=username, password=password, email=email, is_confirmed=True)
    newUser.save()
    #varifyEmail(email, newUser, username)

def varifyEmail(email, user, username):
    """email confirmation

    makesure the email is valid

    Args:
        email: the email to be confirmed
        user: the user of the email
    """
    # get active key with salt and email
    emailThread = EmailVerity(email, username)
    emailThread.start()
    return

def isUserExists(username):
    try:
        User.objects.get(username=username)
        return True
    except:
        return False

def isEmailExists(email):
    try:
        User.objects.get(email=email)
        return True
    except:
        return False

def recordLogin(username, ip, isSuccessful):
    newRecord = loginRecord(identity=username, login_ip=ip)
    newRecord.isSuccess = isSuccessful
    newRecord.save()

@csrf_exempt
def register_confirm(request, activation_key):
    """finish confirmation and active the account

    Args:
        request: the http request
        activation_key: the activation key
    Returns:
        Http redirect to successful page
    """
    user_safety = get_object_or_404(UserSafety, activation_key=activation_key)
    if user_safety.user.is_confirmed:
        return HttpResponseRedirect('/home/project')
    if user_safety.key_expires < timezone.now():
        return render_to_response('accounts/confirmExpires.html')
    user = user_safety.user
    user.is_confirmed = True
    user.save()
    return render_to_response('accounts/confirmed.html')
