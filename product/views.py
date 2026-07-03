from django.shortcuts import render
from django.views import generic
from .models import Product, Colour_cat, Colour_var, Brand, Thickness, Shade_Type

# Create your views here.

class AllProductsListView(generic.ListView):
    """" """

    model= Product
    paginate_by= 12
    template_name= 'product/all-products.html'