from django.conf.urls import patterns, include, url
from django.contrib import admin
from design import views

urlpatterns = patterns('',
    url(r'^search$', views.searchParts),
    url(r'^get$', views.getParts),
    url(r'^dashboard$', views.dashboardView),
    url(r'^updateChain$', views.saveChain),
    url(r'^newProject$', views.createProject),
    url(r'^getChain$', views.getProjectChain),
    url(r'^getUserProject$', views.getUserProjects),
    url(r'^getProject$', views.getProject),
    url(r'^arecommend$', views.getARecommend),
    url(r'^seqRecommend$', views.getMRecommend),
    url(r'^tracks$', views.getTracks),
    url(r'^project', views.projectView),
    url(r'^getChainList', views.getProjectChains),
    url(r'^newDevice', views.createNewDevice),
    url(r'^getResultImage', views.getResultImage),
    url(r'^getChainLength', views.getChainLength),
    url(r'^changeProjectname', views.changeProjectName),
    url(r'^changeTrack', views.changeProjectTrack),
    url(r'^deleteProject', views.deleteProject),
    url(r'^getTrackFunctions', views.getTrackFunctions),
    url(r'^simulation$', views.simulationView),
    url(r'^simulate$', views.simulate)
)
