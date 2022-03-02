from ninja import Schema

class TokenSchema(Schema):
    token:str="token"
    
    def __init__(schema:Schema,*args,**kwargs):
        super().__init__(*args,**kwargs)
        if schema.dict().get("token"):
            del schema.token
class ProductForm(TokenSchema):
    name : str
    category_id : int

class Trade_OrderForm(TokenSchema):
    product_id : int
    point : int
    amount : int
    type_id : int
    
class Asset_ItemForm(TokenSchema):
    product_id : int
    point : int
    code_id : int
    type_id : int
    trade_order : Trade_OrderForm = None
class Trade_Order_CancelForm(TokenSchema):
    product_id:int