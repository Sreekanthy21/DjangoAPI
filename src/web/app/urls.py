"""
web.app.urls
URLConf for miscellaneous URLs.
"""

# Django imports
from django.conf.urls.defaults import patterns
from django.views.generic.simple import redirect_to

# local imports
from views import home, page, help

urlpatterns = patterns('',
    (r'^$', home),
    (r'^help/$', help),
)
