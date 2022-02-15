from django.urls import path
from . import views

app_name = "market"

urlpatterns = [
    path("<str:product_name>/",views.chart,name="chart"),
    path("<str:product_name>/trade",views.make_trade,name="make")
]
