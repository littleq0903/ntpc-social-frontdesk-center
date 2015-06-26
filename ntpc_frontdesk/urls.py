from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.conf.urls.static import static
from django.conf import settings

from apps.main import api


urlpatterns = patterns('',
    url(r'^api/', include(api.ROUTER.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^app/', include('apps.main.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^logout/', 'django.contrib.auth.views.logout_then_login'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
    }),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^$', RedirectView.as_view(url='/app/', permanent=True), name='index')
)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
