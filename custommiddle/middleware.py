import json
import re
from time import time
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
from .models import Token
from base64 import b64decode,b64decode
from pprint import pprint

def get_info(target):
    print("===debug===")
    pprint(dir(target))
    print(target)
    print("===debugend===")

class CustomTokenMiddleware(MiddlewareMixin):    
    def __init__(self,get_response):
        urls = [            
            re.compile(r'^(.*)/api'),
            re.compile(r'^api'),
        ]
        methods = ['GET','POST','PUT','PATCH','DELETE']
        
        self.PREFIX                 = getattr(settings,"CUSTOM_PREFIX",'')
        if self.PREFIX:
            self.PREFIX += "_"
        
        self.BACKEND_ONLY           = getattr(settings,f"{self.PREFIX}BACKEND_ONLY",True)
        self.FILTERED_URLS          = getattr(settings,f"{self.PREFIX}FILTERED_URL",urls)
        self.FILTERED_METHODS       = getattr(settings,f"{self.PREFIX}FILTERED_METHODS",methods)
        self.CONTENT_TYPE           = getattr(settings,f"{self.PREFIX}CONTENT_TYPE","JSON")
        self.STRATEGY               = getattr(settings,f"{self.PREFIX}STRATEGY","WEAK")
        super().__init__(get_response)
    
    def process_request(self,request:HttpRequest):
        #시나리오 1 토큰정보를 가지고 접속함 expired False.
        LOGIN_URL = "/token/signin/"
        if self.BACKEND_ONLY:
            token = self.validator(request)
            if token:
                #시나리오 토큰정보가 유효함. 토큰을 리프레시시켜줌.
                Token.token_refresher(token)
                print("인증된토큰")
            else:
                print("미인가사용자")
                if request.path in LOGIN_URL:
                    get_info(self.get_datas(request))
                    
                    
                elif request.method in self.FILTERED_METHODS:
                    return HttpResponseForbidden(request,"미인가사용자")
            self.authorize(request,token)
                
            if self.get_token_from_url(request) == "test":
                token = Token.get_or_create(token,1)
                self.send_token(request,token)
                self.get_token_from_url(request)
        return self.get_response(request)
    
    def process_response(self,request:HttpRequest,response:HttpResponse):
        if response.status_code==404:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
        #print(request.COOKIES)
        return response  
    
    def get_datas(self,request):
        print(self.CONTENT_TYPE)
        if self.CONTENT_TYPE == "JSON":
            result = json.loads(request.body)
        else:
            result = request.POST
        return result
    
    def validator(self,request):
        """
        request에 담긴 token값을 받아서 유효한토큰 혹은 False를 반환함
        """
        try:
            value = self.get_token_from_url(request)
            #print(f"value : {value}")
            token=Token.objects.get(token=value)
            if token.expired_in >= timezone.now():
                return token
            else:
                return False
        except:
            print('Token Not Found')
            return False
    
    def authorize(self,request,token):
        if token:
            request.user = token.user
        else:
            request.user = AnonymousUser()
    
    def get_token_from_url(self,request:HttpRequest):
        serial = request.COOKIES.get('token')
        #print(f"token  : {serial}")
        try:
            return serial
        except:
            return None
        
    
    def send_token(self,request:HttpRequest,token:Token):
        request.COOKIES.update(token=token.token)
        return token
    
    
def ResponseCheckMiddleware(get_response):
    def MiddleWare(request):
        result = get_response(request)
        return result
    return MiddleWare#

class TimeChecker(MiddlewareMixin):
    
    def process_request(self,request:HttpRequest):
        start_time = time()
        request.COOKIES.update(start_time=start_time)
        print('timechecking')
        return self.get_response(request)
    
    def process_response(self,request:HttpRequest,response:HttpResponse):
        start_time = request.COOKIES.get('start_time')
        print(f"{time()-start_time:0.5f}sec")
        return response
    
class migrator(MiddlewareMixin):
    
    def process_request(self,request:HttpRequest):
        if not get_user_model().objects.all().exists():
            from mysite import datas
        return self.get_response(request)
    