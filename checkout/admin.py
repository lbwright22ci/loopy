from django.contrib import admin
from .models import Order, YarnOrderLineitem
# Register your models here.

class YarnOrderLineItemAdmin(admin.TabularInline):
    model= YarnOrderLineitem
    readonly_fields =['current_price', 'linetotal', 'lineweight',]

class OrderAdmin(admin.ModelAdmin):
    inlines = (YarnOrderLineItemAdmin,)
    readonly_fields=['order_subtotal', 'grand_total', 'order_discount', 'postage_cost', 'parcel_size', 'order_num',
                     'amount_payable',]


admin.site.register(Order, OrderAdmin)