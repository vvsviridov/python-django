from django.http import HttpRequest, HttpResponse


def get_useragent_on_request_middleware(get_response):

    print('Middleware Init')

    def middleware(request: HttpRequest):
        print('Before get response')
        request.user_agent = request.META['HTTP_USER_AGENT']
        response = get_response(request)
        print('After get response')
        return response
    
    return middleware


class CountRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests_count = 0
        self.responses_count = 0
        self.exceptions_count = 0

    def __call__(self, request: HttpRequest):
        self.requests_count += 1
        print('requests_count', self.requests_count)
        response = self.get_response(request)
        self.responses_count += 1
        print('responses_count', self.responses_count)
        return response


class UploadFileSizeValidator:
    def __init__(self, get_response):
        self.get_response = get_response
        self.allowed_size = 1 * 1024 *1024

    def __call__(self, request: HttpRequest):
        if request.method == 'POST' and request.FILES.get('file'):
            myfile = request.FILES['file']
            if myfile.size > self.allowed_size:
                return HttpResponse(f'File "{myfile.name}" too big!')
        response = self.get_response(request)
        return response


class ThrottlingValidator:
    def __init__(self, get_response):
        self.get_response = get_response
        self.user_counter = {}
        self.user_last_active = {}

    def __call__(self, request: HttpRequest):
        user_ip = request.META['REMOTE_ADDR']
        if self.user_counter.get(user_ip):
            self.user_counter['user_ip'] += 1
        else:
            self.user_counter['user_ip'] = 1
        response = self.get_response(request)
        return response
