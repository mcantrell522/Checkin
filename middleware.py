from django.template import RequestContext, loader
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden  

class Http403(Exception):
    pass  

def render_to_403(*args, **kwargs):
    """
        Returns a HttpResponseForbidden whose content is filled with the result of calling
        django.template.loader.render_to_string() with the passed arguments.
    """
    if not isinstance(args,list):
        args = []
        args.append('403.html')              

    httpresponse_kwargs = {'mimetype': kwargs.pop('mimetype', None)}
    response = HttpResponseForbidden(loader.render_to_string(*args, **kwargs), **httpresponse_kwargs)              

    return response

class BadUserCreation(Exception):
    pass  

def render_to_BadUserCreation(*args, **kwargs):
    """
        Returns a HttpResponseForbidden whose content is filled with the result of calling
        django.template.loader.render_to_string() with the passed arguments.
    """
    if not isinstance(args,list):
        args = []
        args.append('BadUserCreation.html')              

    httpresponse_kwargs = {'mimetype': kwargs.pop('mimetype', None)}
    response = HttpResponseForbidden(loader.render_to_string(*args, **kwargs), **httpresponse_kwargs)              

    return response

class HttpExceptionMiddleware(object):
    def process_exception(self,request,exception):
        if isinstance(exception,Http403):
            if settings.DEBUG:
                raise PermissionDenied
            return render_to_403(context_instance=RequestContext(request))
        elif isinstance(exception,BadUserCreation):
            if settings.DEBUG:
                raise PermissionDenied
            return render_to_BadUserCreation(context_instance=RequestContext(request))
