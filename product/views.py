from django.shortcuts import render, reverse, redirect
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator

from .models import Product
from .filters import YarnFilter


# Create your views here.

def AllProducts(request):
    """" """
    product_list = YarnFilter(request.GET, queryset=Product.objects.all()).qs
    form = YarnFilter(request.GET, queryset=Product.objects.all()).form

    query = None
    filters= None
    brands = None
    sales = None
    thicknesses = None
    fibres = None
    colours = None
    natural_yarn= None

    sort = None
    direction = None

    
    # if 'q' in request.GET:
    #     query = request.GET['q']
    #     if not query:
    #         messages.add_message(
    #         request, messages.ERROR, "There was nothing in your search request")
    #         return redirect(reverse('allproducts'))            
    #     queries = Q(name__icontains=query) | Q(fibre__icontains=query) | Q(thickness_id__name__icontains=query)| Q(thickness_id__alt_names__icontains = query) | Q(brand_id__name__icontains=query)
    #     product_list = product_list.filter(queries)
    # elif 'brand' in request.GET:
    #     brands = request.GET['brand']
    #     product_list = product_list.filter(brand_id__name__icontains=brands)
    # elif 'thickness' in request.GET:
    #     thicknesses = request.GET['thickness']
    #     product_list = product_list.filter(thickness_id__name__icontains=thicknesses)
    # elif 'fibre' in request.GET:
    #     fibres = request.GET['fibre']
    #     product_list = product_list.filter(fibre__icontains=fibres)
    # elif 'colour' in request.GET:
    #     colours = request.GET['colour'].split(',')
    #     product_list = set(product_list.filter(product__colour_cat_id__shade_type_id__name__in=colours))
    # elif 'sale' in request.GET:
    #     sales = True
    #     product_list = product_list.filter(on_promotion=True)
    # elif 'natural' in request.GET:
    #     natural_yarn = True
    #     product_list= product_list.filter(natural_fibres=True)
    # elif 'brand_id' in request.GET:
    #     product_list=YarnFilter(request.GET,queryset=Product.objects.all()).qs
    # filters = YarnFilter(request.GET, queryset=Product.objects.all())
    
    # form = YarnFilter(request.GET,queryset=Product.objects.all()).form

    print(request.GET)

    paginator = Paginator(product_list,12)
    page_number= request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context={
        'product_list':product_list,
        'form':form,
        'current_brand':brands,
        'current_thickness':thicknesses,
        'current_fibres':fibres,
        'current_colours':colours,
        'sales':sales,
        'natural':natural_yarn,
        'current_query':query,
        'page_obj':page_obj,
    }
    template = 'product/all-products.html'

    return render(request, template, context)