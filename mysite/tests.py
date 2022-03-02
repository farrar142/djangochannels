from django.test import TestCase
from django.db.models.query import QuerySet
from django.db.models import Model
from asgiref.sync import sync_to_async,async_to_sync
from channels.db import database_sync_to_async
from accounts.models import User
from commons.models import *
from assets.models import Asset_Item
from mysite.serializer import converter
# class SerializerTests(TestCase):
    
#     @classmethod
#     def setUpTestData(cls):
#         from mysite import datas
#         datas.gen_datas()
    
#     def test_기본쿼리셋시리얼라이즈(self):
#         target = User.objects.all()
#         result:list = converter(target)
        
#         self.assertEquals(type(target),QuerySet)
#         self.assertEquals(type(result),list)
#         self.assertEquals(type(result[0]),dict)
        
#     def test_쿼리딕트셋시이얼라이즈(self):
#         target = User.objects.all().values()
        
#         result:list = converter(target)
#         self.assertEquals(type(target),QuerySet)
#         self.assertEquals(type(result),list)
#         self.assertEquals(type(result[0]),dict)
        
#     def test_Model_인스턴스_시리얼라이즈(self):
#         target = User.objects.first()
#         result:list = converter(target)
#         self.assertEquals(type(target),User)
#         self.assertEquals(type(result),list)
#         self.assertEquals(type(result[0]),dict)
        
#     def test_Dict_객체_시리얼라이즈(self):
#         target = {
#             'name':"sandring",
#             "age":"29",
#             "wannacomments?":"sibbal",
#         }
#         result:list = converter(target)
#         self.assertEquals(type(target),dict)
#         self.assertEquals(type(result),list)
#         self.assertEquals(type(result[0]),dict)
    
#     def test_사용자정의클래스_시리얼라이즈(self):
#         class Apple:
#             color='red'
#             edible=True
#         target = Apple()
#         result:list = converter(target)
#         self.assertEquals(type(target),Apple)
#         self.assertEquals(type(result),list)
#         self.assertEquals(type(result[0]),dict)