from django.contrib import admin
from .models import Product, Colour_var


# Register your models here.

class ColourVarAdmin(admin.TabularInline):
    model = Colour_var
    readonly_fields = ['colour_cat_id', 'product_id', 'shade_code']


@admin.action(description="On promotion")
def onsale(modeladmin, request, queryset):
    """ Bulk action to update products to sale pricing"""
    queryset.update(on_promotion=True)


@admin.action(description="Off promotion")
def offsale(modeladmin, request, queryset):
    """ Bulk action to update products to remove sale pricing"""
    queryset.update(on_promotion=False)


@admin.action(description="Add to shop front")
def visible(modeladmin, request, queryset):
    """ Bulk action to update products to show on shop front"""
    queryset.update(visible=True)


@admin.action(description="Remove from shop front")
def draft(modeladmin, request, queryset):
    """ Bulk action to update products to remove from shop front"""
    queryset.update(visible=False)


class ProductAdmin(admin.ModelAdmin):
    """
    Displays instances of :model:`Product` in the Django admin panel
    for editing, creating new and updating.

    Fields in list display are: 'brand', 'name', 'thickness', 'fibre',
    'price', 'on_promotion', 'visible'
    Instances can be filtered by 'on_promotion', 'visible' and 'brand'
    Instances can be searched by 'name', 'fibre' and 'price'

    Instances can be updated in bulk to change their 'on_promotion'
    and 'visible' statuses.
    """
    inlines = (ColourVarAdmin,)
    list_display = ('brand_id', 'name', 'thickness_id',
                    'fibre', 'price', 'on_promotion', 'visible',)
    list_editable = ('price',)
    list_display_links = ('name',)
    list_filter = ('on_promotion', 'visible', 'brand_id')
    search_fields = ['name', 'fibre', 'price',]
    actions = [onsale, offsale, draft, visible,]


admin.site.register(Product, ProductAdmin)


@admin.action(description="Mark as low stock")
def low_stock(modeladmin, request, queryset):
    """ Bulk action to update yarn shade to low stock status"""
    queryset.update(low_stock=True)


@admin.action(description="Remove low stock restriction")
def normal_stock(modeladmin, request, queryset):
    """ Bulk action to update yarn shade to remove low stock status"""
    queryset.update(low_stock=False)


@admin.action(description="Mark as in stock")
def available(modeladmin, request, queryset):
    """ Bulk action to update yarn shade to in stock"""
    queryset.update(in_stock=True)


@admin.action(description="Mark as out of stock")
def outofstock(modeladmin, request, queryset):
    """ Bulk action to update yarn shade to out of stock"""
    queryset.update(in_stock=False)


@admin.register(Colour_var)
class ColourVariantAdmin(admin.ModelAdmin):
    """
    Displays all instances of :model:`Colour_var` for
    editing and updating.

    Fields in list display are: 'product_id', 'colour_cat_id',
    'low_stock', 'in_stock'
    List display can be filtered by 'low_stock', 'in_stock'
    List display can be searched by 'product_id', 'colour_cat_id'
    Instances can be updated in bulk according to their
    'low stock' and 'in stock' statuses.
    """
    model = Colour_var
    list_display = ('product_id', 'colour_cat_id', 'low_stock', 'in_stock',)
    search_fields = ['product_id__name', 'colour_cat_id__colour_name',]
    list_filter = ('low_stock', 'in_stock',)
    list_editable = ('low_stock', 'in_stock',)
    actions = [outofstock, available, low_stock, normal_stock,]
