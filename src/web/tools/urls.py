"""
web.app.urls
URLConf for miscellaneous URLs.
"""

# Django imports
from django.conf.urls.defaults import patterns
from django.views.generic.simple import redirect_to


urlpatterns = patterns('',
    (r'^(?P<page>\w+)/$', page),
)
