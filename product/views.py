from django.shortcuts import render, reverse, redirect
from django.db.models import Q
from django.contrib import messages

from .models import Product
from core.models import SaleSettings

# Create your views here.

def AllProducts(request):
    """" """
    queryset = Product.objects.all()
    product_list = queryset
    
    query = None

    brands = None
    sales = None
    thicknesses = None
    fibres = None
    prices = None
    natural_yarn= None
    machine_wash=None

    sort = None
    direction = None

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.add_message(
                request, messages.ERROR, "There was nothing in your search request")
                return redirect(reverse('allproducts'))            
            queries = Q(name__icontains=query) | Q(fibre__icontains=query) | Q(thickness_id__name__icontains=query)| Q(thickness_id__alt_names__icontains = query) | Q(brand_id__name__icontains=query)
            product_list = product_list.filter(queries)
        if 'brand' in request.GET:
            brands = request.GET['brand']
            product_list = product_list.filter(brand_id__name__icontains=brands)
        if 'thickness' in request.GET:
            thicknesses = request.GET['thickness']
            product_list = product_list.filter(thickness_id__name__icontains=thicknesses)
            if thicknesses =='2':
                thicknesses = '2 ply'
            elif thicknesses == '3':
                thicknesses = '3 ply'
            elif thicknesses == '4':
                thicknesses = '4 ply'
        if 'fibre' in request.GET:
            fibres = request.GET['fibre']
            product_list = product_list.filter(fibre__icontains=fibres)
        if 'price' in request.GET:
            prices = request.GET['price']
            discount_adjust = (100-SaleSettings.objects.filter(active=True)[0].sale_percent)/100
            if prices =='(0,2)':
                pp = (Q(price__range=(0.0,2.00))&Q(on_promotion=False))|(Q(price__range=(0.01/discount_adjust,2.00/discount_adjust))&Q(on_promotion=True))
                product_list = product_list.filter(pp)
                prices = '0-2'
            elif prices =='(2,4)':
                pp = (Q(price__range=(2.01,4.00))&Q(on_promotion=False))|(Q(price__range=(2.01/discount_adjust,4.00/discount_adjust))&Q(on_promotion=True))
                product_list = product_list.filter(pp)
                prices = '2-4'
            elif prices =='(4,6)':
                pp = (Q(price__range=(4.01,6.00))&Q(on_promotion=False))|(Q(price__range=(4.01/discount_adjust,6.00/discount_adjust))&Q(on_promotion=True))
                product_list = product_list.filter(pp)
                prices = '4-6'
            elif prices =='(6,10)':
                pp = (Q(price__range=(6.01,10.00))&Q(on_promotion=False))|(Q(price__range=(6.01/discount_adjust,10.00/discount_adjust))&Q(on_promotion=True))
                product_list = product_list.filter(pp)
                prices = '6-10'
            elif prices =='(10,20)':
                pp = (Q(price__range=(10.01,100.00))&Q(on_promotion=False))|(Q(price__range=(10.01/discount_adjust,100.00/discount_adjust))&Q(on_promotion=True))
                product_list = product_list.filter(pp)
                prices = '10+'
        if 'sale' in request.GET:
            sales = True
            product_list = product_list.filter(on_promotion=True)
        if 'natural' in request.GET:
            natural_yarn = True
            product_list= product_list.filter(natural_fibres=True)
        if 'machine_wash' in request.GET:
            machine_wash = True
            product_list= product_list.filter(machine_wash=True)
  

    context={
        'product_list':product_list,
        'current_brand':brands,
        'current_thickness':thicknesses,
        'current_fibres':fibres,
        'current_prices':prices,
        'sales':sales,
        'natural':natural_yarn,
        'machine_wash':machine_wash,
        'current_query':query,
    }
    template = 'product/all-products.html'

    return render(request, template, context)