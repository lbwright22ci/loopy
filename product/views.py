from django.shortcuts import (render, reverse, redirect,
                              get_object_or_404, HttpResponse)
from django.db.models import Q, Case, When, FloatField, F
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Lower

from .models import Product
from core.models import SaleSettings, UserProfile
from checkout.models import ReviewYarns

# Create your views here.


def AllProducts(request):
    """
    Displays all instances of :model:`Product` based on Queryset.
    Only products with field 'visible = True' are shown.

    Queryset filters available are:
    'q', 'brand', 'thickness', 'fibre', 'price', 'sale',
    'natural', 'machine_wash'
    'natural'

    Sorting available by:
    'price' and 'name'

    Authenticated users can view their 'wish_list' and update it.

    **Template**
    'product/all-products.html'

    **Context**
    'favourite_list'
    'product_list'
    'current_brand'
    'current_thickness'
    'current_fibres'
    'current_prices'
    'sales'
    'natural'
    'machine_wash'
    'current_query'
    'current_sorting'
    """
    queryset = Product.objects.all()
    product_list = queryset

    query = None

    brands = None
    sales = None
    thicknesses = None
    fibres = None
    prices = None
    natural_yarn = None
    machine_wash = None

    sort = None
    direction = None

    discount_adjust = (
        100 - SaleSettings.objects.filter(active=True)[0].sale_percent) / 100

    if request.GET:
        if 'sort' in request.GET:
            sortparam = request.GET['sort']
            sort = sortparam
            if sortparam == 'name':
                sortparam = 'lower_name'
                product_list = product_list.annotate(lower_name=Lower('name'))
            if sortparam == 'price':
                sortparam = 'corrected_price'
                product_list = product_list.annotate(
                    corrected_price=Case(
                        When(
                            on_promotion=True,
                            then=(
                                F('price') *
                                discount_adjust)),
                        default=(
                            F('price')),
                        output_field=FloatField()))
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortparam = f'-{sortparam}'
            product_list = product_list.order_by(sortparam)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.add_message(
                    request, messages.ERROR, "There was nothing \
                        in your search request")

                return redirect(reverse('allproducts'))
            queries = Q(
                name__icontains=query) | Q(
                fibre__icontains=query) | Q(
                thickness_id__name__icontains=query) | Q(
                thickness_id__alt_names__icontains=query) | Q(
                    brand_id__name__icontains=query)
            product_list = product_list.filter(queries)
        if 'brand' in request.GET:
            brands = request.GET['brand']
            product_list = product_list.filter(
                brand_id__name__icontains=brands)
        if 'thickness' in request.GET:
            thicknesses = request.GET['thickness']
            product_list = product_list.filter(
                thickness_id__name__icontains=thicknesses)
        if 'fibre' in request.GET:
            fibres = request.GET['fibre']
            product_list = product_list.filter(fibre__icontains=fibres)
        if 'price' in request.GET:
            prices = request.GET['price']

            if prices == '(0,2)':
                pp = (Q(price__range=(0.0, 2.00)) & Q(on_promotion=False)) | (Q(price__range=(
                    0.01 / discount_adjust, 2.00 / discount_adjust)) & Q(on_promotion=True))
                product_list = product_list.filter(pp)

            elif prices == '(2,4)':
                pp = (Q(price__range=(2.01, 4.00)) & Q(on_promotion=False)) | (Q(price__range=(
                    2.01 / discount_adjust, 4.00 / discount_adjust)) & Q(on_promotion=True))
                product_list = product_list.filter(pp)

            elif prices == '(4,6)':
                pp = (Q(price__range=(4.01, 6.00)) & Q(on_promotion=False)) | (Q(price__range=(
                    4.01 / discount_adjust, 6.00 / discount_adjust)) & Q(on_promotion=True))
                product_list = product_list.filter(pp)

            elif prices == '(6,10)':
                pp = (Q(price__range=(6.01, 10.00)) & Q(on_promotion=False)) | (Q(price__range=(
                    6.01 / discount_adjust, 10.00 / discount_adjust)) & Q(on_promotion=True))
                product_list = product_list.filter(pp)

            elif prices == '(10,20)':
                pp = (Q(price__range=(10.01, 100.00)) & Q(on_promotion=False)) | (
                    (Q(price__range=(
                        10.01 / discount_adjust, 100.00 / discount_adjust))) & (
                        Q(on_promotion=True)))
                product_list = product_list.filter(pp)

        if 'sale' in request.GET:
            sales = True
            product_list = product_list.filter(on_promotion=True)
        if 'natural' in request.GET:
            natural_yarn = True
            product_list = product_list.filter(natural_fibres=True)
        if 'machine_wash' in request.GET:
            machine_wash = True
            product_list = product_list.filter(machine_wash=True)

    current_sorting = f'{sort}_{direction}'

    fav_list = []

    if request.user.is_authenticated:
        current_user = get_object_or_404(UserProfile, user__id=request.user.id)
        fave_list = current_user.wish_list

        if fave_list:
            # convert str to list
            fav_list = fave_list.split()
            fav_list = [int(f) for f in fav_list]

    context = {
        'favourite_list': fav_list,
        'product_list': product_list,
        'current_brand': brands,
        'current_thickness': thicknesses,
        'current_fibres': fibres,
        'current_prices': prices,
        'sales': sales,
        'natural': natural_yarn,
        'machine_wash': machine_wash,
        'current_query': query,
        'current_sorting': current_sorting,
    }
    template = 'product/all-products.html'

    return render(request, template, context)


