from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

from apps.main import api

urlpatterns = patterns('',
    url(r'^api/', include(api.ROUTER.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^app/', include('apps.main.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('django.contrib.auth.urls')),
)

urlpatterns += staticfiles_urlpatterns()
