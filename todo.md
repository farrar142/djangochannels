[o]1. 현재는 장고 orm에서 쿼리해와서 기존 거래 기록을 뿌려줌.
[o]2. 이를 웹소켓에 접속!(accept)할때 ,거래가 성사(receive)될때! 쿼리하도록 바꿀예정.

[]3. 에셋-트레이드 간의 로직, 거래로직 필요
###구매하는 쪽은 판매쪽의 가장오래된 regdate를 가지는 trade에서 quantity를 차감후  asset으로 전환
###판매하는 쪽은 자신의 asset을 trade로 전환
#market.models.Trade.trade_logic 수정요
#
[]4. 프론트/백엔드 로그인구현

[]5. 스케쥴러를 이용해 Product를 ProductLog로 migrate


    def gen_users(App,Scheme_editor):
        User(username="admin",password=make_password(PASSWORDS),email="gksdjf1690@gmail.com",is_superuser=True,is_staff=True).save()
        User(username="test",password=make_password(PASSWORDS),email="test@gmail.com",is_superuser=True,is_staff=True).save()
        for i in range(5):
            User(username=f"test{i}",password=make_password("12334"),email=f"test{i}@gmail.com").save()
    
    def gen_products(app,scheme_editor):
        categories = ["IT","건축","토목","기계","전기","회계","교육","유통","방송","화학","제조","대부"]
        for i in categories:
            Product_Category(name=i).save()
        names = ["삼선중공업","구아바톡","식인펠리컨","배달의만족","카사바마켓"]
        categories = Product_Category.objects.all()
        for name in names:
            Product(name=name,category=random.choice(categories)).save()


docker restart daphne && docker logs --tail 10 -f daphne

docker exec -it daphne bash
python3 manage.py runserver 0.0.0.0:8021
https://americanopeople.tistory.com/category/%EC%86%8C%ED%94%84%ED%8A%B8%EC%9B%A8%EC%96%B4-%EC%9D%B4%EC%95%BC%EA%B8%B0/%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%98%EB%B0%8D%20%EC%96%B8%EC%96%B4%EC%99%80%20%ED%94%84%EB%A0%88%EC%9E%84%EC%9B%8C%ED%81%AC