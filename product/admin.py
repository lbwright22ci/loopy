from django.contrib import admin
from .models import Product, Colour_var

# Register your models here.

class ColourVarAdmin(admin.TabularInline):
    model = Colour_var
    readonly_fields =['colour_cat_id', 'product_id', 'shade_code']

class ProductAdmin(admin.ModelAdmin):
    inlines = (ColourVarAdmin,)




admin.site.register(Product, ProductAdmin)
