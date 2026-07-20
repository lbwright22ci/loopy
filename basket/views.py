from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, reverse
from django.contrib import messages

from product.models import Colour_var
from core.models import UserProfile

import json

# Create your views here.


def view_basket(request):
    """ """

    context = {
    }
    template ='basket/basket.html'

    return render(request, template, context)


def add_to_basket(request):
    """ """

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
                messages.add_message(request, messages.SUCCESS, f'Updated the quantity of {col_var.product_id.brand_id.name} {col_var.product_id.name},\
                               shade {col_var.colour_cat_id.colour_name} to {test} balls')
            else:
                # can not add to basket- error message and redirect
                messages.add_message(request, messages.ERROR, f'Low stock! Unable to add {quantity} extra \
                               balls of {col_var.product_id.brand_id.name} {col_var.product_id.name}\
                               to your basket.')
                return redirect(redirect_url)
        else:
            test = basket[col_var_id] + quantity
            if test < 50:
                basket[col_var_id] += quantity
                messages.success(request, messages.SUCCESS, f'Updated the quantity of {col_var.product_id.brand_id.name} {col_var.product_id.name},\
                               shade {col_var.colour_cat_id.colour_name} to {test} balls')
            else:
                
                messages.error(request, messages.ERROR, f'Insufficient stock! Unable to add {quantity} extra \
                               balls of {col_var.product_id.brand_id.name} {col_var.product_id.name}\
                               to your basket.')
                return redirect(redirect_url)
                
    else:
        basket[col_var_id] = quantity
        messages.success(request, f'Added {quantity} ball(s) of {col_var.product_id.brand_id.name} {col_var.product_id.name},\
                               shade {col_var.colour_cat_id.colour_name}')

    request.session['basket'] = basket

    # add to user profile temporary basket if the user is logged in.

    if request.user.is_authenticated:
        current_user = UserProfile.objects.filter(user__id= request.user.id)
        basket_string = str(basket)
        basket_string = basket_string.replace("\'", "\"")
        current_user.update(temporary_basket= str(basket_string))

    return redirect(redirect_url)

def update_basket(request, item_id):
    """ """
    
    col_var = get_object_or_404(Colour_var, pk=item_id)
    quantity = int(request.POST.get('quantity'))

    basket = request.session.get('basket', {})
    try:
        basket[str(item_id)] = quantity
        request.session['basket'] = basket
        
        if request.user.is_authenticated:
            current_user = UserProfile.objects.filter(user__id= request.user.id)
            basket_string = str(basket)
            basket_string = basket_string.replace("\'", "\"")
            current_user.update(temporary_basket= str(basket_string))
        
        messages.add_message(request, messages.SUCCESS, f'Updated {col_var.product_id.brand_id.name} {col_var.product_id.name} in \
                               shade {col_var.colour_cat_id.colour_name} to {quantity} balls.')
    except:
        messages.add_message(request, messages.ERROR, f'Unable to update the quantity of {col_var.product_id.brand_id.name} {col_var.product_id.name} in \
                               shade {col_var.colour_cat_id.colour_name} in your basket.')


    return redirect(reverse('view_basket'))

def delete_from_basket(request, item_id):
    """ """

    try:
        col_var = get_object_or_404(Colour_var, pk=item_id)
        basket = request.session.get('basket', {})
        basket.pop(str(item_id))
        messages.add_message(request, messages.SUCCESS, f'Removed {col_var.product_id.brand_id.name} {col_var.product_id.name} in \
                               shade {col_var.colour_cat_id.colour_name} from your basket.')
        request.session['basket'] = basket
        if request.user.is_authenticated:
            current_user = UserProfile.objects.filter(user__id= request.user.id)
            basket_string = str(basket)
            basket_string = basket_string.replace("\'", "\"")
            current_user.update(temporary_basket= str(basket_string))

        return HttpResponse(status=200)
    except Exception as e:
        print('here', e)
        messages.add_message(request, messages.ERROR, f'Unable to remove {col_var.product_id.brand_id.name} {col_var.product_id.name} in \
                               shade {col_var.colour_cat_id.colour_name} from your basket.\
                               Error code {e}.')
        return HttpResponse(status=500)