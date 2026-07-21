from django.urls import path
from . import views

urlpatterns = [
    path('step-one/', views.checkout_step1, name="checkout"),
]