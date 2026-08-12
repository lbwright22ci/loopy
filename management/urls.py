from django.urls import path
from . import views

urlpatterns = [
    path('', views.management_home, name ="management_home"),
    path('orders/', views.management_orders, name="management_orders"),
    path('products/', views.management_products, name ="management_products"),
    path('settings/', views.management_settings, name="management_settings"),
]