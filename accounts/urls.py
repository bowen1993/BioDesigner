from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from accounts import views

urlpatterns = patterns('',
    url(r'^$', views.indexView),
    url(r'^login$', views.loginAction),
    url(r'^logout$', views.logoutAction),
    url(r'^register$', views.registerAction),
    url(r'^successful', views.registerSuccessView),
    url(r'^confirm/(?P<activation_key>\w+)/', views.register_confirm),
)
