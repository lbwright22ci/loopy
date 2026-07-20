from django import forms
from .models import Order

class ContactAndBillingForm(forms.ModelForm):

    class Meta:
        model: Order
        fields:['first_name', 'second_name', 'email', 'phone', 
                'billing_street_address1', 'billing_street_address2',
                'billing_street_address1']