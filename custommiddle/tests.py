from urllib.parse import urlencode
from django.test import TestCase
from django.urls import reverse, reverse_lazy
from mysite.secret import PASSWORDS
from django.test.utils import override_settings
from django.conf import settings
import json

class TokenAPITests(TestCase):
    
    def df(self,path,cmd):
        url =reverse(path)
        case = {
            'get': self.client.get(url),
            'post':self.client.post(url)
        }
        
        return case.get(cmd)
    
    def token_없이_접근_시도(self):
        """POST로의 접근은 모두 막아놈."""
        pass
    
    def test_POST_접근에_실패함(self):
        url = reverse_lazy("token:post")   
        response = self.client.post(url)        
        self.assertEquals(response.status_code, 403)
        
    def test_GET_접근에_성공함(self):
        url = reverse_lazy("token:get")
        print(url)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        
    def test_SIGNIN에_로그인정보없이_접근_실패함(self):
        url = reverse_lazy("token:signin")
        data={
            "username":"",
            "password":""
        }
        response = self.client.post(url,content_type='application/json' ,data=json.dumps(data))
        self.assertEquals(response.status_code,403)
        
    def test_SIGNIN에_로그인정보로_접근_성공함(self):
        url = reverse_lazy("token:signin")
        data={
            "username":"admin",
            "password":"1234"
        }
        response = self.client.post(url,content_type='application/json' ,data=json.dumps(data))
        self.assertEquals(response.status_code,200)
        
    def test_SIGNIN_정보가_유효함(self):
        url = reverse_lazy("token:signin")