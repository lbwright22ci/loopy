from django.http import HttpResponse
from django.shortcuts import render
from .forms import ContactAndBillingForm, PostageForm, ShippingAddressForm, ExtraDetailsForm

from formtools.wizard.views import SessionWizardView

# Create your views here.

def show_shipping_form(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('0') or {}
    print(cleaned_data.get('billing_shipping_same'))
    return cleaned_data.get('billing_shipping_same')

class OrderForms(SessionWizardView):
    form_list = [ContactAndBillingForm, ShippingAddressForm, PostageForm, ExtraDetailsForm]
    template_name = 'checkout/checkout.html'
    condition_dict= {'1': show_shipping_form}

    def done(self, form_list, **kwargs):

        return HttpResponse('form submitted')