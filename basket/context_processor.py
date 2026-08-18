import json
from decimal import Decimal

from django.shortcuts import get_object_or_404
from django.db.models import Q

from core.models import SaleSettings, Postage, Announcements, UserProfile
from product.models import Colour_var



def basket_contents(request):
    """
    Makes basket contents available to all templates across the site.

    Dependent on :model: `core.SalesSettings` (for correcting product price if on sale),
    :model: `core.Postage`, :model: `core.Announcements` (for calculating bulk buy discounts),
    :model:`UserProfile` (for retriving saved basket items in someone's account when they log in),
    :model:`Colour_var` (for product weight, price)

    **Context**
    ``basket_items``: a list of dictionaries. For each item in the list the following
    data is available- 'item_id', 'quantity', 'col_var' and 'price'
    (Price is adjusted depending on whether the product is on sale or not)

    ``total``: basket subtotal

    ``ball_count``: total number of balls of wool in the basket

    ``parcel_size``: '0' is small parcel, '1' is medium parcel (calculated on both weight and number of balls)

    ``discount``: bulk buy discount according to shop settings 

    ``estimated_postage``: second class postage for the basket contents based on current weight and
    number of balls of wool (ie. parcel size)

    ``grand_total``: Total payable if 2nd class postage

    ``first_class``: cost of 1st class postage for the basket contents

    ``grand_total_first``: Total payable if 1st class postage.

    """
    basket_items = []
    total = 0
    ball_count = 0
    order_weight = 0
    discount = 0
    estimated_postage = 0
    parcel_size = 0

    sale_discount = SaleSettings.objects.filter(active=True)[0].sale_percent
    bulk_buy = Announcements.objects.filter(active=True)[0]

    basket = request.session.get('basket', {})
    remove_item = []

    if request.user.is_authenticated:
        current_user = UserProfile.objects.get(user__id=request.user.id)
        saved_basket = current_user.temporary_basket

        if saved_basket:
            converted_basket = json.loads(saved_basket)

            # add contents of saved basket to the session basket when the user logs back in
            for key, value in converted_basket.items():
                if key in basket:
                    pass
                else:
                    basket[key] = int(value)
        basket_string = str(basket)
        basket_string = basket_string.replace("\'", "\"")
        current_user.temporary_basket = str(basket_string)
        current_user.save()

        request.session['basket'] = basket

    for item_id, item_data in basket.items():
        col_var = get_object_or_404(Colour_var, pk=item_id)
        if not col_var.product_id.visible:
            remove_item.append(item_id)
            continue
        if not col_var.in_stock:
            remove_item.append(item_id)
            continue
        if col_var.product_id.on_promotion:
            total += item_data * \
                Decimal(col_var.product_id.price*(100-sale_discount)/100)
            price = Decimal(col_var.product_id.price*(100-sale_discount)/100)
        else:
            total += item_data * col_var.product_id.price
            price = col_var.product_id.price
        ball_count += item_data
        order_weight += col_var.product_id.skein_weight*item_data
        basket_items.append({
            'item_id': item_id,
            'quantity': item_data,
            'col_var': col_var,
            'price': price,
        })

    for out_of_stock_item in remove_item:
        basket.pop(str(out_of_stock_item))

    # take into account any items removed if now out of stock or not visible:
    request.session['basket'] = basket

    # need to update saved basket if the user is logged in

    if request.user.is_authenticated:
        current_user = UserProfile.objects.filter(user__id=request.user.id)
        basket_string = str(basket)
        basket_string = basket_string.replace("\'", "\"")
        current_user.update(temporary_basket=str(basket_string))

    # take account of order discount based on number of balls of yarn in the basket
    if bulk_buy.bulk_buy == True:
        if ball_count > bulk_buy.upper_ball_num:
            discount = total*Decimal((bulk_buy.upper_discount)/100)
        elif ball_count < bulk_buy.lower_ball_num:
            discount = 0
        else:
            discount = total*Decimal((bulk_buy.lower_discount)/100)

    # find parcel size for postage
    # first adjust order weight to account for the weight of packing materials
    if ball_count < 5:
        order_weight = order_weight + 200
    else:
        order_weight = order_weight + 400

    small_ball_limit = Postage.objects.filter(
        Q(parcel_size=0) & Q(postage_class=0))[0].max_no_balls
    small_weight_limit = Postage.objects.filter(
        Q(parcel_size=0) & Q(postage_class=0))[0].max_weight*1000

    if ball_count < small_ball_limit and order_weight < small_weight_limit:
        parcel_size = 0
        estimated_postage = Postage.objects.filter(
            Q(parcel_size=0) & Q(postage_class=0))[0].postage_cost
        first_class = Postage.objects.filter(
            Q(parcel_size=0) & Q(postage_class=1))[0].postage_cost
    else:
        parcel_size = 1
        estimated_postage = Postage.objects.filter(
            Q(parcel_size=1) & Q(postage_class=0))[0].postage_cost
        first_class = Postage.objects.filter(
            Q(parcel_size=1) & Q(postage_class=1))[0].postage_cost

    if not bulk_buy.bulk_buy and ball_count > bulk_buy.upper_ball_num:
        discount = estimated_postage

    grand_total = total + estimated_postage - discount
    grand_total_first = total + first_class - discount

    return {
        'basket_items': basket_items,
        'total': total,
        'ball_count': ball_count,
        'parcel_size': parcel_size,
        'discount': discount,
        'estimated_postage': estimated_postage,
        'grand_total': grand_total,
        'first_class': first_class,
        'grand_total_first': grand_total_first,
    }
