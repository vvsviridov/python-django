from django.http import HttpRequest, HttpResponseBadRequest
from datetime import datetime


def get_useragent_on_request_middleware(get_response):

    # print('Middleware Init')

    def middleware(request: HttpRequest):
        # print('Before get response')
        request.user_agent = request.META['HTTP_USER_AGENT']
        response = get_response(request)
        # print('After get response')
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
        # print('requests_count', self.requests_count)
        response = self.get_response(request)
        self.responses_count += 1
        # print('responses_count', self.responses_count)
        return response


class ThrottlingValidator:
    def __init__(self, get_response):
        self.get_response = get_response
        self.user_counter = {}
        self.user_last_active = {}

    def __call__(self, request: HttpRequest):
        user_ip = request.META['REMOTE_ADDR']
        if self.user_counter.get(user_ip) is not None:
            self.user_counter[user_ip] += 1
            if self.user_counter[user_ip] > 5:
                if (datetime.now() - self.user_last_active[user_ip]).seconds < 10:
                    return HttpResponseBadRequest(f'Too many requests!')
                else:
                    self.user_counter[user_ip] = 1
        else:
            self.user_counter[user_ip] = 1
        self.user_last_active[user_ip] = datetime.now()
        response = self.get_response(request)
        return response
