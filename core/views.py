from django.shortcuts import render, reverse, redirect, get_object_or_404, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User

from .models import HomePageSlides, UserProfile
from .forms import AddressForm, DetailsForm
from checkout.models import Order, ReviewYarns
from product.models import Colour_var, Product


# Create your views here.

def home_page(request):
    """
    Renders the home page for the Loopy e-commerce site, displaying 
    the 5 most recently updated instances of :model:`HomePageSlides`

    **Template**
    :template: `home.html`

    **Context**
    ``slides``

    """

    slides = HomePageSlides.objects.all()[0:5]

    template = 'core/home.html'
    context = {'slides': slides, }

    return render(request, template, context)


@login_required
def customer_account(request):
    """
    Renders a page for authenticated Users displaying account information, past orders and 
    their favourites list.

    Displays information related to instance of :model:`UserProfile` and associated instances of 
    :model:`Order`.
    Displays instance of :form:`DetailsForm` and :form:`AddressForm` to enable user to update 
    name & saved phone number and address details respectively.

    **Template**
    'core/account.html'

    **Context**
    `details_form`
    `address_form`
    `favourites`
    `past_orders`
    """
    profile = UserProfile.objects.get(user=request.user)
    past_orders = profile.orders.all().order_by('-created_on')

    details_form = DetailsForm(initial={
        'first_name': profile.user.first_name,
        'last_name': profile.user.last_name,
        'Phone': profile.default_phone,
    })
    address_form = AddressForm(initial={
        'default_street_address1': profile.default_street_address1,
        'default_street_address2': profile.default_street_address2,
        'default_county': profile.default_county,
        'default_country': profile.default_country,
        'default_postcode': profile.default_postcode,
        'default_town': profile.default_town,
    })

    favourite_list = []
    fave_list = profile.wish_list

    if fave_list:
        # convert str to list
        fav_list = fave_list.split()
        for item in fav_list:
            yarn = get_object_or_404(Product, pk=int(item))
            favourite_list.append({
                'prod_id': int(item),
                'yarn': yarn
            })

    context = {
        'favourites': favourite_list,
        'address_form': address_form,
        'details_form': details_form,
        'past_orders': past_orders,
    }
    template = 'core/account.html'

    return render(request, template, context)


@login_required
def update_details(request):
    """"
    Updates 'first_name', 'second_name' and 'default_phone' fields of instance of :model:`UserProfile`
    """
    current_user = UserProfile.objects.get(user__id=request.user.id)
    user = User.objects.get(id=request.user.id)
    try:
        if request.POST:
            details_form = DetailsForm(data=request.POST)

            if details_form.is_valid():
                user.first_name = request.POST.get('first_name')
                user.last_name = request.POST.get('last_name')
                current_user.default_phone = request.POST.get('Phone')
                current_user.save()
                user.save()

                messages.add_message(
                    request, messages.SUCCESS, f'Your account details have been updated!')
    except Exception as e:
        messages.add_message(
            request, messages.ERROR, f'Unable to update your account details. Error message: {e}')

    return redirect(reverse('customer_account'))


@login_required
def update_address(request):
    """"
    Updates 'default_street_address1', 'default_street_address2', 'default_town',
    'default_county', 'default_postcode' and 'default_country' fields of instance of 
    :model:`UserProfile`
    """
    current_user = UserProfile.objects.get(user__id=request.user.id)
    try:
        if request.POST:
            address_form = AddressForm(data=request.POST)
            if address_form.is_valid():
                current_user.default_street_address1 = request.POST.get(
                    'default_street_address1')
                current_user.default_street_address2 = request.POST.get(
                    'default_street_address2')
                current_user.default_town = request.POST.get('default_town')
                current_user.default_county = request.POST.get(
                    'default_county')
                current_user.default_country = request.POST.get(
                    'default_country')
                current_user.default_postcode = request.POST.get(
                    'default_postcode')
                current_user.save()

                messages.add_message(
                    request, messages.SUCCESS, f'Your address details have been updated!')
    except Exception as e:
        messages.add_message(
            request, messages.ERROR, f'Unable to update your address details. Error message: {e}')

    return redirect(reverse('customer_account'))


@login_required
def past_order(request, order_num):
    """
    Displays all information relating to instance of :model:`checkout.models.Order`

    **Template**
    'checkout/past-order.html'

    **Context**
    'order'

    """
    order = get_object_or_404(Order, order_num=order_num)

    context = {
        'order': order,
    }
    template = 'core/past-order.html'

    return render(request, template, context)


