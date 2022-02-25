from ninja import NinjaAPI,Schema
from django.http import HttpResponse, HttpResponseForbidden
from django.urls import path
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from .models import Token

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
@api.post('anotherpost/',url_name="another_post")
def another(request):
    return HttpResponse("success")
@api.post('signin/',url_name="signin")
def signin(request,user:User=None):
    username = user.username.strip()
    password = user.password.strip()
    if username and password:
        print(password)
        user = get_user_model().objects.filter(username=username).first()
        if user and check_password(password,user.password):
            token = Token.get_valid_token(user.pk)
            return HttpResponse(user)
    
    return HttpResponseForbidden(request)
    

