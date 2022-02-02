# chat/views.py
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.views import View

from products.models import *

class MainView(View):
    def get(self,request):
        products = Product.objects.order_by('category__name')
        context={'products':products}
        return render(request,'index.html',context)
