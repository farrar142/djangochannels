# chat/views.py
from django.http import Http404, HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import render,redirect
from django.views import View
from asgiref.sync import sync_to_async
from trades.models import *
from accounts.models import Wallet
def index(request):
    return render(request,'index.html')
def test(request):
    context = {}
    result = Wallet.objects.all()[:2]
    context.update(wallets=result)
    return render(request,'test.html',context)

