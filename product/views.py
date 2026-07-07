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
    brands = None
    sales = None
    thicknesses = None
    fibres = None
    colours = None

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
        if 'brand' in request.GET:
            brands = request.GET['brand']
            product_list = product_list.filter(brand_id__name__in=brands)
            brands = Brand.objects.filter(name__in=brands)
        if 'thickness' in request.GET:
            thicknesses = request.GET['thickness']
            product_list = product_list.filter(thickness_id__name__icontains=thicknesses)
            thicknesses = Thickness.objects.filter(name__in=thicknesses)
        if 'fibre' in request.GET:
            fibres = request.GET['fibre'].split(',')
            product_list = product_list.filter(fibre__in=fibres)
            fibres = Product.objects.filter(fibre__icontains=fibres)
        if 'colour' in request.GET:
            colours = request.GET['colour'].split(',')
            product_list = set(product_list.filter(product__colour_cat_id__shade_type_id__name__in=colours))
            colours = Shade_Type.objects.filter(name__in=colours)
        if 'sale' in request.GET:
            sales = True
            product_list = product_list.filter(on_promotion=True)

    context={
        'product_list':product_list,
        'form':form,
        'current_brand':brands,
        'current_thickness':thicknesses,
        'current_fibres':fibres,
        'current_colours':colours,
        'sales':sales,
    }
    template = 'product/all-products.html'

    return render(request, template, context)