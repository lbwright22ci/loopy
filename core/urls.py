from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home_page, name="home"),
    path('my_account/', views.customer_account, name="customer_account"),
    path('my_account/update_details/', views.update_details, name="update_details"),
    path('my_account/update_address/', views.update_address, name="update_address"),
]