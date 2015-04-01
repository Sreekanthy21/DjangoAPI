"""
web.urls
Top level URLConf for the Dispatcher.
"""

# Django imports
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.simple import redirect_to

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

# Dispatcher imports
from api.urls import rest_api

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'web.views.home', name='home'),
    # url(r'^web/', include('web.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    #(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

    # APIs
    url(r'^go/', include(rest_api.urls)),
    
    # Other APPs
    url(r'^go/app/', include('web.app.urls')),
    url(r'^go/tools/', include('web.tools.urls')),
)

urlpatterns += staticfiles_urlpatterns()

