from django.shortcuts import render
from django.db.models import Q

from django_filters.views import FilterView

from .models import Product, Colour_cat, Colour_var, Brand, Thickness, Shade_Type
from .filters import YarnFilter


# Create your views here.

def AllProducts(request):
    """" """
    product_list = Product.objects.filter(visible=True)
    form = YarnFilter().form
    query = None
    filters= None
    sort = None
    direction = None

    if request.GET:

        if 'extended-filter' in request.GET:
            filters = YarnFilter(request.GET, queryset=Product.objects.filter(visible=True))
            product_list = filters.qs
            form = filters.form

    context={
        'product_list':product_list,
        'form':form,
    }
    template = 'product/all-products.html'

    return render(request, template, context)