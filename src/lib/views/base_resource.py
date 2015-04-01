'''
'''
import socket
from datetime import datetime, date
import time
from xml.etree import ElementTree
from pprint import pprint
import json

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound 
from tastypie.exceptions import NotFound, ImmediateHttpResponse
from tastypie.http import HttpApplicationError, HttpBadRequest, HttpNotImplemented, HttpResponse, HttpAccepted, HttpMethodNotAllowed
from tastypie.resources import ModelResource, convert_post_to_put
from tastypie.utils.mime import build_content_type
from decorators import rest_wrapper
from lib.error import DispatcherHTTP405
from utils import remove_objects_from_serialized

class BaseModelResource(ModelResource):
    '''
    A child class that inherits from ModelResource. It is intended to override
    methods from ModelResource so it generates the responses that we need.
    '''
    
    def _handle_500(self, request, exception):
        """
        Overriding tastypie method to return HTTP response 500 error back in 
        serialized format
        """
        import traceback
        import sys
        the_trace = '\n'.join(traceback.format_exception(*(sys.exc_info())))
        response_class = HttpApplicationError
        
        if isinstance(exception, (NotFound, ObjectDoesNotExist)):
            response_class = HttpResponseNotFound
        
        if settings.DEBUG:
            data = {
                "error_message": unicode(exception),
                "traceback": the_trace,
            }
            desired_format = self.determine_format(request)
            serialized = self.serialize(request, data, desired_format)
            return response_class(content=serialized, content_type=build_content_type(desired_format))
        
        # When DEBUG is False, send an error message to the admins (unless it's
        # a 404, in which case we check the setting).
        if not isinstance(exception, (NotFound, ObjectDoesNotExist)) or getattr(settings, 'SEND_BROKEN_LINK_EMAILS', False):
            from django.core.mail import mail_admins
            subject = 'Error (%s IP): %s' % ((request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS and 'internal' or 'EXTERNAL'), request.path)
            try:
                request_repr = repr(request)
            except:
                request_repr = "Request repr() unavailable"
            
            message = "%s\n\n%s" % (the_trace, request_repr)
            mail_admins(subject, message, fail_silently=True)
        
        # Prep the data going out.
        desired_format = self.determine_format(request)
        data = {
            "error_message": getattr(settings, 'TASTYPIE_CANNED_ERROR', "Sorry, this request could not be processed. Please try again later."),
        }
        error_response = self.create_error_response(request, message=data['error_message'], http_status_code=500)
        return response_class(content=error_response.content, content_type=build_content_type(desired_format))
    
    def create_datetime(self, d=None, t=None, dt=None):
        """
        Helper method to create datetime object from an XML date, time, and
        datetime
        """
        date_time = None
        if d and t:
            date_time = datetime.combine(d, t)
        elif d is None and t:
            d = date.today()
            date_time = datetime.combine(d, t)
        elif d and t is None:
            t = datetime.now().time()
            date_time = datetime.combine(d, t)
        elif dt:
            date_time = datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S")
        return date_time
    
    def create_error_response(self, request, **kwargs):
        """
        Helper method to create a error response
        """
        desired_format = self.determine_format(request)
        standard_result_dict = {'message': kwargs['message']}
        error_code = kwargs.get('error_code')
        if error_code:
            standard_result_dict['error_code'] = error_code
        serialized = self.serialize(request, standard_result_dict, desired_format)
        if kwargs['http_status_code'] == 404:
            return HttpResponseNotFound(content=serialized, content_type=build_content_type(desired_format))
        if kwargs['http_status_code'] == 405:
            return HttpMethodNotAllowed(content=serialized, content_type=build_content_type(desired_format))
        else:
            return HttpBadRequest(content=serialized, content_type=build_content_type(desired_format))
        
    
    #@rest_wrapper
    def dispatch(self, request_type, request, **kwargs):
        """
        Overridden Tastypie method that handles the common operations 
        (allowed HTTP method, authentication, throttling, method lookup) 
        surrounding most CRUD interactions.
        """
        request.META['start_time'] = time.time()
        try:
            allowed_methods = getattr(self._meta, "%s_allowed_methods" % request_type, None)
            request_method = self.method_check(request, allowed=allowed_methods)
        except ImmediateHttpResponse, e:
            raise DispatcherHTTP405("Method Not Allowed")
        
        method = getattr(self, "%s_%s" % (request_method, request_type), None)
        
        if method is None:
            raise ImmediateHttpResponse(response=HttpNotImplemented())
        
        self.is_authenticated(request)
        self.is_authorized(request)
        self.throttle_check(request)
        
        # All clear. Process the request.
        request = convert_post_to_put(request)
        response = method(request, **kwargs)
        
        # Add the throttled request.
        self.log_throttled_access(request)
        
        # If what comes back isn't a ``HttpResponse``, assume that the
        # request was accepted and that some action occurred. This also
        # prevents Django from freaking out.
        if not isinstance(response, HttpResponse):
            response = HttpAccepted()
        
        return response

    def determine_format(self, request):
        if request.GET.get('format'):
            return super(BaseModelResource,self).determine_format(request);
        
        return 'application/json'

    def get_response(self, request, data):
        desired_format = self.determine_format(request)
        serialized = self.serialize(request, data, desired_format)
        serialized = remove_objects_from_serialized(serialized)
        return HttpResponse(content=serialized,
                            content_type=build_content_type(desired_format))

    def get_api_response(self, request, status, result):
        desired_format = self.determine_format(request)
        time_taken = str(time.time() - request.META['start_time']) + " seconds"
        render_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S %a')
        render_host = socket.gethostname()
        out =  {
            '_meta': {
                'date': render_time,
                #'host': render_host,
                'time_taken': time_taken,
            },
            'status': status
        }
        if (result != None):
            out['result'] = result

        serialized = self.serialize(request, out, desired_format)
        #serialized = json.dumps(out)
        #serialized = remove_objects_from_serialized(serialized)
        return HttpResponse(content=serialized,
                            content_type=build_content_type(desired_format))