def reorder(request):
    """ 
    Adds instance of :model:`product.model.Colour_var` to session basket 
    (and UserProfile.temporary_basket) with 
    the same 'quantity' as in instance of :model:`checkout.model.Order` related to 
    :model:`UserProfile`.

    User is redirected to 'view_basket'
    """

    quantity = int(request.POST.get('quantity'))
    col_var_id = request.POST['colour_var']
    col_var = get_object_or_404(Colour_var, pk=col_var_id)

    basket = request.session.get('basket', {})

    if col_var_id in list(basket.keys()):
        if col_var.low_stock:
            test = basket[col_var_id] + quantity
            if test < 10:
                basket[col_var_id] += quantity

                messages.add_message(request, messages.SUCCESS, f'Updated the quantity of {col_var.product_id.brand_id.name} {col_var.product_id.name},\
                               shade {col_var.colour_cat_id.colour_name} to {test} balls')
            else:
                # can not add to basket- error message and redirect
                messages.add_message(request, messages.ERROR, f'Low stock! Unable to add {quantity} extra \
                               balls of {col_var.product_id.brand_id.name} {col_var.product_id.name}\
                               to your basket.')
                return redirect(reverse('view_basket'))
        else:
            test = basket[col_var_id] + quantity
            if test < 50:
                basket[col_var_id] += quantity
                messages.add_message(request, messages.SUCCESS, f'Updated the quantity of {col_var.product_id.brand_id.name} {col_var.product_id.name},\
                               shade {col_var.colour_cat_id.colour_name} to {test} balls')
            else:

                messages.add_message(request, messages.ERROR, f'Insufficient stock! Unable to add {quantity} extra \
                               balls of {col_var.product_id.brand_id.name} {col_var.product_id.name}\
                               to your basket.')
                return redirect(reverse('view_basket'))

    else:
        basket[col_var_id] = quantity

        messages.add_message(request, messages.SUCCESS, f'Added {quantity} ball(s) of {col_var.product_id.brand_id.name} {col_var.product_id.name},\
                               shade {col_var.colour_cat_id.colour_name}')

    request.session['basket'] = basket

    # add to user profile temporary basket if the user is logged in.

    if request.user.is_authenticated:
        current_user = UserProfile.objects.filter(user__id=request.user.id)
        basket_string = str(basket)
        basket_string = basket_string.replace("\'", "\"")
        current_user.update(temporary_basket=str(basket_string))

    return redirect(reverse('view_basket'))


@login_required
def leave_review(request, order_num):
    """
    """
    order = get_object_or_404(Order, order_num=order_num)
    # get reviews if they have already been created
    reviews = ReviewYarns.objects.filter(order=order)

    context = {
        'order': order,
        'reviews': reviews,
    }

    template = 'core/submit-review.html'
    return render(request, template, context)


def submit_review(request, order_num):
    """ """
    order = get_object_or_404(Order, order_num=order_num)
    if request.POST:
        try:
            rating = request.POST.get('rating')
            comment = request.POST.get('comment')
            yarn = request.POST.get('yarn')
            query = Q(order=order) & Q(yarn=yarn)

            if not rating:
                messages.add_message(
                    request, messages.ERROR, f'You need to submit a star rating')
                return HttpResponse(status=200)

            if not comment:
                messages.add_message(
                    request, messages.ERROR, f'You need to submit a comment')
                return HttpResponse(status=200)
            if rating and comment:
                if not ReviewYarns.objects.filter(query):
                    new_review = ReviewYarns(
                        order=order,
                        yarn=Colour_var.objects.get(id=(yarn)),
                        rating=rating,
                        comment=comment,
                    )
                    new_review.save()
                    messages.add_message(
                        request, messages.SUCCESS, f'Thankyou for your review!')
                    return HttpResponse(status=200)
                else:
                    existing_review = ReviewYarns.objects.get(query)
                    existing_review.rating = rating
                    existing_review.comment = comment
                    existing_review.approved = False
                    existing_review.save()
                    messages.add_message(
                        request, messages.SUCCESS, f'Thank you for updating your review!')
                    return HttpResponse(status=200)
        except Exception as e:
            messages.add_message(
                request, messages.ERROR, f'Unable to submit or update your review due to error {e}')
            return redirect(reverse('leave_review', kwargs={'order_num': order_num}))
