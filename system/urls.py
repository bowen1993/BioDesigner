from django.conf.urls import patterns, include, url
from django.contrib import admin
from system import views

urlpatterns = patterns('',
    url(r'^searchCompound$', views.searchCompound),
    url(r'^getCompound$', views.getCompound),
    url(r'^related$', views.getRelatedCompound),
    url(r'^system$', views.systemView)
)
