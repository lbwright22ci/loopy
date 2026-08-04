from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home_page, name="home"),
    path('my_account/', views.customer_account, name="customer_account"),
    path('my_account/past_order/<order_num>/', views.past_order, name="past_order"),
    path('my_account/reorder/', views.reorder, name="reorder"),
    path('my_account/review/<order_num>/', views.leave_review, name="leave_review"),
    path('my_account/review/submit/<order_num>/', views.submit_review, name="submit_review"),
    path('my_account/update_address/', views.update_address, name="update_address"),
    path('my_account/update_details/', views.update_details, name="update_details"),
]