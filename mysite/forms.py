from ninja import Schema

class ProductForm(Schema):
    name : str
    category_id : int

class Trade_OrderForm(Schema):
    product_id : int
    point : int
    amount : int
    type_id : int
    fake_token : str = "admin"
    
class Asset_ItemForm(Schema):
    user_id : int
    product_id : int
    point : int
    code_id : int
    type_id : int
    trade_order : Trade_OrderForm = None
