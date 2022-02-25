from datetime import timedelta
import json
from django.test import TestCase
from django.urls import reverse, reverse_lazy
from django.test.utils import override_settings
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.conf import settings

from .models import Token

PASSWORDS = "test"

class TokenAPITests(TestCase):
    
    def gen_users(cls):
        user = get_user_model()
        user(username="admin",password=make_password(PASSWORDS),email="gksdjf1690@gmail.com",is_superuser=True,is_staff=True).save()
        user(username="test",password=make_password(PASSWORDS),email="test@gmail.com",is_superuser=True,is_staff=True).save()
        for i in range(5):
            user(username=f"test{i}",password=make_password("12334"),email=f"test{i}@gmail.com").save()
    ##미들웨어스타트
    
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
        print("test_SIGNIN에_로그인정보없이_접근_실패함")
        url = reverse_lazy("token:signin")
        data={
            "username":"",
            "password":""
        }
        response = self.client.post(url,content_type='application/json' ,data=json.dumps(data))
        self.assertEquals(response.status_code,403)
    ##미들웨어 엔드
    
    ##로직에서 구현해야 되는 것.
    def test_SIGNIN_정보가_유효하지않음(self):
        print("test_SIGNIN_정보가_유효하지않음")
        self.gen_users()
        url = reverse_lazy("token:signin")
        data={
            "username":"admin",
            "password":"asd"
        }
        response = self.client.post(url,content_type='application/json' ,data=json.dumps(data))
        self.assertEquals(response.status_code,403)
    ##로직 엔드    
    
    ##미들웨어 스타트
    def test_SIGNIN_정보가_유효하고_토큰이_없을시_발급(self):
        print("test_SIGNIN_정보가_유효하고_토큰이_없을시_발급")
        self.gen_users()
        url = reverse_lazy("token:signin")
        data={
            "username":"admin",
            "password":PASSWORDS
        }
        response = self.client.post(url,content_type='application/json' ,data=json.dumps(data))

        self.assertEquals(response.status_code,200)
        self.assertEquals(Token.objects.all().count(),1)
        
    def test_SIGNIN_정보가_유효하고_토큰이_유효할시_통과하고_만료연장(self):
        print("test_SIGNIN_정보가_유효하고_토큰이_유효할시_통과하고_만료연장")
        self.gen_users()
        token = Token.token_factory(get_user_model().objects.all().first().pk)
        token.expired_in = timezone.now() - timedelta(minutes=30)
        token.save()
        
        url = reverse_lazy("token:signin")
        data={
            "username":"admin",
            "password":PASSWORDS
        }
        response = self.client.post(url,content_type='application/json' ,data=json.dumps(data))
        
        tokens = Token.objects.all()
        self.assertEquals(response.status_code,200)
        self.assertEquals(tokens.count(),1)
        self.assertGreaterEqual(tokens.first().expired_in,timezone.now()+timedelta(minutes=50))
        
    def test_SIGNIN_정보가_유효하고_토큰이_만료되었을시_재발급(self):
        print("test_SIGNIN_정보가_유효하고_토큰이_만료되었을시_재발급")
        self.gen_users()
        token = Token.token_factory(get_user_model().objects.all().first().pk)
        token.expired_in -= timedelta(hours=5)
        token.save()
        url = reverse_lazy("token:signin")
        data={
            "username":"admin",
            "password":PASSWORDS
        }
        response = self.client.post(url,content_type='application/json' ,data=json.dumps(data))
        
        self.assertEquals(response.status_code,200)
        self.assertEquals(Token.objects.all().count(),1)
        
    def test_토큰으로_POST_페이지_접속_성공(self):
        print("test_토큰으로_POST_페이지_접속_성공")
        self.gen_users()
        token:Token = Token.token_factory(get_user_model().objects.all().first().pk)        
        cookies={
            "token":token.token
            }
        url = reverse_lazy("token:another_post")   
        self.client.cookies.load(cookies)
        print(self.client.cookies)
        response = self.client.post(url)        
        self.assertEquals(response.status_code, 200)
        self.assertEquals(Token.objects.all().count(),1)
    
    def test_하지만_토큰없인_못들어간다(self):
        print("test_하지만_토큰없인_못들어간다")
        self.gen_users()
        url = reverse_lazy("token:another_post")   
        print(self.client.cookies)
        response = self.client.post(url)        
        self.assertEquals(response.status_code, 403)
        self.assertEquals(Token.objects.all().count(),0)
        
        
    def test_만료된_토큰은_삭제후_접근거부(self):
        print("만료된_토큰은_삭제후_접근거부")
        self.gen_users()
        token:Token = Token.token_factory(get_user_model().objects.all().first().pk) 
        token.expired_in -= timedelta(hours=5)
        token.save()       
        cookies={
            "token":token.token
            }
        url = reverse_lazy("token:another_post")   
        self.client.cookies.load(cookies)
        print(self.client.cookies)
        response = self.client.post(url)        
        self.assertEquals(response.status_code, 403)
        self.assertEquals(Token.objects.all().count(),0)
        
    def test_body로_오는_json_토큰도_받을_수_있어야_됨(self):
        print("test_body로_오는_json_토큰도_받을_수_있어야_됨")
        self.gen_users()
        token:Token = Token.token_factory(get_user_model().objects.all().first().pk)   
        data={
            "token":token.token
            }
        url = reverse_lazy("token:another_post")   
        response = self.client.post(url,content_type='application/json' ,data=json.dumps(data))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(Token.objects.all().count(),1)