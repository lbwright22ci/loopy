from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.decorators.http import require_POST
from django.conf import settings
from django.contrib import messages
from .forms import ContactAndBillingForm, ShippingAddressForm, ExtraDetailsForm
from .models import Order, YarnOrderLineitem
from core.models import UserProfile, SaleSettings
from product.models import Colour_var
from basket.context_processor import basket_contents

import json
import stripe

@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag', {})),
            'save_details': request.POST.get('save_detail'),
            'username': request.user,
            'is_gift': request.session.get('is_gift'),
            'gift_message': request.session.get('gift_message'),
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.add_message(request, messages.ERROR, 'Sorry your payment can not be processed \
                       right now.  Please try again later')
        return HttpResponse(content=e, status = 400)

def checkout_step1(request):
    """" """
    
    basket = request.session.get('basket', ())
    if not basket:
        messages.add_message(request, messages.ERROR, 'There is nothing in your basket at the moment')
        return redirect(reverse ('allproducts'))
    
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
            contact_billing_form = ContactAndBillingForm(initial={
                'first_name':profile.user.first_name,
                'second_name':profile.user.last_name,
                'email': profile.user.email,
                'phone': profile.default_phone,
                'billing_street_address1': profile.default_street_address1,
                'billing_street_address2': profile.default_street_address2,
                'billing_county': profile.default_county,
                'billing_country': profile.default_country,
                'billing_postcode': profile.default_postcode,
                'billing_town': profile.default_town,
            })
        except UserProfile.DoesNotExist:
            contact_billing_form =ContactAndBillingForm()
    else:
        contact_billing_form= ContactAndBillingForm()

    if request.POST:
        contact_billing_form= ContactAndBillingForm(data=request.POST)
        if contact_billing_form.is_valid():
            request.session['first_name'] = request.POST.get('first_name')
            request.session['second_name'] = request.POST.get('second_name')
            request.session['email'] = request.POST.get('email')
            request.session['billing_street_address1'] = request.POST.get('billing_street_address1')
            request.session['billing_street_address2'] = request.POST.get('billing_street_address2')
            request.session['billing_town'] = request.POST.get('billing_town')
            request.session['billing_county'] = request.POST.get('billing_county')
            request.session['billing_country'] = request.POST.get('billing_country')
            request.session['billing_postcode'] = request.POST.get('billing_postcode')
            if request.POST.get('billing_shipping_same'):
                request.session['bs_same'] = True
            else:
                request.session['bs_same'] = False
            
            return redirect(checkout_step2)
    
    context={
        'form':contact_billing_form,
    }
    template = 'checkout/checkout-step1.html'
    return render(request, template, context)

def checkout_step2(request):
    """" """
    
    basket = request.session.get('basket', ())
    if not basket:
        messages.add_message(request, messages.ERROR, 'There is nothing in your basket at the moment')
        return redirect(reverse ('allproducts'))
    
    bs_same = request.session['bs_same']

    if bs_same :
        shipping_form = ShippingAddressForm(initial={
            'shipping_street_address1' : request.session.get('billing_street_address1'),
            'shipping_street_address2' : request.session.get('billing_street_address2'),
            'shipping_town' : request.session.get('billing_town'),
            'shipping_county' : request.session.get('billing_county'),
            'shipping_country' : request.session.get('billing_country'),
            'shipping_postcode' : request.session.get('billing_postcode'),
        })
    else:
        shipping_form = ShippingAddressForm()

    if request.POST:
        shipping_form= ShippingAddressForm(data=request.POST)
        if shipping_form.is_valid():
            request.session['shipping_street_address1'] = request.POST.get('shipping_street_address1')
            request.session['shipping_street_address2'] = request.POST.get('shipping_street_address2')
            request.session['shipping_town'] = request.POST.get('shipping_town')
            request.session['shipping_county'] = request.POST.get('shipping_county')
            request.session['shipping_postcode'] = request.POST.get('shipping_postcode')
        
            request.session['postage_class'] = int(request.POST.get('shippingClass'))
            
            return redirect(checkout_step3)    

    context={
        'form':shipping_form,
    }
    template = 'checkout/checkout-step2.html'
    return render(request, template, context)

