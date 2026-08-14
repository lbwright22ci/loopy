from django.urls import path
from . import views

urlpatterns = [
    path('', views.management_home, name ="management_home"),
    path('orders/', views.management_orders, name="management_orders"),
    path('settings/', views.management_settings, name="management_settings"),
    path('settings/address', views.update_shopsettings, name="update_shopsettings"),
    path('settings/promo', views.update_announcements, name ="update_announcements"),
    path('settings/sale', views.update_salesettings, name="update_salesettings"),
]