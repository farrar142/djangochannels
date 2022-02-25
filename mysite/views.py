# chat/views.py
from django.http import Http404, HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import render,redirect
from django.views import View
from asgiref.sync import sync_to_async
from trades.models import *
def index(request):
    return HttpResponse("indexpage")
def test(request):
    trade_order = Trade_Order.objects.all()
    context= {"trade_order":trade_order}
    return render(request,'test.html',context)

