from django.urls import path
from . import views

urlpatterns = [
    path('', views.AllProducts, name="allproducts"),
    path('<slug:slug>/', views.ProductDetail, name="productdetail"),
    path('fav/<prod_id>/', views.update_wishlist, name="update_wishlist"),
]
