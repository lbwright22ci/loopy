from django.contrib import admin
from .models import Order, YarnOrderLineitem, ReviewYarns, Refund, Shipped
# Register your models here.


class YarnOrderLineItemAdmin(admin.TabularInline):
    model = YarnOrderLineitem
    readonly_fields = ['current_price', 'linetotal', 'lineweight',]


class RefundAdmin(admin.TabularInline):
    model = Refund
    readonly_fields = ['refund_id', 'amount', 'order']


class ShippedAdmin(admin.TabularInline):
    model = Shipped
    readonly_fields = ['dispatched_on', 'order']


class OrderAdmin(admin.ModelAdmin):
    """ Displays instances of :model:`ReviewYarns` in the Django admin panel for editing, creating new and updating.

    Fields in list display are: 'created_on', 'first_name', 'second_name', 'parcel_size', 'postage_class', 'grand_total',
    'is_shippped', 'refund_status'
    Instances can be filtered by 'is_shipped' and 'refund_status' statuses
    Instances can be searched by 'email', 'order_num', 'second_name'
    """
    inlines = (RefundAdmin, ShippedAdmin)
    list_filter = ('is_shipped', 'refund_status')
    list_display = ('created_on', 'first_name', 'second_name', 'parcel_size',
                    'postage_class', 'grand_total', 'is_shipped', 'refund_status',)
    search_fields = ['email', 'order_num', 'second_name',]
    readonly_fields = ['order_subtotal', 'grand_total', 'order_discount', 'postage_cost', 'parcel_size', 'order_num',
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
    """ Displays instances of :model:`ReviewYarns` in the Django admin panel for editing, creating new and updating.

    Fields in list display are: 'updated_on', 'yarn', 'rating', 'approved'
    Instances can be filtered by 'approved' and 'rating' statuses

    Instances can be updated in bulk to change their 'approved' status."""
    list_display = ('updated_on', 'yarn', 'rating', 'approved')
    list_filter = ('approved', 'rating',)
    actions = [approve, remove_approval]
