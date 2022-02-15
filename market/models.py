from django.db import models
from products.models import Product
from commons.models import *
from mysite.const import *
# Create your models here.
class TradeOrder(AsyncModel):
    asset = models.ForeignKey('accounts.asset',on_delete=models.CASCADE,related_name='tradeorder')
    code = models.ForeignKey(Code,on_delete=models.DO_NOTHING)
    type = models.ForeignKey(Type,on_delete=models.DO_NOTHING)
    fee = models.IntegerField('수수료',default=0)
    reg_date = models.DateTimeField('게시날짜', auto_now_add=True)
    update_date = models.DateTimeField('수정날짜', auto_now_add=True)
    
    @classmethod
    def custom_create(cls,*args,**kwargs):
        t_dict = kwargs.copy()
        t_dict.pop('point')
        t_dict.pop('quantity')
        t_dict.update(code_id=1)
        
        tradeorder = cls(**t_dict)
        tradeorder.save()
        
        quantity:int = kwargs['quantity']
        point:int = kwargs['point']
        type_id:int = kwargs['type_id']
        #method1 
        #1 insert per 1 quantity
        # for i in range(0,quantity):
        #     TradeItem(tradeorder=tradeorder,code_id=NORMAL,type_id=type_id,point=point).save()
        #method2
        #1 isnert per any quantity, but cannot use save method
        my_trades_list = TradeItem.objects.bulk_create(
            [TradeItem(tradeorder=tradeorder,code_id=NORMAL,type_id=type_id,point=point) for i in range(0,quantity) ]
        )#filter나all()은 queryset을 반환하지만 이놈은 TradeItem이 담긴 List를반환
        
        #만들어진 list와 db모델의 id를 동기화 시키기위해 id만 추출해옴
        my_ids = [i.id for i in my_trades_list]
        #print(type(test[0]),test)
        if type_id==BUY:
            cls.update_logic(SELL,point,quantity,my_ids)
        if type_id==SELL:
            cls.update_logic(BUY,point,quantity,my_ids)
        return tradeorder
    @classmethod
    def update_logic(self,CODE,point,quantity,my_ids):
            #quantity만큼 가져와서 count를함.
            targets = TradeItem.objects.filter(
                    code_id=NORMAL,type_id=CODE,point=point,                
                    ).order_by('reg_date')[:quantity]
            #장고orm에서업데이트
            for i in targets:
                i.code_id = COMPLETE
            #code_id를 db에 업데이트함과 동시에 update가 이뤄진 개수를 리턴받음
            count = TradeItem.objects.bulk_update(targets,['code_id'])
            #자기가 가진 id중에서 업데이트가 이루어진 target갯수만큼을 가져옴
            my_trades = TradeItem.objects.filter(id__in = my_ids)[:count]
            for i in my_trades:
                i.code_id = COMPLETE
            TradeItem.objects.bulk_update(my_trades,['code_id'])
        
        
class TradeItem(AsyncModel):
    tradeorder = models.ForeignKey(TradeOrder,on_delete=models.CASCADE,related_name='tradeitem')
    code = models.ForeignKey(Code,on_delete=models.DO_NOTHING)
    type = models.ForeignKey(Type,on_delete=models.DO_NOTHING)
    point = models.IntegerField('거래가격')
    reg_date = models.DateTimeField('게시날짜', auto_now_add=True)
    
    
    def trade_save(self):
        """
        1 .매입을 걸어 놓을 시 소유자의 현금이 까여야됨.
        2. 자신이 구매라면
            1. 가격대가맞는 판매가있는지
            2. 맞다면 그중에서 제일 오래된 SELL,COMPLETE거래를가져옴
        3. 자신이 판매라면
            1. 최저가인지
            2. 제일오래되었는지
        buy,sell을 반환받고 둘의 상태를 COMPLETE로전환
        """
        self.save()
        if self.type_id==BUY:
            target = TradeItem.objects.filter(
                code_id=NORMAL,type_id=SELL,point=self.point,                
                ).order_by('reg_date').first()