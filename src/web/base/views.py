"""
web.base.views
Shared  view code.
"""

from datetime import datetime
import socket

# Django imports
from django.template import RequestContext
from django.shortcuts import render_to_response

# constants
_MAX_LIST_LENGTH = 25


def dsr_render(request, template, app, param_dict={}):
    render_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S %a')
    render_host = socket.gethostname()
    param_dict.update ( {
            'render_time': render_time,
            'render_host': render_host,
            'hostname':  "stage2os3109",
            'current_app': app,
            'navigation_links': (
                 ('SDK', '//sdk/'),
             )
         }
    )
    return render_to_response(template, param_dict, RequestContext(request))
