from django.utils.deprecation import MiddlewareMixin

class ThemeMiddleware(MiddlewareMixin):
    """Middleware to handle theme preferences"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        #Set default theme if not set
        if 'theme' not in request.session:
            request.session['theme'] = 'light'

        response = self.get_response(request)
        return response
    
    
