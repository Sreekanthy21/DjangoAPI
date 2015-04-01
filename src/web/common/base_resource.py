'''
web.base_resource
Base class for API resources.
'''

# imports
from web.guard.views import GuardClientAuthentication, GuardUserAuthorization
from lib.views.base_resource import BaseModelResource


class BaseAPIResource(BaseModelResource):
    class Meta:
        authentication = GuardClientAuthentication()
        authorization = GuardUserAuthorization()
