from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.AllProductsListView.as_view(), name="allproducts"),
]