from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Order, YarnOrderLineitem

@receiver(post_save, sender=YarnOrderLineitem)
def update_on_save(sender, instance, created, **kwargs):
    """
    update order total on line item update or create """
    instance.order.update_order()

@receiver(post_delete, sender=YarnOrderLineitem)
def update_on_delete(sender, instance, **kwargs):
    """
    update order total on line item deletion """
    instance.order.update_order()