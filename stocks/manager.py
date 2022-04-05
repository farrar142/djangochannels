from .models import Product
class ProductManager:
    def __init__(self,product_id):
        self.product = Product.objects.get(pk=1)