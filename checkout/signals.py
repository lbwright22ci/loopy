from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import YarnOrderLineitem

@receiver(post_save, sender=YarnOrderLineitem)
def update_on_save(sender, instance, created, **kwargs):
    """
    Calls 'models.Order.update_order()' when an instance of :model:`YarnOrderLineItem`
    is created or updated.
    """
    instance.order.update_order()

@receiver(post_delete, sender=YarnOrderLineitem)
def update_on_delete(sender, instance, **kwargs):
    """
    Calls 'models.Order.update_order()' when an instance of :model:`YarnOrderLineItem`
    is deleted.
    """
    instance.order.update_order()