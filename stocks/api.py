from ninja import Router
from django.db.models import *

from mysite.serializer import converter
from mysite.forms import *

from stocks.models import *
router = Router()

@router.get('/')
async def get_product_all(request):
    result = Product.objects.all().annotate(category_name=F('category_id__name'))#db에 query하지않음
    return await converter(result)

@router.get('/get/{product_id}')
async def get_product(request,product_id:int):
    result = Product.objects.filter(**{"pk":product_id}).annotate(category_name=F('category_id__name'))
    return await converter(result)

@router.post('/post/')
async def post_product(request,form:ProductForm):
    """
    product_id : int
    user_id : int
    price : int
    quantity : int
    type_id : int
    code_id : int
    """
    result = Product(**form.dict())
    await result.async_save()
    return await converter(result)
