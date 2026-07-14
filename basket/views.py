from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

# Create your views here.


def view_basket(request):
    """ """

    context = {

    }
    template ='basket/basket.html'

    return render(request, template, context)


def add_to_basket(request):
    """ """

    col_var = request.POST.get['colour_var']
    quantity = request.POST.get['quantity']
    col_var_id = col_var.id
    redirect_url = request.get['redirect_url']

    basket = request.session.get('basket', {})

    if col_var_id in list(basket.keys()):
        if col_var.low_stock:
            test = basket[col_var_id] + quantity
            if test < 10:
                basket[col_var_id] += quantity
                messages.info(request, f'Updated the quantity of {col_var.product_id.name},\
                               shade {col_var.colour_cat_id.colour_name}')
            else:
                # can not add to basket- error message and redirect
                messages.error(request, f'Low stock! Unable to add {quantity} extra \
                               balls of {col_var.product_id.name}\
                               to your basket.')
                return redirect(redirect_url)
        else:
            test = basket[col_var_id] + quantity
            if test < 50:
                basket[col_var_id] += quantity
                messages.info(request, f'Updated the quantity of {col_var.product_id.name},\
                               shade {col_var.colour_cat_id.colour_name}')
            else:
                messages.error(request, f'Insufficient stock! Unable to add {quantity} extra \
                               balls of {col_var.product_id.name}\
                               to your basket.')
                return redirect(redirect_url)
                
    else:
        basket[col_var_id] = quantity
        messages.info(request, f'Added {col_var.product_id.name},\
                               shade {col_var.colour_cat_id.colour_name}')

    request.session['basket', {}]

    return redirect(redirect_url)
