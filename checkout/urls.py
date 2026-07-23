from django.urls import path
from . import views

urlpatterns = [
    path('step-one/', views.checkout_step1, name="checkout"),
    path('step-two/', views.checkout_step2, name='checkout-ship'),
    path('step-three/', views.checkout_step3, name='checkout-final'),
    path('success/<order_num>', views.checkout_success, name="checkout_success"),
]