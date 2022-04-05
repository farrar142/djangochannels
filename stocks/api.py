from ninja import Router
from django.db.models import *
from django.utils import timezone
from datetime import timedelta
from asgiref.sync import sync_to_async
from mysite.serializer import aconverter as converter
from mysite.forms import *

from stocks.models import *
router = Router()


@sync_to_async
@router.get('/')
def get_product_all(request):
    result = Product.objects.all().annotate(category_name=F('category_id__name'))#db에 query하지않음
    return result

@sync_to_async
@router.get('/logs/get')
def get_products_logs(request,product_id:int=0,date:int=0):
    result = ProductLog.objects.values('logged_date','id','name','start_price','end_price','max_price','min_price')
    if product_id:
        result = result.filter(id=product_id)
    if date:
        result = result.filter(logged_date__gte=timezone.now()-timedelta(days=date))
    return result

@sync_to_async
@router.get('/get/{product_id}')
def get_product(request,product_id:int):
    result = Product.objects.filter(**{"pk":product_id}).annotate(category_name=F('category_id__name'))
    return result


@sync_to_async
@router.post('/post/')
def post_product(request,form:ProductForm):
    """
    product_id : int
    user_id : int
    price : int
    quantity : int
    type_id : int
    code_id : int
    """
    result = Product(**form.dict())
    result.save()
    return result
