from django.http import JsonResponse
from django.shortcuts import redirect, render,get_object_or_404
from django.contrib import messages
from django.db.models import *
from products.models import Product
from .models import *
from .forms import TradeItemForm
from mysite.const import *
# Create your views here.
from mysite.functions import auto_login

@auto_login
def chart(request,product_name):
    context={}
    product = get_object_or_404(Product,name=product_name)
    buys = TradeItem.objects.filter(product=product,type=BUY)
    sells = TradeItem.objects.filter(product=product,type=SELL)
    buys =buys.values('price').annotate(quantity=Sum('quantity'),count=Count('user'))
    sells =sells.values('price').annotate(quantity=Sum('quantity'),count=Count('user'))
    context.update(product=product)
    context.update(buys=buys)
    context.update(sells=sells)
    return render(request,'market/호가창.html',context)

@auto_login
def make_trade(request,product_name):
    product = get_object_or_404(Product,name=product_name)
    user = request.user
    context = {}
    if request.method == "POST":
        form = TradeItemForm(request.POST)
        messages.success(request,form)
        if form.is_valid():
            trade = form.save(commit=False)
            trade.user = user
            trade.product = product
            if trade.trade_logic():
                trade.save()
        # return redirect("market:호가",product_name = product.name)
        return JsonResponse({"test": trade.price})
    return JsonResponse({"test":"code"})