import json
import time
import stripe
from decimal import Decimal

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string

from .models import Order, YarnOrderLineitem, Refund
from product.models import Colour_var
from core.models import UserProfile, ShopContactInfo, SaleSettings


class StripeWH_Handler:
    """
    Receives webhook events from `stripe` and determines the course of action.

    **Methods**
    `handle_event()`
    `handle_payment_intent_succeeded()`
    `handle_payment_intent_payment_failed()`
    `_send_order_conf_email`
    """

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """ Handle all webhook events other than 'payment_intent.succeeded'
        and 'payment_intent.payment_failed' """

        return HttpResponse(
            content=f'Unhandled webhook receieved: {event['type']}',
            status=200)

    def _send_order_conf_email(self, order):
        """
        Sends email to customer on completion of an order.

        **Email context**
        `phone`
        `order`
        """
        phone = f'0{ShopContactInfo.objects.all()[0].shop_phone}'
        email_subject = "Your order with Loopy Yarns has been received!"
        html_message = render_to_string('checkout/email/order-received.html',
                                        {'order': order, 'phone': phone},
                                        )
        plain_message = strip_tags(html_message)

        msg = EmailMultiAlternatives(
            email_subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [order.email],)
        msg.attach_alternative(html_message, "text/html")
        msg.send()

    def _send_refund_order_email(self, refund):
        """
        Sends email to customer when their order has been cancelled.

        **Email context**
        `refund`
        """
        if "cancel" in refund.reason:
            reason_int = 1
        else:
            reason_int = 0

        email_subject = "Your order with Loopy Yarns has been refunded!"
        html_message = render_to_string('checkout/email/cancel-order.html',
                                        {'refund': refund,
                                            'reason_int': reason_int, },
                                        )
        plain_message = strip_tags(html_message)

        msg = EmailMultiAlternatives(
            email_subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [refund.order.email],)
        msg.attach_alternative(html_message, "text/html")
        msg.send()

    def handle_payment_intent_succeeded(self, event):
        """
        Handles all instances of the webhook 'payment_intent.succeeded'

        If an instance of :model:`Order` with identical
        `stripe_pid` exists in the database
        already then only :method: `_send_order_conf_email` is called.

        If instance of :model:`Order` with `stripe_pid` does
        not exist in database after 5
        seconds then one is created, details are saved to the
        related instance of :model:`UserProfile` if relavent and
        the :method: `_send_order_conf_email` called.

        Else error message generated.
        """
        intent = event.data.object
        pid = intent.id

        basket = intent.metadata.basket
        is_gift = intent.metadata.is_gift
        gift_message = intent.metadata.gift_message
        userid = int(intent.metadata.username)
        postage_class = intent.metadata.postage_class
        parcel_size = intent.metadata.parcel_size

        if is_gift == 'true':
            is_gift = True
        elif is_gift == 'false':
            is_gift = False

        if intent.metadata.save_details == 'true':
            save_details = True
        else:
            save_details = False

        # Get the Charge object
        stripe_charge = stripe.Charge.retrieve(
            intent.latest_charge
        )

        billing_details = stripe_charge.billing_details  # updated
        shipping_details = intent.shipping
        grand_total = round(stripe_charge.amount / 100, 2)  # updated

        if shipping_details.address.line2 == "":
            shipping_details.address.line2 = None
        if billing_details.phone == "ul":
            billing_details.phone = None

        username = None
        if userid != "AnonymousUser":
            username = UserProfile.objects.get(user=userid)
            user = User.objects.get(id=userid)
            if save_details:
                username.default_phone = billing_details.phone
                username.default_street_address1 = billing_details.address.line1
                username.default_street_address2 = billing_details.address.line2
                username.default_town = billing_details.address.city
                username.default_county = billing_details.address.state
                username.default_country = shipping_details.address.country
                user.first_name = billing_details.name.split()[0]
                user.last_name = billing_details.name.split()[1]
                username.default_postcode = shipping_details.address.postal_code
                username.save()
                user.save()

        order_exists = False
        attempt = 1
        time.sleep(1)
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    stripe_pid=pid,
                    grand_total=grand_total,
                )

                # Historical orders with the same details would not have the
                # same stripe_pid values.

                order_exists = True

                break

            except Order.DoesNotExist:

                attempt += 1
                time.sleep(1)

        if order_exists:
            self._send_order_conf_email(order)
            return HttpResponse(
                content=f'Webhook receieved: {
                    event['type']} | SUCCESS: order exists in the database',
                status=200)
        else:
            order = None

            try:
                first_name = billing_details.name.split()[0]
                second_name = billing_details.name.split()[1]

                order = Order.objects.create(
                    first_name=first_name,
                    second_name=second_name,
                    user_profile=username,
                    phone=int(billing_details.phone),
                    email=billing_details.email,
                    billing_street_address1=billing_details.address.line1,
                    billing_street_address2=billing_details.address.line2,
                    billing_town=billing_details.address.city,
                    billing_county=billing_details.address.state,
                    billing_postcode=shipping_details.address.postal_code,
                    billing_country=shipping_details.address.country,
                    shipping_street_address1=shipping_details.address.line1,
                    shipping_street_address2=shipping_details.address.line2,
                    shipping_town=shipping_details.address.city,
                    shipping_county=shipping_details.address.state,
                    shipping_postcode=shipping_details.address.postal_code,
                    stripe_pid=pid,
                    basket_contents='{}'
                )

                order.basket_contents = str(basket)
                order.postage_class = int(postage_class)
                order.parcel_size = int(parcel_size)
                order.grand_total = grand_total
                order.gift_message = gift_message
                order.is_gift = is_gift
                order.save

                for item_id, item_data in json.loads(basket).items():
                    col_var = get_object_or_404(Colour_var, pk=item_id)
                    if col_var.product_id.on_promotion:
                        sale_discount = SaleSettings.objects.filter(
                            active=True)[
                            0].sale_percent
                        current_price = Decimal(
                            col_var.product_id.price * (
                                100 - sale_discount) / 100)
                    else:
                        current_price = col_var.product_id.price
                    yarn_order_line_item = YarnOrderLineitem(
                        order=order,
                        quantity=item_data,
                        yarn=col_var,
                        current_price=current_price,
                        linetotal=item_data * current_price,)
                    yarn_order_line_item.save()

            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook receieved: {
                        event['type']} | ERROR: {e}', status=500)

        self._send_order_conf_email(order)
        return HttpResponse(
            content=f'Webhook receieved: {
                event['type']} | order created in database by webhook',
            status=200)

    def handle_payment_intent_payment_failure(self, event):
        """
        Handles instances of webhook `payment_intent.payment_failure`
        """
        return HttpResponse(
            content=f'Webhook receieved: {event['type']}',
            status=200)

    def handle_refund_updated(self, event):
        """
        Handles all instances of the webhook 'refund.updated'

        If an instance of :model:`Refund` with identical
        `refund_id` exists in the database
        already then only :method: `_send_refund_order_email` is called.

        If instance of :model:`Refund` with `refund_id` does not
          exist in database after 5
        seconds then one is created and
        the :method: `_send_refund_order_email` called.

        Else error message generated.
        """
        intent = event.data.object
        refund_pid = intent.id
        amount = intent.amount
        order = get_object_or_404(Order, stripe_pid=intent.payment_intent)
        rreason = intent.reason

        # test to see if refund exists in the database
        refund_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                refund = Refund.objects.get(
                    refund_id__iexact=refund_pid,
                )

                refund_exists = True

                break

            except Refund.DoesNotExist:

                attempt += 1
                time.sleep(1)

        if refund_exists:
            self._send_refund_order_email(refund)
            return HttpResponse(
                content=f'Webhook receieved: {
                    event['type']} | \
                                SUCCESS: refund exists in the database',
                status=200)
        else:
            refund = None
            try:
                if rreason == "requested_by_customer":
                    reason = "customer cancelled order"
                else:
                    reason = "admin refunded customer"
                refund = Refund(
                    order=order,
                    reason=reason,
                    amount=amount / 100,
                    refund_id=refund_pid,
                )
                refund.save()
                order.refund_status = True
                order.save()
                if reason == 'customer cancelled order':
                    messages.add_message(
                        event, messages.SUCCESS, 'We are sorry that you changed your \
                                                     mind about this order.  A refund has \
                                                        been issued and the money will be \
                                                     returned to your payment card soon.')
                else:
                    messages.add_message(
                        event, messages.SUCCESS, f'#{order.order_num} has been \
                                                 refunded £{amount}.  \
                                                 Customer has been notified.')
            except Exception as e:

                if refund:
                    refund.delete()
                    return HttpResponse(
                        content=f'Webhook receieved: {
                            event['type']} | ERROR: {e}', status=500)

        self._send_refund_order_email(refund)
        return HttpResponse(content=f'Webhook receieved: {event['type']} | \
                            refund created in database by webhook', status=200)
