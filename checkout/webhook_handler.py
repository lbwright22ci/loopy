from decimal import Decimal
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib import messages 
from .models import Order, YarnOrderLineitem
from product.models import Colour_var
from core.models import UserProfile

import json
import time
import stripe

class StripeWH_Handler:
    """  """

    def __init__(self, request):
        self.request = request
    
    def handle_event(self, event):
        """ Handle generic/unknown/unexpected webhook event """
        return HttpResponse(
            content=f'Unhandled webhook receieved: {event['type']}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """ Handle generic/unknown/unexpected webhook event """
        intent =event.data.object
        pid = intent.id

        basket = intent.metadata.basket
        save_details = intent.metadata.save_details
        is_gift = intent.metadata.is_gift
        gift_message = intent.metadata.gift_message
        username = intent.metadata.username
        postage_class = intent.metadata.postage_class
        parcel_size = intent.metadata.parcel_size
        order_subtotal = intent.metadata.order_subtotal
        order_discount = intent.metadata.order_discount

        if is_gift == 'true':
            is_gift = True
        else:
            is_gift = False

        if save_details =='true':
            save_details = True
        else:
            save_details = False 

        # Get the Charge object
        stripe_charge = stripe.Charge.retrieve(
            intent.latest_charge
        )

        billing_details = stripe_charge.billing_details # updated
        shipping_details = intent.shipping
        grand_total = round(stripe_charge.amount / 100, 2) # updated

        if shipping_details.address.line2 =="":
            shipping_details.address.line2 = None
        if billing_details.phone=="ul":
            billing_details.phone = None
        
        order_exists = False
        attempt = 1
        while attempt <=5:
            try:
                order = Order.objects.get(
                    phone = billing_details.phone,
                    email__iexact = billing_details.email,
                    billing_street_address1__iexact = billing_details.address.line1,
                    billing_street_address2__iexact = billing_details.address.line2,
                    billing_town__iexact = billing_details.address.city,
                    billing_county__iexact= billing_details.address.state,
                    postage_class = postage_class,
                    shipping_street_address1__iexact = shipping_details.address.line1,
                    shipping_street_address2__iexact = shipping_details.address.line2,
                    shipping_town__iexact = shipping_details.address.city,
                    shipping_county__iexact= shipping_details.address.state,
                    shipping_postcode__iexact = shipping_details.address.postal_code,
                    parcel_size = parcel_size,
                    grand_total = grand_total,
                    stripe_pid__iexact = pid,
                    gift_message__iexact = gift_message,
                )

                # Historical orders with the same details would not have the same stripe_pid values.

                order_exists = True

                break

            except Order.DoesNotExist:
                attempt +=1
                time.sleep(1)

        if order_exists:
            return HttpResponse(
                    content=f'Webhook receieved: {event['type']} | SUCCESS: order exists in the database',
                    status=200)
        else:
            order = None

            try:
                first_name = billing_details.name.split()[0]
                second_name = billing_details.name.split()[1]

                order = Order(
                    first_name = first_name,
                    second_name = second_name,
                    user_profile = username,
                    phone = billing_details.phone,
                    email = billing_details.email,
                    billing_street_address1 = billing_details.address.line1,
                    billing_street_address2 = billing_details.address.line2,
                    billing_town = billing_details.address.city,
                    billing_county= billing_details.address.state,
                    billing_postcode = shipping_details.address.postal_code,
                    billing_country = billing_details.address.country,
                    postage_class = postage_class,
                    shipping_street_address1 = shipping_details.address.line1,
                    shipping_street_address2 = shipping_details.address.line2,
                    shipping_town = shipping_details.address.city,
                    shipping_county= shipping_details.address.state,
                    shipping_postcode = shipping_details.address.postal_code,
                    parcel_size = parcel_size,
                    order_subtotal = order_subtotal,
                    order_discount = order_discount,
                    grand_total = total,
                    gift_message = gift_message,
                    stripe_pid = pid,
                    basket_contents = basket,
                    is_gift = is_gift,
                    )
                
                order.save()

                for item_id, item_data in json.loads(basket).items():
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
                
            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(content = f'Webhook receieved: {event['type']} | ERROR: {e}', 
                                    status= 500)

        return HttpResponse(
            content=f'Webhook receieved: {event['type']} | order created in database by webhook',
            status=200)
    
    def handle_payment_intent_payment_failure(self, event):
        """ Handle generic/unknown/unexpected webhook event """
        return HttpResponse(
            content=f'Webhook receieved: {event['type']}',
            status=200)