def checkout_step3(request):
    """" """
    
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if not stripe_public_key:
        messages.add_message(request, messages.ERROR, 'Stripe Public Key is missing. We can not ' \
        'process your order.  Please email loopyyarnsuk@gmail.com')
        return redirect(reverse('view_basket'))
    
    first_name = request.session.get('first_name')
    second_name = request.session.get('second_name')
    full_name = f'{first_name} {second_name}'
    email = request.session.get('email')
    phone = request.session.get('phone')
    billing_street_address1 = request.session.get('billing_street_address1')
    billing_street_address2 = request.session.get('billing_street_address2')
    billing_town = request.session.get('billing_town')
    billing_county = request.session.get('billing_county')
    billing_country = request.session.get('billing_country')
    billing_postcode = request.session.get('billing_postcode')
    shipping_street_address1 = request.session.get('shipping_street_address1')
    shipping_street_address2 = request.session.get('shipping_street_address2')
    shipping_town = request.session.get('shipping_town')
    shipping_county = request.session.get('shipping_county')
    shipping_country = "GB"
    shipping_postcode = request.session.get('shipping_postcode')
    postage_class = request.session.get('postage_class')

    current_basket = basket_contents(request)
    if postage_class == 0:
        total = current_basket['grand_total']
        postage_cost = current_basket['estimated_postage']
    elif postage_class ==1:
        total = current_basket['grand_total_first']
        postage_cost = current_basket['first_class']
    else:
        messages.add_message(request, messages.ERROR, 'Postage class not assigned to the order')
    stripe_total = round(total*100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )
    

    if request.POST:
        extra_form = ExtraDetailsForm(data=request.POST)
        if extra_form.is_valid:
            
            temp = request.POST.get('is_gift')
            if temp == 'on':
                is_gift = True
            else:
                is_gift = False
            request.session['is_gift'] = is_gift
            request.session['gift_message'] = request.POST.get('gift_message')

            order = Order(
                first_name = first_name,
                second_name = second_name,
                phone = phone,
                email = email,
                billing_street_address1 = billing_street_address1,
                billing_street_address2 = billing_street_address2,
                billing_town = billing_town,
                billing_county= billing_county,
                billing_postcode = billing_postcode,
                billing_country = billing_country,
                postage_class = postage_class,
                shipping_street_address1 = shipping_street_address1,
                shipping_street_address2 = shipping_street_address2,
                shipping_town = shipping_town,
                shipping_county= shipping_county,
                shipping_postcode = shipping_postcode,
                parcel_size = current_basket['parcel_size'],
                order_subtotal = current_basket['total'],
                order_discount =current_basket['discount'],
                grand_total = total,
                postage_cost = postage_cost,
                is_gift = is_gift,
                gift_message = request.POST.get('gift_message'),)
            # order.save(commit = False)

            pid =request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid

            basket = request.session.get('basket', ())
            order.basket_contents = json.dumps(basket)
            order.save()
            
            for item_id, item_data in basket.items():
                try:
                    col_var = get_object_or_404(Colour_var, pk = item_id)
                    if col_var.product_id.on_promotion:
                        sale_discount = SaleSettings.objects.filter(active=True)[0].sale_percent
                        current_price = Decimal(col_var.product_id.price*(100-sale_discount)/100)
                    else:
                        current_price = col_var.product_id.price
                    yarn_order_line_item = YarnOrderLineitem(
                        order = order,
                        quantity = item_data,
                        yarn = col_var,
                        current_price= current_price,
                        linetotal = item_data * current_price,)
                    yarn_order_line_item.save()
                except Colour_var.DoesNotExist:
                    messages.add_message(request, messages.ERROR, 'One of the items in your order is no longer ' \
                    'available.  Please email us for assitance: loopyyarnsuk@gmail.com')
                    order.delete()
                    return redirect(reverse('view_basket'))
            request.session['save_details']= request.POST.get('save_details')
            return redirect(reverse('checkout_success', args=[order.order_num]))        
        else:
            messages.add_message(request, 'Form is incorrectly completed. Please check your details')

    else:
        extra_form = ExtraDetailsForm()

        basket = request.session.get('basket', ())
        if not basket:
            messages.add_message(request, messages.ERROR, 'There is nothing in your basket at the moment')
            return redirect(reverse ('allproducts'))

    context={
        'form':extra_form,
        'first_name': first_name,
        'second_name' : second_name,
        'full_name':full_name, 
        'email': email, 
        'phone' : phone,
        'billing_street_address1' : billing_street_address1,
        'billing_street_address2' : billing_street_address2,
        'billing_town' : billing_town, 
        'billing_county': billing_county, 
        'billing_country': billing_country, 
        'billing_postcode': billing_postcode, 
        'shipping_street_address1': shipping_street_address1, 
        'shipping_street_address2': shipping_street_address2, 
        'shipping_town': shipping_town, 
        'shipping_county': shipping_county, 
        'shipping_country': shipping_country,
        'shipping_postcode':shipping_postcode,
        'postage_class':postage_class, 
        'stripe_public_key':stripe_public_key,
        'client_secret': intent.client_secret,
    }
    template = 'checkout/checkout-step3.html'
    return render(request, template, context)

def checkout_success(request, order_num):
    """ """
    order = get_object_or_404(Order, order_num = order_num)
    save_details = request.session.get('save_details')

    if request.user.is_authenticated:
        user_profile = get_object_or_404(UserProfile, user = request.user)
        order.user_profile = user_profile
        order.save()
        if save_details == "on":
            user_profile.default_phone = order.phone
            user_profile.default_street_address1 = order.billing_street_address1
            user_profile.default_street_address2 = order.billing_street_address2
            user_profile.default_town = order.billing_town
            user_profile.default_county = order.billing_county
            user_profile.default_country = order.billing_country
            user_profile.user.first_name = order.first_name
            user_profile.user.last_name = order.second_name
            user_profile.default_postcode = order.billing_postcode
            user_profile.save()

    messages.add_message(request, messages.SUCCESS, f'Your order ({order.order_num}) has been placed!\
                         A confirmation email will be sent to {order.email}. Please check your spam\
                         folder if you do not receive it.')

    if 'basket' in request.session:
        del request.session['basket']

    context={
        'order':order,
    }
    template= 'checkout/checkout-success.html'

    return render(request, template, context)