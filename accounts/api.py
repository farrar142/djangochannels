from ninja import Router
from django.db.models import *

from mysite.serializer import aconverter
from accounts.models import *
accounts_api = Router()
points_api = Router()

@accounts_api.get('/user/get')
async def get_user(request,user_id:int):
    result = User.objects.filter(pk=user_id)
    return await aconverter(result)

@points_api.get('/point/get')
async def get_point(request,point_id:int):
    result = Point.objects.filter(pk=point_id)
    return await aconverter(result)