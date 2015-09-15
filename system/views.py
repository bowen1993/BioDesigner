import json

from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response
from django.template import RequestContext, loader
from django.core.mail import send_mail
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from system.gene import search_compound, get_compound_info, get_gene_info
from system.gene import gene_graph

@csrf_exempt
def systemView(request):
    template = loader.get_template('home/system.html')
    context = RequestContext(request, { 
        })
    return HttpResponse(template.render(context))

@csrf_exempt
def searchCompound(request):
    keyword = request.GET.get('keyword')
    result = search_compound(keyword)
    return HttpResponse(json.dumps(result), content_type='application/json')

@csrf_exempt
def getCompound(request):
    cid = request.GET.get('id')
    get_result = get_compound_info(cid)
    result = {
        'isSuccessful': get_result[0],
        'info' : get_result[1]
    }
    return HttpResponse(json.dumps(result), content_type='application/json')

@csrf_exempt
def getGene(request):
    gid = request.GET.get('id')
    get_result = get_gene_info(gid)
    result = {
        'isSuccessful': get_result[0],
        'info': get_result[1],
    }
    return HttpResponse(json.dumps(result), content_type='application/json')

@csrf_exempt
def getRelatedCompound(request):
    cstr = request.POST.get('id', '')
    graph = gene_graph(cstr, None)
    graph.cal_graph()
    result = graph.get_graph()
    return HttpResponse(json.dumps(result), content_type='application/json')