# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'clients.views.entry', name='entry'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^settimeoffset/', 'dela.views.settimeoffset', name='settimeoffset'),
    url(r'^savenote/', 'clients.views.savenote', name='savenote'),
    url(r'^testrequest/', 'clients.views.testrequest', name='testrequest'),
	url(r'^login/', 'clients.views.login', name='login'),
    url(r'^logout/', 'clients.views.logout_view', name='logout'),
    url(r'^jdatatableaction/', 'utils.Jdatatable.views.jdatatableaction', name='jdatatableaction'),
    url(r'^jeditformprocessor/', 'utils.Jdatatable.views.jeditformprocessor', name='jeditformprocessor'),
    url(r'^projects/', 'projects.views.projectsentry', name='projects'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
