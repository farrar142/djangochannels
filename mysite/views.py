# chat/views.py
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.views import View
from asgiref.sync import sync_to_async
from stocks.models import *
from trades.models import *
from assets.models import *
def index(request):
    products = Product.objects.order_by('category__name')
    context={'products':products}
    return render(request,'index.html',context)

def test(request):
    trade_order = Trade_Order.objects.all()
    context= {"trade_order":trade_order}
    return render(request,'test.html',context)