def ProductDetail(request, slug):
    """
    Displays single instance of :model:`Product`

    **Template**
    'product/product-detail.html'

    **Context**
    'prod' : instance of :model:`Product`
    'colour_options' : instances of :model:`Colour_var`
    related to selected :model:`Product`
    'no_colours'
    'recommend' : different yarns with the same thickness as the one detailed.
    'favourite' : related to instance of :model:`UserProfile` field `wish_list`
    """
    queryset = Product.objects.filter(visible=True)
    prod = get_object_or_404(queryset, slug=slug)
    colour_options = prod.product.filter(in_stock=True).order_by('shade_code')
    no_colours = colour_options.count()
    recommend = Product.objects.filter(
        thickness_id=prod.thickness_id).order_by('price')[0:3]
    reviews = ReviewYarns.objects.filter(
        yarn__product_id=prod).order_by('-updated_on')

    favourite = False

    if request.user.is_authenticated:
        current_user = UserProfile.objects.get(user__id=request.user.id)
        fave_list = current_user.wish_list

        if fave_list:
            fav_list = fave_list.split()
            if str(prod.pk) in fav_list:
                favourite = True
        else:
            favourite = False

    template = "product/product-detail.html"
    context = {
        'prod': prod,
        'colour_options': colour_options,
        'no_colours': no_colours,
        'recommend': recommend,
        'favourite': favourite,
        'reviews': reviews,
    }

    return render(request, template, context)


@login_required
def update_wishlist(request, prod_id):
    """
    Adds or removes instance of :model:`Product` to the authenticated instance
    of :model:`UserProfile` field 'wish_list'
    """
    if request.user.is_authenticated:
        current_user = UserProfile.objects.get(user__id=request.user.id)
        fave_list = current_user.wish_list

        if fave_list:
            # convert str to list
            fav_list = fave_list.split()
        else:
            fav_list = []

        if str(prod_id) in fav_list:
            fav_list.remove(str(prod_id))
            fave_list = ' '.join([str(s) for s in fav_list])
            current_user.wish_list = fave_list
            current_user.save()
            product = Product.objects.get(pk=prod_id)
            messages.add_message(
                request, messages.SUCCESS, f'Removed {
                    product.brand_id.name} {
                    product.name} from your favourites list')
        else:
            fav_list.append(str(prod_id))
            fave_list = ' '.join([str(s) for s in fav_list])
            current_user.wish_list = fave_list
            current_user.save()
            product = Product.objects.get(pk=prod_id)
            messages.add_message(
                request, messages.SUCCESS, f'Added {
                    product.brand_id.name} {
                    product.name} to your favourites list')

    return HttpResponse(status=200)
