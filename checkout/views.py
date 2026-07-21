from django.http import HttpResponse
from django.shortcuts import render
from .forms import ContactAndBillingForm, PostageForm, ShippingAddressForm, ExtraDetailsForm
from .models import Order, YarnOrderLineitem
from core.models import UserProfile

def checkout_step1(request):
    """" """
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
            order.first_name = request.POST.get('first_name')
            order.second_name = request.POST.get('second_name')
            order.email = request.POST.get('email')
            order.billing_street_address1 = request.POST.get('billing_street_address1')
            order.billing_street_address2 = request.POST.get('billing_street_address2')
            order.billing_town = request.POST.get('billing_town')
            order.billing_county = request.POST.get('billing_county')
            order.billing_country = request.POST.get('billing_country')
            order.billing_postcode = request.POST.get('billing_postcode')
            if request.POST.get('billing_shipping_same' == 'on'):
                request.session['bs_same'] = True
            else:
                request.session['bs_same'] = False
            request.session['order'] = order

            return redirect(checkout_step2)
    
    context={
        'form':contact_billing_form,
    }
    template = 'checkout/checkout-step1.html'
    return render(request, template, context)