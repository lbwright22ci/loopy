from django.contrib import admin
from .models import Product, Colour_var

# Register your models here.

class ColourVarAdmin(admin.TabularInline):
    model = Colour_var
    readonly_fields =['colour_cat_id', 'product_id', 'shade_code']

@admin.action(description="on promotion")
def onsale(modeladmin, request, queryset):
    """ Bulk action to update products to sale pricing"""
    queryset.update(on_promotion=True)

@admin.action(description="off promotion")
def offsale(modeladmin, request, queryset):
    """ Bulk action to update products to remove sale pricing"""
    queryset.update(on_promotion=False)

@admin.action(description="add to shop front")
def visible(modeladmin, request, queryset):
    """ Bulk action to update products to show on shop front"""
    queryset.update(visible=True)

@admin.action(description="remove from shop front")
def draft(modeladmin, request, queryset):
    """ Bulk action to update products to remove from shop front"""
    queryset.update(visible=False)

class ProductAdmin(admin.ModelAdmin):
    """
    Displays instances of :model:`Product` in the Django admin panel for editing, creating new and updating.
    
    Fields in list display are: 'brand', 'name', 'thickness', 'fibre', 'price', 'on_promotion', 'visible'
    Instances can be filtered by 'on_promotion', 'visible' and 'brand'
    Instances can be searched by 'brand_id', 'name', 'fibre' and 'price'

    Instances can be updated in bulk to change their 'on_promotion' and 'visible' statuses.
    """
    inlines = (ColourVarAdmin,)
    list_display =('brand_id', 'name', 'thickness_id', 'fibre', 'price', 'on_promotion', 'visible',)
    list_editable = ('price',)
    list_display_links =('name',)
    list_filter =('on_promotion', 'visible', 'brand_id')
    search_fields= ['brand_id', 'name', 'fibre', 'price',]
    actions=[ onsale, offsale, draft, visible,]

admin.site.register(Product, ProductAdmin)
