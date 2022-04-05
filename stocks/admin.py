from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Product)
admin.site.register(ProductLog)

admin.site.register(Product_Category)