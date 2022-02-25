from ninja import NinjaAPI,Schema
from django.http import HttpResponse, HttpResponseForbidden
from django.urls import path

api = NinjaAPI(urls_namespace="token",csrf=False)

class User(Schema):
    username:str=""
    password:str=""
@api.get('get/',url_name="get")
def get(request):
    return HttpResponse("success")
    
@api.post('post/',url_name="post")
def  post(request):
    return HttpResponseForbidden(request)

@api.post('signin/',url_name="signin")
def signin(request,user:User=None):
    if user.username.strip() and user.password.strip():
        return HttpResponse(user)
    else:
        return HttpResponseForbidden(request)
    

