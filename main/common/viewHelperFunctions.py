
from django.http import Http404

def ajaxRequest(func):
    '''
        Check that input request is an ajax request.
    '''
    def wrapFunc(*args, **kwargs):
        request = args[0]
        if not request.is_ajax():
            raise Http404
        return func(*args, **kwargs)
    return wrapFunc


def checkPost(func):
    '''
        Verify that text post to network is valid.
    '''
    def wrapFunc(*args, **kwargs):
        request = args[0]
        if not request.POST:
            raise Http404

        return func(*args, **kwargs)
    return wrapFunc
