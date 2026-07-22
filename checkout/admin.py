from django.contrib import admin
from .models import Order, YarnOrderLineitem
# Register your models here.

class YarnOrderLineItemAdmin(admin.TabularInline):
    model= YarnOrderLineitem
    readonly_fields =['current_price', 'linetotal', 'lineweight',]

class OrderAdmin(admin.ModelAdmin):
    inlines = (YarnOrderLineItemAdmin,)


admin.site.register(Order, OrderAdmin)