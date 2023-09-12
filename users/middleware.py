import json
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

class MoveJWTRefreshCookieIntoTheBody(MiddlewareMixin):

    def __init__(self, get_response):
        super().__init__(get_response)
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, *view_args, **view_kwargs):

        if request.path == '/api/login/refresh/' and settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'] in request.COOKIES:

            data = {"refresh": request.COOKIES[settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH']]}
            request._body = data
