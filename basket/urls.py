from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_basket, name="view_basket"),
    path('add/', views.add_to_basket, name='add_to_basket'),
    path('update/<int:item_id>', views.update_basket, name="update_basket"),
]