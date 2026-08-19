from django.shortcuts import (render, HttpResponse, redirect,
                              get_object_or_404, reverse)
from django.contrib import messages

from product.models import Colour_var, Product
from core.models import UserProfile

# Create your views here.


def view_basket(request):
    """
    Displays current basket contents as well as customer favourites'
      list if they are
    logged in (part of :model:`UserProfile`)

    **Template**
    `basket/basket.html`

    **Context**
    ``favourites_list`` - visible for authenticated users only.

    """
    favourite_list = []

    if request.user.is_authenticated:
        current_user = get_object_or_404(UserProfile, user__id=request.user.id)
        fave_list = current_user.wish_list

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
    }
    template = 'basket/basket.html'

    return render(request, template, context)


def add_to_basket(request):
    """
    Adds a item to a basket saved to the current session and
    :model:`UserProfile`
      (if the user is authenticated)
    On return, the page from which the request was made is reloaded and success
    message displayed to customer.

    Items added to the basket are instances of :model:`product.Colour_var`.
    Maximum quantity of an item
    which can be added to the basket corrected depending on whether it has
    `low_stock=True` property.

    If the item is already in the basket then quantity is increased.
    """

    quantity = int(request.POST.get('quantity'))
    col_var_id = request.POST['colour_var']
    col_var = get_object_or_404(Colour_var, pk=col_var_id)
    redirect_url = request.POST.get('redirect_url')

    basket = request.session.get('basket', {})

    if col_var_id in list(basket.keys()):
        if col_var.low_stock:
            test = basket[col_var_id] + quantity
            if test < 10:
                basket[col_var_id] += quantity

                messages.add_message(
                    request, messages.SUCCESS, f'Updated the quantity of {
                        col_var.product_id.brand_id.name} {
                        col_var.product_id.name},\
                               shade {
                        col_var.colour_cat_id.colour_name} to {test} balls')
            else:
                # can not add to basket- error message and redirect
                messages.add_message(
                    request, messages.ERROR, f'Low stock! Unable to add \
                          {quantity} extra balls of {
                        col_var.product_id.brand_id.name} {
                        col_var.product_id.name}\
                               to your basket.')
                return redirect(redirect_url)
        else:
            test = basket[col_var_id] + quantity
            if test < 50:
                basket[col_var_id] += quantity
                messages.add_message(
                    request, messages.SUCCESS, f'Updated the quantity of {
                        col_var.product_id.brand_id.name} {
                        col_var.product_id.name},\
                               shade {
                        col_var.colour_cat_id.colour_name} to {test} balls')
            else:

                messages.add_message(
                    request,
                    messages.ERROR,
                    f'Insufficient stock! Unable to add {quantity} extra \
                               balls of {
                        col_var.product_id.brand_id.name} {
                        col_var.product_id.name}\
                               to your basket.')
                return redirect(redirect_url)

    else:
        basket[col_var_id] = quantity

        messages.add_message(
            request, messages.SUCCESS, f'Added {quantity} ball(s) of {
                col_var.product_id.brand_id.name} {
                col_var.product_id.name},\
                               shade {
                col_var.colour_cat_id.colour_name}')

    request.session['basket'] = basket

    # add to user profile temporary basket if the user is logged in.

    if request.user.is_authenticated:
        current_user = UserProfile.objects.filter(user__id=request.user.id)
        basket_string = str(basket)
        basket_string = basket_string.replace("\'", "\"")
        current_user.update(temporary_basket=str(basket_string))

    return redirect(redirect_url)


def update_basket(request, item_id):
    """
    Increase or decrease quantity of instance of :model:`Colour_var` in
    session basket and
    :model:`UserProfile` field `temporary_basket`

    Maximum quantity of an item depends on its `low_stock` property.

    On return the `view_basket` view is reloaded.
    """

    col_var = get_object_or_404(Colour_var, pk=item_id)
    quantity = int(request.POST.get('quantity'))

    basket = request.session.get('basket', {})
    try:
        basket[str(item_id)] = quantity
        request.session['basket'] = basket

        if request.user.is_authenticated:
            current_user = UserProfile.objects.filter(user__id=request.user.id)
            basket_string = str(basket)
            basket_string = basket_string.replace("\'", "\"")
            current_user.update(temporary_basket=str(basket_string))

        messages.add_message(
            request, messages.SUCCESS, f'Updated {
                col_var.product_id.brand_id.name} {
                col_var.product_id.name} in \
                               shade {
                col_var.colour_cat_id.colour_name} to {quantity} balls.')
    except BaseException:
        messages.add_message(
            request, messages.ERROR, f'Unable to update the quantity of {
                col_var.product_id.brand_id.name} {
                col_var.product_id.name} in \
                               shade {
                col_var.colour_cat_id.colour_name} in your basket.')

    return redirect(reverse('view_basket'))


def delete_from_basket(request, item_id):
    """
    Removes instance of :model:`Colour_var` from `basket` saved to session
      and :model:`UserProfile.temporary_basket`

    returns HttpResponse 200 if successfully completed.
    """

    try:
        col_var = get_object_or_404(Colour_var, pk=item_id)
        basket = request.session.get('basket', {})
        basket.pop(str(item_id))
        messages.add_message(
            request, messages.SUCCESS, f'Removed {
                col_var.product_id.brand_id.name} {
                col_var.product_id.name} in \
                               shade {
                col_var.colour_cat_id.colour_name} from your basket.')
        request.session['basket'] = basket
        if request.user.is_authenticated:
            current_user = UserProfile.objects.filter(user__id=request.user.id)
            basket_string = str(basket)
            basket_string = basket_string.replace("\'", "\"")
            current_user.update(temporary_basket=str(basket_string))

        return HttpResponse(status=200)
    except Exception as e:
        print('here', e)
        messages.add_message(
            request, messages.ERROR, f'Unable to remove {
                col_var.product_id.brand_id.name} {
                col_var.product_id.name} in \
                               shade {
                col_var.colour_cat_id.colour_name} from your basket.\
                               Error code {e}.')
        return HttpResponse(status=500)
