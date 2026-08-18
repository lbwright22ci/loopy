from decimal import Decimal

from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.decorators.http import require_POST
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

from .forms import ContactAndBillingForm, ShippingAddressForm, SaveDetailsForm
from .models import Order, YarnOrderLineitem, Refund, Shipped
from core.models import UserProfile, SaleSettings
from product.models import Colour_var
from basket.context_processor import basket_contents

import json
import stripe


@require_POST
def cache_checkout_data(request):
    """
    Saves checkout data to the cache when a new instance of :model:`Order` is created by a POST request.

    Adds the following fields to `metadata` field of stripe.PayemntIntent:
    'basket', 'username', 'is_gift', 'gift_message', 'postage_class', 'parcel_size', 'save_details'
    """
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        current_basket = basket_contents(request)

        stripe.PaymentIntent.modify(pid, metadata={
            'basket': json.dumps(request.session.get('basket', {})),
            'username': request.user,
            'is_gift': request.session.get('is_gift'),
            'gift_message': request.session.get('gift_message'),
            'postage_class': request.session.get('postage_class'),
            'parcel_size': current_basket['parcel_size'],
            'save_details': request.POST.get('save_details')
        })

        return HttpResponse(status=200)
    except Exception as e:
        messages.add_message(request, messages.ERROR, 'Sorry your payment can not be processed \
                       right now.  Please try again later')
        return HttpResponse(content=e, status=400)


