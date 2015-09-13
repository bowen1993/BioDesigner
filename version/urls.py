from django.conf.urls import patterns, include, url
from django.contrib import admin
from version import views

urlpatterns = patterns('',
    url(r'^createV', views.createVersion),
    url(r'^getTheV', views.getTheVersion),
    url(r'^getVS',views.getVersions),
)