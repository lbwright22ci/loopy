from django.shortcuts import render, reverse, redirect
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
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "There was nothing in your search request")
                return redirect(reverse('allproducts'))
            
            queries = Q(name__icontains=query) | Q(fibre__icontains=query) | Q(thickness_id__name__icontains=query)| Q(thickness_id__alt_names__icontains = query) | Q(brand_id__name__icontains=query)
            product_list = product_list.filter(queries)


    context={
        'product_list':product_list,
        'form':form,
    }
    template = 'product/all-products.html'

    return render(request, template, context)