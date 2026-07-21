from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import ContactAndBillingForm, ShippingAddressForm, ExtraDetailsForm
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
    
    context={
        'form':extra_form,
    }
    template = 'checkout/checkout-step3.html'
    return render(request, template, context)