def checkout_step1(request):
    """
    First step of customer checkout flow before creating a new instance of :model:`Order`. Displays instance of 
    :form:`ContactAndBillingForm`.

    Data retrieved from POST request in this view is saved to the session.

    **Template**
    'checkout/checkout-step1.html'

    **Context**
    `form` : instance of :form:'ContactAndBillingForm'
    `google_key` : key required for Google Maps API for autofill address facility ('static/js/address.js')
    """

    basket = request.session.get('basket', ())
    if not basket:
        messages.add_message(request, messages.ERROR,
                             'There is nothing in your basket at the moment')
        return redirect(reverse('allproducts'))

    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
            contact_billing_form = ContactAndBillingForm(initial={
                'first_name': profile.user.first_name,
                'second_name': profile.user.last_name,
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
            contact_billing_form = ContactAndBillingForm()
    else:
        contact_billing_form = ContactAndBillingForm()

    if request.POST:
        contact_billing_form = ContactAndBillingForm(data=request.POST)
        if contact_billing_form.is_valid():
            request.session['first_name'] = request.POST.get('first_name')
            request.session['second_name'] = request.POST.get('second_name')
            request.session['email'] = request.POST.get('email')
            request.session['phone'] = request.POST.get('phone')
            request.session['billing_street_address1'] = request.POST.get(
                'billing_street_address1')
            request.session['billing_street_address2'] = request.POST.get(
                'billing_street_address2')
            request.session['billing_town'] = request.POST.get('billing_town')
            request.session['billing_county'] = request.POST.get(
                'billing_county')
            request.session['billing_country'] = request.POST.get(
                'billing_country')
            request.session['billing_postcode'] = request.POST.get(
                'billing_postcode')
            if request.POST.get('billing_shipping_same'):
                request.session['bs_same'] = True
            else:
                request.session['bs_same'] = False

            return redirect(checkout_step2)

    context = {
        'form': contact_billing_form,
        'google_key': settings.GOOGLE_MAPS_DEMO
    }
    template = 'checkout/checkout-step1.html'
    return render(request, template, context)


def checkout_step2(request):
    """
    Second step of customer checkout flow before creating a new instance of :model:`Order`. Displays instance of 
    :form:`ShippingAddressForm`.

    Data retrieved from POST request in this view is saved to the session.

    **Template**
    'checkout/checkout-step2.html'

    **Context**
    'form' : instance of :form:`ShippingAddressForm`
    'bs_same' : billing and shipping addresses are the same
    """

    basket = request.session.get('basket', ())
    if not basket:
        messages.add_message(request, messages.ERROR,
                             'There is nothing in your basket at the moment')
        return redirect(reverse('allproducts'))

    bs_same = request.session['bs_same']

    if bs_same:
        shipping_form = ShippingAddressForm(initial={
            'shipping_street_address1': request.session.get('billing_street_address1'),
            'shipping_street_address2': request.session.get('billing_street_address2'),
            'shipping_town': request.session.get('billing_town'),
            'shipping_county': request.session.get('billing_county'),
            'shipping_country': request.session.get('billing_country'),
            'shipping_postcode': request.session.get('billing_postcode'),
        })
    else:
        shipping_form = ShippingAddressForm()

    if request.POST:
        shipping_form = ShippingAddressForm(data=request.POST)
        if shipping_form:
            if not bs_same:
                request.session['shipping_street_address1'] = request.POST.get(
                    'shipping_street_address1')
                request.session['shipping_street_address2'] = request.POST.get(
                    'shipping_street_address2')
                request.session['shipping_town'] = request.POST.get(
                    'shipping_town')
                request.session['shipping_county'] = request.POST.get(
                    'shipping_county')
                request.session['shipping_postcode'] = request.POST.get(
                    'shipping_postcode')
            else:
                request.session['shipping_street_address1'] = request.session.get(
                    'billing_street_address1')
                request.session['shipping_street_address2'] = request.session.get(
                    'billing_street_address2')
                request.session['shipping_town'] = request.session.get(
                    'billing_town')
                request.session['shipping_county'] = request.session.get(
                    'billing_county')
                request.session['shipping_postcode'] = request.session.get(
                    'billing_postcode')

            request.session['postage_class'] = int(
                request.POST.get('shippingClass'))

            temp = request.POST.get('is_gift')
            if temp == 'on':
                request.session['is_gift'] = True
            else:
                request.session['is_gift'] = False
            gift_message = request.POST.get('gift_message')
            if gift_message:
                request.session['gift_message'] = gift_message
            else:
                request.session['gift_message'] = "  "
            return redirect(checkout_step3)

    context = {
        'form': shipping_form,
        'bs_same': bs_same,
    }
    template = 'checkout/checkout-step2.html'
    return render(request, template, context)


def checkout_step3(request):
    """
    Last step of customer checkout flow to create a new instance of :model:`Order`. Displays instance of 
    :form:`SaveDetailsForm`.

    Data retrieved from POST request in this view used to create an instance of :model:`Order`

    **Template**
    'checkout/checkout-step3.html'

    **Context** 
    'form': instance of :form:`SaveDetailsForm`
    'first_name': available in page context so that order can be created by
    `webhook_handler.StripeWH_handler.handle_payment_intent_succeeded` if necessary
    'second_name' : available in page context so that order can be created by
    `webhook_handler.StripeWH_handler.handle_payment_intent_succeeded` if necessary
    'full_name':available in page context so that order can be created by
    `webhook_handler.StripeWH_handler.handle_payment_intent_succeeded` if necessary
    'email': available in page context so that order can be created by
    `webhook_handler.StripeWH_handler.handle_payment_intent_succeeded` if necessary
    'phone' : available in page context so that order can be created by
    `webhook_handler.StripeWH_handler.handle_payment_intent_succeeded` if necessary
    'billing_street_address1' : available in page context so that order can be created by
    `webhook_handler.StripeWH_handler.handle_payment_intent_succeeded` if necessary
    'billing_street_address2' : available in page context so that order can be created by
    `webhook_handler.StripeWH_handler.handle_payment_intent_succeeded` if necessary
    'billing_town' : available in page context so that order can be created by
    `webhook_handler.StripeWH_handler.handle_payment_intent_succeeded` if necessary
    'billing_county': available in page context so that order can be created by
    `webhook_handler.StripeWH_handler.handle_payment_intent_succeeded` if necessary
    'billing_country': available in page context so that order can be created by
    `webhook_handler.StripeWH_handler.handle_payment_intent_succeeded` if necessary
    'billing_postcode': available in page context so that order can be created by
    `webhook_handler.StripeWH_handler.handle_payment_intent_succeeded` if necessary 
    'shipping_street_address1': available in page context so that order can be created by
    `webhook_handler.StripeWH_handler.handle_payment_intent_succeeded` if necessary 
    'shipping_street_address2': available in page context so that order can be created by
    `webhook_handler.StripeWH_handler.handle_payment_intent_succeeded` if necessary 
    'shipping_town': available in page context so that order can be created by
    `webhook_handler.StripeWH_handler.handle_payment_intent_succeeded` if necessary
    'shipping_county': available in page context so that order can be created by
    `webhook_handler.StripeWH_handler.handle_payment_intent_succeeded` if necessary 
    'shipping_country': available in page context so that order can be created by
    `webhook_handler.StripeWH_handler.handle_payment_intent_succeeded` if necessary
    'shipping_postcode':available in page context so that order can be created by
    `webhook_handler.StripeWH_handler.handle_payment_intent_succeeded` if necessary
    'postage_class':available in page context so that order can be created by
    `webhook_handler.StripeWH_handler.handle_payment_intent_succeeded` if necessary
    'stripe_public_key':available in page context so that order can be created by
    `webhook_handler.StripeWH_handler.handle_payment_intent_succeeded` if necessary
    'client_secret': available in page context so that order can be created by
    `webhook_handler.StripeWH_handler.handle_payment_intent_succeeded` if necessary
    'is_gift': available in page context so that order can be created by
    `webhook_handler.StripeWH_handler.handle_payment_intent_succeeded` if necessary
    'gift_message' : available in page context so that order can be created by
    `webhook_handler.StripeWH_handler.handle_payment_intent_succeeded` if necessary
    """

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if not stripe_public_key:
        messages.add_message(request, messages.ERROR, 'Stripe Public Key is missing. We can not '
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
    is_gift = request.session.get('is_gift')
    gift_message = request.session.get('gift_message')

    current_basket = basket_contents(request)
    if postage_class == 0:
        total = current_basket['grand_total']
        postage_cost = current_basket['estimated_postage']
    elif postage_class == 1:
        total = current_basket['grand_total_first']
        postage_cost = current_basket['first_class']
    else:
        messages.add_message(request, messages.ERROR,
                             'Postage class not assigned to the order')

    stripe_total = round(total*100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    if request.POST:
        extra_form = SaveDetailsForm(data=request.POST)
        if extra_form.is_valid:
            ttemp = request.POST.get('save_details')
            if ttemp == "on":
                save_details = True
            else:
                save_details = False
            request.session['save_details'] = save_details

            order = Order(
                first_name=first_name,
                second_name=second_name,
                phone=phone,
                email=email,
                billing_street_address1=billing_street_address1,
                billing_street_address2=billing_street_address2,
                billing_town=billing_town,
                billing_county=billing_county,
                billing_postcode=billing_postcode,
                billing_country=billing_country,
                postage_class=postage_class,
                shipping_street_address1=shipping_street_address1,
                shipping_street_address2=shipping_street_address2,
                shipping_town=shipping_town,
                shipping_county=shipping_county,
                shipping_postcode=shipping_postcode,
                parcel_size=current_basket['parcel_size'],
                order_subtotal=current_basket['total'],
                order_discount=current_basket['discount'],
                grand_total=total,
                postage_cost=postage_cost,
                is_gift=is_gift,
                gift_message=gift_message,)

            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid

            basket = request.session.get('basket', ())
            order.basket_contents = json.dumps(basket)
            order.save()

            for item_id, item_data in basket.items():
                try:
                    col_var = get_object_or_404(Colour_var, pk=item_id)
                    if col_var.product_id.on_promotion:
                        sale_discount = SaleSettings.objects.filter(active=True)[
                            0].sale_percent
                        current_price = Decimal(
                            col_var.product_id.price*(100-sale_discount)/100)
                    else:
                        current_price = col_var.product_id.price
                    yarn_order_line_item = YarnOrderLineitem(
                        order=order,
                        quantity=item_data,
                        yarn=col_var,
                        current_price=current_price,
                        linetotal=item_data * current_price,)
                    yarn_order_line_item.save()
                except Colour_var.DoesNotExist:
                    messages.add_message(request, messages.ERROR, 'One of the items in your order is no longer '
                                         'available.  Please email us for assitance: loopyyarnsuk@gmail.com')
                    order.delete()
                    return redirect(reverse('view_basket'))

            return redirect(reverse('checkout_success', args=[order.order_num]))

        else:
            messages.add_message(
                request, messages.ERROR, 'Form is incorrectly completed. Please check your details')

    else:
        extra_form = SaveDetailsForm()

        basket = request.session.get('basket', ())

        if not basket:
            messages.add_message(request, messages.ERROR,
                                 'There is nothing in your basket at the moment')
            return redirect(reverse('allproducts'))

    context = {
        'form': extra_form,
        'first_name': first_name,
        'second_name': second_name,
        'full_name': full_name,
        'email': email,
        'phone': phone,
        'billing_street_address1': billing_street_address1,
        'billing_street_address2': billing_street_address2,
        'billing_town': billing_town,
        'billing_county': billing_county,
        'billing_country': billing_country,
        'billing_postcode': billing_postcode,
        'shipping_street_address1': shipping_street_address1,
        'shipping_street_address2': shipping_street_address2,
        'shipping_town': shipping_town,
        'shipping_county': shipping_county,
        'shipping_country': shipping_country,
        'shipping_postcode': shipping_postcode,
        'postage_class': postage_class,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
        'is_gift': is_gift,
        'gift_message': gift_message,
    }

    template = 'checkout/checkout-step3.html'

    return render(request, template, context)


def checkout_success(request, order_num):
    """
    Displays details of a newly created instance of :model:`Order`

    **Template**
    'checkout/checkout-success.html'

    **Context**
    `order`
    """
    order = get_object_or_404(Order, order_num=order_num)
    save_details = request.session.get('save_details')

    if request.user.is_authenticated:
        user_profile = get_object_or_404(UserProfile, user=request.user)
        user = get_object_or_404(User, id=request.user.id)
        order.user_profile = user_profile
        order.save()
        if save_details:
            user_profile.default_phone = order.phone
            user_profile.default_street_address1 = order.billing_street_address1
            user_profile.default_street_address2 = order.billing_street_address2
            user_profile.default_town = order.billing_town
            user_profile.default_county = order.billing_county
            user_profile.default_country = order.billing_country
            user.first_name = order.first_name
            user.last_name = order.second_name
            user_profile.default_postcode = order.billing_postcode
            user_profile.save()
            user.save()

    messages.add_message(request, messages.SUCCESS, f'Your order ({order.order_num}) has been placed!\
                         A confirmation email will be sent to {order.email}. Please check your spam\
                         folder if you do not receive it.')

    if 'basket' in request.session:
        del request.session['basket']
        if request.user.is_authenticated:
            current_user = get_object_or_404(UserProfile, user=request.user)
            current_user.temporary_basket = {}
            current_user.save()

    context = {
        'order': order,
    }
    template = 'checkout/checkout-success.html'

    return render(request, template, context)


@login_required
def Cancel_order(request, order_num):
    """
    Creates a new instance of the :model:`Refund` (related to :model:`Order` by a one-to-one relationship)

    Returns the user to the page from which they submitted the refund request (for customers this will
    be their account page and for shop admin it will be the order page in the admin area.)

    Refund payment is handled by Stripe.
    """

    order = get_object_or_404(Order, order_num=order_num)
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.POST:
        amount = Decimal(request.POST.get('amount'))

        reason = request.POST.get('reason')
        order_pid = request.POST.get('stripe_pid')

        stripe.api_key = stripe_secret_key

        if reason == 'customer cancelled order':
            rreason = 'requested_by_customer'
            refund = stripe.Refund.create(
                payment_intent=order_pid,
                amount=round(amount*100),
                reason=rreason,
            )
        else:
            reason = 'admin refunded customer'
            refund = stripe.Refund.create(
                payment_intent=order_pid,
                amount=round(amount*100),
            )
        refund_pid = refund.id
        new_refund = Refund(
            order=order,
            reason=reason,
            amount=amount,
            refund_id=refund_pid,
        )
        new_refund.save()
        order.refund_status = True
        order.save()

        if reason == 'customer cancelled order':
            messages.add_message(request, messages.SUCCESS, f'We are sorry that you changed your mind \
                             about this order.  A refund has been issued and the money will be \
                             returned to your payment card soon.')
            return HttpResponse(status=200)
        else:
            messages.add_message(request, messages.SUCCESS, f'#{order_num} has been refunded £{amount}.  \
                                 Customer has been notified.')

            return redirect(reverse('management_orders'))


@login_required
def mark_shipped(request):
    """
    Creates a new instance of :model:`Shipped` (related to :model:`Order` in a one-to-one relationship

    Success or failure message is displayed to shop admin and an email is sent to customer.
    )
    """
    if not request.user.is_superuser:
        messages.add_message(request, messages.ERROR, f"This page is only accessible for \
                                 Loopy Yarns staff.")
        return redirect(reverse('home'))
    try:
        if request.POST:
            order = Order.objects.get(pk=int(request.POST.get('order')))
            order.is_shipped = True
            order.save()
            shipped = Shipped(
                order=order,
            )
            shipped.save()

            email_subject = "Your order with Loopy Yarns has been shipped!"
            html_message = render_to_string('checkout/email/shipped.html',
                                            {'order': order, },
                                            )
            plain_message = strip_tags(html_message)

            msg = EmailMultiAlternatives(
                email_subject,
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [order.email],)
            msg.attach_alternative(html_message, "text/html")
            msg.send()

            messages.add_message(request, messages.SUCCESS, f'Order {order.order_num}\
                                  has been marked as shipped')
    except Exception as e:
        order.is_shipped = False
        order.save()
        shipped.delete()
        messages.add_message(request, messages.ERROR,
                             f'Unable to mark order as shipped due to error {e}')
    return redirect(reverse('management_orders'))
