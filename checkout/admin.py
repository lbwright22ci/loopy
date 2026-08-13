from django.contrib import admin
from .models import Order, YarnOrderLineitem, ReviewYarns, Refund
# Register your models here.

class YarnOrderLineItemAdmin(admin.TabularInline):
    model= YarnOrderLineitem
    readonly_fields =['current_price', 'linetotal', 'lineweight',]

class RefundAdmin(admin.TabularInline):
    model= Refund

class OrderAdmin(admin.ModelAdmin):
    inlines = (RefundAdmin,  )
    readonly_fields=['order_subtotal', 'grand_total', 'order_discount', 'postage_cost', 'parcel_size', 'order_num',
                     'amount_payable',]

admin.site.register(Order, OrderAdmin)

@admin.action(description="Approve")
def approve(modeladmin, request, queryset):
    """ Bulk action to update reviews to approved for publication"""
    queryset.update(approved=True)

@admin.action(description="Reject")
def remove_approval(modeladmin, request, queryset):
    """ Bulk action to update reviews to unapproved for publication"""
    queryset.update(approved=False)

@admin.register(ReviewYarns)
class ReviewYarnsAdmin(admin.ModelAdmin):
    """ """

    list_display = ('updated_on', 'yarn', 'rating', 'approved')
    list_filter = ('approved', 'rating',)
    actions = [approve, remove_approval]
