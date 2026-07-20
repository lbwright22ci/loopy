from django.urls import path
from . import views

urlpatterns = [
    path('', views.OrderForms.as_view(), name="checkout"),
]