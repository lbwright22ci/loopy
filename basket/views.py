from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.


def view_basket(request):
    """ """

    context = {

    }
    template =

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
                # success message
            else:
                # can not add to basket- error message and redirect
        else:
            test = basket[col_var_id] + quantity
            if test < 50:
                basket[col_var_id] += quantity
                # success message
            else:
                # can not add to basket- error message and redirect
                
    else:
        basket[col_var_id] = quantity
        # success message

    request.session['basket', {}]

    return redirect(redirect_url)
