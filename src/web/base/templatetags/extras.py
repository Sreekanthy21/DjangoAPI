"""
web.base.templatetags.extras
Custom tags and filters for Django apps.
"""

# system imports
import os

# Django imports
from django import template

# template registration
register = template.Library()

# global variables
_version = ''


@register.simple_tag
def version():
    global _version
    if _version:
        return _version
    version_path = os.path.join(os.getenv('XDRIVE_ROOT'), 'data', 'version')
    if os.path.exists(version_path):
        version_file = open(version_path)
        try:
            _version = "Version %s" % version_file.read().strip()
        finally:
            version_file.close()
    else:
        _version = 'Development'
    return _version
