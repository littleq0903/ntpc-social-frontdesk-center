from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    url(r'^case-printing/(?P<application_id>\d+)/$', views.case_print),
    url(r'$', views.index), 
)


