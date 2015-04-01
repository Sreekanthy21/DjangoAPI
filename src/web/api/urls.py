'''
urls for the REST API app
'''

# Django imports


# Tasty Pie imports
from tastypie.api import Api

# resources
from web.api.views import BuildResource

rest_api   = Api(api_name='api')

rest_api.register(Resource())
