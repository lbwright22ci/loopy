from django.urls import path
from . import views
from .webhooks import webhook

urlpatterns = [
    path(
        'cache_checkout_data/',
        views.cache_checkout_data,
        name="cache_checkout_data"),
    path(
        'step-one/',
        views.checkout_step1,
        name="checkout"),
    path(
        'step-two/',
        views.checkout_step2,
        name='checkout-ship'),
    path(
        'step-three/',
        views.checkout_step3,
        name='checkout-final'),
    path(
        'success/<order_num>/',
        views.checkout_success,
        name="checkout_success"),
    path(
        'cancel/<order_num>/',
        views.Cancel_order,
        name="cancel_order"),
    path(
        'ship/',
        views.mark_shipped,
        name="mark_shipped"),
    path(
        'wh/',
        webhook,
        name="webhook"),
]
