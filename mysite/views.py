# chat/views.py
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from django.views import View
from asgiref.sync import sync_to_async
from trades.models import *
def index(request):
    if request.user.is_authenticated:
        return HttpResponse("success")
    else:
        return Http404("failed")

def test(request):
    trade_order = Trade_Order.objects.all()
    context= {"trade_order":trade_order}
    return render(request,'test.html',context)

