"""
web.app.views
View code for the Dispatcher SDK.
"""

# system imports
from __future__ import division
import logging
import os
import errno
import sys
import subprocess
import pickle
from pprint import pprint
import datetime
import json
import urllib2
from datetime import datetime, timedelta, date
from collections import defaultdict

# Django imports
from django.conf import settings
from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db import connections


def page(request, page):
    """
    """
    return _app_render(request, page + '.html')


