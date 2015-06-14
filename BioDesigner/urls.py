from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tagging.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # 
    url(r'^$', include('accounts.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^home/', include('design.urls')),
)
