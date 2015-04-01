"""
web.api.views.package
REST API packages resource code.
"""

# System imports
import logging
import datetime
from pprint import pprint
import urllib2
import urllib
import glob
import fnmatch
import os

# Django imports
from django.http import HttpResponseNotFound 
from django.conf.urls.defaults import url
from django.db import connections

# 3rd party libs
from tastypie.utils import trailing_slash
from tastypie.exceptions import NotFound, ImmediateHttpResponse
from tastypie.http import HttpApplicationError, HttpBadRequest, HttpNotImplemented, HttpResponse, HttpAccepted, HttpMethodNotAllowed

# Dispatcher imports
from lib.views.decorators import obj_wrapper

# local imports
from web.common.base_resource import BaseAPIResource
from web.common.utils import get_query_string_value
import web.settings as settings
import utils

logger = logging.getLogger("drive.api.views.pacakge")

class Resource(BaseAPIResource):

    class Meta(BaseAPIResource.Meta):
        resource_name = 'builds'
        list_allowed_methods = ['get']
        detail_allowed_methods = []
        #detail_allowed_methods = ['get', 'post', 'put', 'delete']
        always_return_data = True
        default_format = 'application/json'

    def base_urls(self):
        return [
            url(r"^(?P<resource_name>%s)%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('dispatch_list'), name="api_dispatch_list"),
        ]


    # GET request
    # http://.../.../api/builds/?build_ids=24234234
    def get_list(self, request, **kwargs):

        result = {
            'builds' : {},
        }
        pprint(result)
    
        return self.get_api_response(request, 'success', result)
		
    #=================================================================================
