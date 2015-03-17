from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^app/', include('apps.main.urls')),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += staticfiles_urlpatterns()
