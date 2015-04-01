"""
Decorators for the REST API.
"""

# system imports
from functools import wraps

# Django imports
from django.db import transaction

#DispatcherError and Tastypie imports
from lib.error import DispatcherError, DispatcherHTTP405, DispatcherHTTP404
from tastypie.exceptions import ImmediateHttpResponse

# logging
import logging
logger = logging.getLogger('dispatcher.lib.views')

# error classes
class MissingUsername():
    pass


def obj_wrapper(f):
    """
    Wrapper for obj_create, obj_update, and obj_delete Tastypie override
    methods. This wrapper applies the Django commit/rollback semantics;
    """
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        @transaction.commit_on_success
        def _wrapped_f(self, *args, **kwargs):
            try:
                return f(self, *args, **kwargs)
            except Exception, e:
                logger.exception(str(e))
                raise e
        return _wrapped_f(self, *args, **kwargs)
    return wrapper

def rest_wrapper(f):
    """
    Wrapper for post_, get_, put_ ,and delete_ Tastypie override
    methods. This wrapper does the following:
      1. wrap try/catch blocks for REST api to formalize catch response
      2. provide In and Out method log message to better REST api logging
      3. Implements DispatcherError codes for customers
    """
    @wraps(f)
    def wrapper(self, request_type, request, **kwargs):
        logger.info("Calling %s: %s %s" % (f.__name__, request.method, request.path))
        try:
            return f(self, request_type, request, **kwargs)
        except DispatcherHTTP404, e:
            logger.exception("Error code: %d: %s" % (e.code, str(e)))
            message = str(e)
            error_code = str(e.code)
            raise ImmediateHttpResponse(response=self.create_error_response(request,
                                                                            message=message,
                                                                            error_code=error_code,
                                                                            http_status_code=404))
        except DispatcherHTTP405, e:
            logger.exception("Error code: %d: %s" % (e.code, str(e)))
            message = str(e)
            error_code = str(e.code)
            raise ImmediateHttpResponse(response=self.create_error_response(request,
                                                                            message=message,
                                                                            error_code=error_code,
                                                                            http_status_code=405))
        except DispatcherError, e:
            #logger.exception("Error code: %d: %s" % (e.code, str(e)))
            # Changed from exception to warn b/c this was taking 45 seconds to log
            logger.warn("Error code: %d: %s" % (e.code, str(e)))
            message = str(e)
            error_code = str(e.code)
            raise ImmediateHttpResponse(response=self.create_error_response(request,
                                                                            message=message,
                                                                            error_code=error_code,
                                                                            http_status_code=400))
        except Exception, e:
            logger.exception(str(e))
            raise ImmediateHttpResponse(response=self.create_error_response(request,
                                                                            message=str(e),
                                                                            http_status_code=500))
        finally:
            logger.info("Exiting %s: %s %s" % (f.__name__, request.method, request.path))
    return wrapper
